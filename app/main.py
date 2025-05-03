from bot.bot_processor import BotProcessor
from neural.ai_connector import AiConnector

from database.database import Database
from database.repository import UserRepository, TaskRepository
from datetime import date

import api.backend as api
import uvicorn
import threading

if __name__ == "__main__":

    # База данных
    db = Database(dotenv_path="../.env")
    user_repo = UserRepository(db)
    task_repo = TaskRepository(db)

    ai_connector = AiConnector(api_key="AQVN0S-PrEc6lVsqi-b4n0_5qLfQZYY6j0tv_7mo")
    bot = BotProcessor(ai_connector)

    bot.run()

    def run_api():
        uvicorn.run(api.app, host="0.0.0.0", port=8000)
    threading.Thread(target=run_api).start()
