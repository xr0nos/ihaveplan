from bot.bot_processor import BotProcessor
from neural.ai_connector import AiConnector

from database.database import Database
from database.repository import UserRepository, TaskRepository
from datetime import date
from dotenv import load_dotenv
import os

import api.backend as api
import uvicorn
import threading

if __name__ == "__main__":
    # База данных
    db = Database()
    user_repo = UserRepository(db)
    task_repo = TaskRepository(db)

    load_dotenv()
    api_key = os.getenv('GPT_API')
    ai_connector = AiConnector(api_key, user_repo, task_repo)
    bot = BotProcessor(ai_connector)

    def run_api():
        uvicorn.run(api.app, host="0.0.0.0", port=8000)

    # Запускаем API в потоке-демоне
    api_thread = threading.Thread(target=run_api, daemon=True)
    api_thread.start()

    # Запускаем бота в основном потоке
    try:
        bot.run()
    except KeyboardInterrupt:
        print("Завершение работы...")
