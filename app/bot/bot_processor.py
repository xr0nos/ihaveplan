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
    def __init__(self, ai_connector):
        """
        Инициализация класса BotProcessor
        :param ai_connector: Объект для подключения к AI
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
        Метод для вызова Yandex GPT
        """
        message = await self._ai_connector.make_request(
            telegram_id, message_text
        )
        if message:
            await self._send_message(telegram_id, message)

    async def _send_message(self, telegram_id: int, message_text: str):
        """
        Метод для отправки сообщения пользователю
        """
        await self._bot.send_message(telegram_id, message_text)

    async def start_handler(self, message: Message):
        """
        Обработчик команды /start
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
        Обработчик обычных сообщений
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
        Запуск бота
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
