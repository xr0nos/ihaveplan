import requests
from typing import Dict, List
from datetime import datetime, timedelta
from commands.commands_engine import CommandsEngine
from api.websocket_manager import WebSocketManager
import json


class AiConnector:
    """Класс для взаимодействия с нейросетевым API и управления пользовательскими запросами.

    Отвечает за:
    - Отправку запросов к Yandex GPT API
    - Ведение истории диалогов пользователей
    - Обработку информации о пользователях и их задачах
    - Выполнение команд на основе ответов ИИ
    - Управление WebSocket-уведомлениями
    """

    def __init__(self, api_key, user_repo, task_repo):
        """
        Инициализирует подключение к AI-сервису и настраивает необходимые компоненты.

        Аргументы:
            api_key (str): API-ключ для доступа к Yandex GPT API
            user_repo: Репозиторий для работы с пользователями (должен реализовывать интерфейс UserRepository)
            task_repo: Репозиторий для работы с задачами (должен реализовывать интерфейс TaskRepository)

        Инициализирует:
            - Параметры подключения к Yandex GPT API:
                * URL API (_api_url)
                * HTTP-заголовки (_headers)
                * URI модели (_model_uri)
                * Параметры запроса по умолчанию (_default_options)

            - Системные компоненты:
                * История диалогов пользователей (_user_histories)
                * Системный промпт (_system_prompt) - загружается из файла neural/system_prompt.txt
                * Движок команд (_commands_engine)
                * Менеджер WebSocket-соединений (_websocket_manager)
                * Словарь соответствия дней недели (_days_of_week)

        """
        self._api_url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
        self._headers = {
            "Content-Type": "application/json",
            "Authorization": f"Api-Key {api_key}"
        }
        self._model_uri = "gpt://b1gkd7sr0i2ipteg0eqg/llama"
        self._default_options = {
            "stream": False,
            "temperature": 0.5,
            "maxTokens": "2000"
        }
        # Истории запросов пользователей
        self._user_histories: Dict[int, Dict[str, str]] = {}
        self._system_prompt = {
            "role": "system", 
            "text": open("neural/system_prompt.txt", "r").read()
        }
        # Репозитории
        self._user_repo = user_repo
        self._task_repo = task_repo
        # Обработка команд
        self._commands_engine = CommandsEngine(user_repo, task_repo)
        # Менеджер сокетов
        self._websocket_manager = WebSocketManager()
        # Дни недели
        self._days_of_week = {
            "(Monday)": "Понедельник",
            "(Tuesday)": "Вторник",
            "(Wednesday)": "Среда",
            "(Thursday)": "Четверг",
            "(Friday)": "Пятница",
            "(Saturday)": "Суббота",
            "(Sunday)": "Воскресенье"
        }


    def _get_user_info(self, telegram_id: int) -> str:
        """
        Формирует подробную информацию о пользователе и его задачах для системного промпта.

        Собирает:
        - Основную информацию о пользователе
        - Календарь задач на ближайшие 2 недели
        - Важные предупреждения о доступном времени

        Аргументы:
            telegram_id: Уникальный идентификатор пользователя в Telegram

        Возвращает:
            Отформатированную строку с полной информацией о пользователе,
            включая расписание на 14 дней

            Для дней без задач возвращает: '[дата]: нет задач'
        """
        user = self._user_repo.get_user_by_telegram_id(telegram_id)
        res = "\n\nКалендарь пользователя на ближайшие 2 недели: (уже сохранен, снова сохранять не нужно):\n"
        tasks = self._task_repo.get_tasks_for_ai(telegram_id)
        today = datetime.now()
        res += f'Сегодня {today.strftime("%H:%M")} '
        for i in range(14):
            date = today.strftime("%Y-%m-%d (%A)")
            date = date.replace(date.split()[1], self._days_of_week[date.split()[1]])
            today_tasks = [task for task in tasks if task.date == today.date()]
            if today_tasks:
                res += f"{date}:\n"
                for task in today_tasks:
                    res += f" - {task.title} ({task.start_time} - {task.end_time}). id: {task.id}. Заметки AI: {task.ai_notes}\n"
            else:
                res += f"{date}: нет задач\n"
            today = today + timedelta(days=1)
        res += "\n!!!ОЧЕНЬ ВАЖНО: Всегда сверяй время новой задачи с информацией о пользователе ниже:\n"
        res += f"\n\"{user.user_info}\"\n"
        res += "\n!!!ОЧЕНЬ ВАЖНО: Добавляй задачу только на то время, когда пользователь свободен. Задачи не должны ставиться на недоступное время — даже если кажется, что «влезет»."
        
        return res


    def _add_message(self, telegram_id: int, role: str, text: str) -> None:
        """
        Добавляет сообщение в историю переписки пользователя.

        Аргументы:
            telegram_id: ID пользователя в Telegram
            role: Роль отправителя ('user' для пользователя, 'assistant' для ИИ)
            text: Текст сообщения для сохранения
        """
        if telegram_id not in self._user_histories:
            self._user_histories[telegram_id] = []
        self._user_histories[telegram_id].append({"role": role, "text": text})


    def _parse_response(self, response):
        """
        Извлекает текстовый ответ из JSON-ответа нейросети.

        Аргументы:
            response: Ответ от API Yandex GPT в формате JSON

        Возвращает:
            Текст ответа нейросети или None при ошибке парсинга
        """
        try:
            return response['result']['alternatives'][0]['message']['text']
        except Exception:
            return None


    def _send_message(self, telegram_id):
        """
        Отправляет подготовленный запрос к API нейросети.

        Аргументы:
            telegram_id: ID пользователя для которого отправляется запрос

        Возвращает:
            Ответ нейросети (результат _parse_response) или None при ошибке сети
        """
        system_prompt = self._system_prompt.copy()
        system_prompt["text"] += self._get_user_info(telegram_id)
        prompt = {
            "modelUri": self._model_uri,
            "completionOptions": self._default_options,
            "messages": [system_prompt] + self._user_histories[telegram_id]
        }

        try:
            response = requests.post(self._api_url, headers=self._headers, json=prompt)
            return self._parse_response(response.json())
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return None
        

    async def make_request(self, telegram_id: int, message_text: str):
        """
        Основной метод для взаимодействия с нейросетью (публичный интерфейс).

        Полный цикл обработки:
        1. Сохраняет сообщение пользователя
        2. Отправляет запрос к ИИ
        3. Обрабатывает ответ
        4. Выполняет команды (если есть)
        5. Отправляет уведомления через WebSocket
        6. Возвращает ответ пользователю

        Аргументы:
            telegram_id: ID пользователя в Telegram
            message_text: Текст сообщения от пользователя

        Возвращает:
            Текст ответа для пользователя или сообщение об ошибке

        """
        if telegram_id not in self._user_histories:
            self._user_histories[telegram_id] = []

        self._add_message(telegram_id, "user", message_text)
        response = self._send_message(telegram_id)
        
        if not response:
            return "Неизвестная ошибка. Попробуйте еще раз."
        
        self._add_message(telegram_id, "assistant", response)
        # Удаляем старые сообщения, если их больше 6
        if len(self._user_histories[telegram_id]) > 6:
            self._user_histories[telegram_id] = self._user_histories[telegram_id][-6:]

        # Парсинг струкруты ответа
        response = response.replace("```json", "")
        response = response.replace("```", "")
        try:
            data = json.loads(response)
        except json.decoder.JSONDecodeError as e:
            print("Ошибка парсинга JSON:", e)
            return "Неизвестная ошибка. Попробуйте еще раз."
        
        # Исполняем команды
        if data.get("commands"):
            print()
            for command in data["commands"]:
                try:
                    self._commands_engine.execute(telegram_id, command)
                except ValueError as e:
                    print(f"Ошибка выполнения команды: {e}")
                    return "Неизвестная ошибка. Попробуйте еще раз."
            
            # Отправляем уведомление через WebSocket
            await self._websocket_manager.notify_task_update(telegram_id)
            
        # Отвечаем пользователю
        return data.get("answer", "Неизвестная ошибка. Попробуйте еще раз.")
