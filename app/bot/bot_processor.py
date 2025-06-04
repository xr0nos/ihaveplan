from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
import asyncio
import os
from dotenv import load_dotenv
import warnings

# Подавляем предупреждение Pydantic
warnings.filterwarnings("ignore", message="Valid config keys have changed in V2")

from database.repository import UserRepository


class BotProcessor:
    """
    Основной класс для обработки Telegram-бота по планированию задач.

    Класс отвечает за:
    - Обработку команд и сообщений пользователей
    - Управление состояниями пользователей
    - Взаимодействие с AI-сервисом
    - Работу с базой данных пользователей
    """

    def __init__(self, ai_connector):
        """
        Инициализация бота, загрузка переменных окружения.

        Args:
            ai_connector: Объект для подключения к AI-сервису, должен иметь:
                         - метод make_request() для обращения к AI
                         - доступ к репозиторию пользователей _user_repo
        """
        load_dotenv()  # Загрузка переменных окружения
        self._ai_connector = ai_connector
        self._bot = None
        self._dp = None
        self._user_repo = ai_connector._user_repo

        # Состояния пользователей
        self.user_states = {}  # {telegram_id: "waiting_for_info" | None}

    async def _call_ai(self, telegram_id: int, message_text: str):
        """
        Отправляет сообщение пользователя в AI и возвращает ответ.
        Обрабатывает ошибки соединения с AI-сервисом.

        Args:
            telegram_id: ID пользователя в Telegram (int)
            message_text: Текст сообщения для обработки (str)

        Returns:
            None, но отправляет ответ пользователю через _send_message()
        """
        message = await self._ai_connector.make_request(
            telegram_id, message_text
        )
        if message:
            await self._send_message(telegram_id, message)

    async def _send_message(self, telegram_id: int, message_text: str):
        """
        Отправляет сообщение пользователю через Telegram API.
        Поддерживает HTML-разметку в сообщениях.

        Args:
            telegram_id: ID пользователя в Telegram (int)
            message_text: Текст сообщения (str), может содержать HTML-теги

        Raises:
            aiogram.exceptions.TelegramAPIError: при ошибках отправки
        """
        await self._bot.send_message(telegram_id, message_text)

    async def start_handler(self, message: Message):
        """
        Обработчик команды /start. Начинает onboarding пользователя:
        - Приветствует
        - Запрашивает информацию о расписании
        - Устанавливает состояние 'waiting_for_info'

        Args:
            message: Объект Message от aiogram с данными о сообщении
        """
        telegram_id = message.from_user.id
        welcome_text = (
            "Привет!👋 Я помогу тебе с планированием задач. Для начала расскажи мне о себе:\n"
            "1. Чем ты занимаешься\n"
            "2. Цель использования этого бота\n"
            "3. Твое расписание (когда ты занят и когда свободен)\n\n"
            "Пример ответа:\n"
            "Ставь мне все задачи на это время:\n"
            "Понедельник: с 17 до 22\n"
            "Вторник: с 15 до 20\n"
            "Среда: весь день\n"
            "Четверг: с 20 до 22\n"
            "Пятница: с 18 до 23\n"
            "Суббота: свободен\n"
            "Воскресенье: весь день, но лучше не ставить.\n"
            "Между задачами делай перерыв 30 минут. Задачи, которые занимают больше 4 часов дели на несколько."
        )

        self.user_states[telegram_id] = "waiting_for_info"
        await self._send_message(telegram_id, welcome_text)

    async def message_handler(self, message: Message):
        """
        Основной обработчик сообщений. Реализует логику:
        - Обработка информации о пользователе (в состоянии waiting_for_info)
        - Сохранение данных в БД
        - Передача обычных сообщений в AI
        - Управление состояниями диалога

        Args:
            message: Объект Message от aiogram с данными о сообщении
        """
        telegram_id = message.from_user.id
        message_text = message.text

        if self.user_states.get(telegram_id) == "waiting_for_info":
            name = message.from_user.first_name or message.from_user.username or "Пользователь"
            user_info = f"Меня зовут {name}. !!!ОЧЕНЬ ВАЖНО!!! Запомни моё свободное время и никогда не" \
                        "добавляй задачи на часы, когда я занят.\n"
            user_info += message_text

            user = self._user_repo.get_user_by_telegram_id(telegram_id)
            if user:
                self._user_repo.update_user(user.id, name=name, user_info=user_info)
            else:
                self._user_repo.add_user(name=name, telegram_id=telegram_id, user_info=user_info)

            self.user_states[telegram_id] = None
            await self._send_message(
                telegram_id,
                "Я запомнил инфу о тебе. Если захочешь добавить еще что-то, напиши: \"запомни, что ...\""
            )
            return

        await self._call_ai(telegram_id, message_text)

    def run(self):
        """
        Запускает бота. Выполняет:
        - Инициализацию бота с токеном из .env
        - Настройку диспетчера
        - Регистрацию обработчиков
        - Запуск long-polling

        Для остановки требуется ручное прерывание (Ctrl+C).
        """

        async def main():
            self._bot = Bot(
                token=os.getenv('BOT_TOKEN'),
                default=DefaultBotProperties(parse_mode=ParseMode.HTML)
            )
            self._dp = Dispatcher()

            self._dp.message.register(self.start_handler, Command("start"))
            self._dp.message.register(self.message_handler)

            await self._dp.start_polling(self._bot)

        asyncio.run(main())