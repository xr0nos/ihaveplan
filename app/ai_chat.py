from neural.ai_connector import AiConnector
from database.database import Database
from database.repository import UserRepository, TaskRepository

TELEGRAM_ID = 123456789

# База данных
db = Database(dotenv_path="../.env")
user_repo = UserRepository(db)
task_repo = TaskRepository(db)

ai_connector = AiConnector("AQVN0S-PrEc6lVsqi-b4n0_5qLfQZYY6j0tv_7mo",
                            user_repo, task_repo)

while True:
    msg = input("> ")
    message = ai_connector.make_request(
        TELEGRAM_ID, msg
    )
    print(f"\n{message}\n")
