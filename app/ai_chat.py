from neural.ai_connector import AiConnector
from database.database import Database
from database.repository import UserRepository, TaskRepository
from api.websocket_manager import WebSocketManager
import asyncio
import threading
import uvicorn
import api.backend as api

TELEGRAM_ID = 123456789

# База данных
db = Database(dotenv_path="../.env")
user_repo = UserRepository(db)
task_repo = TaskRepository(db)

ai_connector = AiConnector("AQVN0S-PrEc6lVsqi-b4n0_5qLfQZYY6j0tv_7mo",
                            user_repo, task_repo)


async def main():
    while True:
        msg = input("> ")
        message = await ai_connector.make_request(
            TELEGRAM_ID, msg
        )
        print(f"\n{message}\n")

if __name__ == "__main__":
    def run_api():
        uvicorn.run(api.app, host="0.0.0.0", port=8000, log_level="error")
    threading.Thread(target=run_api).start()
    
    asyncio.run(main())
