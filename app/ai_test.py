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

    ai_connector = AiConnector("AQVN0S-PrEc6lVsqi-b4n0_5qLfQZYY6j0tv_7mo",
                               user_repo, task_repo)
    bot = BotProcessor(ai_connector)

    bot.run()

    bot._call_ai(123456789, "У меня поменялось расписание, теперь в среду я свободен только с 18 часов. И добавь на ближайшую среду прогулку с другом, как раз вечером. Гулять будем 3 часа.")
    #bot._call_ai(123456789, "Перенеси его на следующий день")
