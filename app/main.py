from bot.bot_processor import BotProcessor
from neural.ai_connector import AiConnector

from database.database import Database
from database.repository import UserRepository, TaskRepository
from datetime import date

if __name__ == "__main__":
    
    # База данных
    db = Database(dotenv_path="../.env")
    user_repo = UserRepository(db)
    task_repo = TaskRepository(db)

    # Добавляем пользователя
    user_id = user_repo.add_user("Алексей", user_info="Программист", tasks_info="Много задач")
    print(f"Добавлен пользователь с ID: {user_id}")

    # Добавляем несколько задач
    task1_id = task_repo.add_task(
        user_id=user_id, title="Написать код", start_time="09:00",
        end_time="12:00", priority="high", date=date(2025, 4, 1)
    )
    task2_id = task_repo.add_task(
        user_id=user_id, title="Тестирование", start_time="14:00",
        end_time="16:00", priority="medium", date=date(2025, 4, 2)
    )
    task3_id = task_repo.add_task(
        user_id=user_id, title="Планирование", start_time="10:00",
        priority="low", date=date(2025, 4, 3)
    )

    # Задаём диапазон дат
    start_range = date(2025, 4, 1)  # 1 апреля
    end_range = date(2025, 4, 2)    # 2 апреля

    # Получаем задачи в заданном диапазоне
    tasks_in_range = task_repo.get_tasks_by_time_range(user_id, start_range, end_range)
    print(f"Задачи в диапазоне {start_range} - {end_range}:")
    for task in tasks_in_range:
        print(task)

    # Удаляем задачи и пользователя для очистки
    task_repo.delete_task(task1_id)
    task_repo.delete_task(task2_id)
    task_repo.delete_task(task3_id)
    user_repo.delete_user(user_id)

    # -------------------------

    # Пример использования классов
    ai_connector = AiConnector()
    bot = BotProcessor(ai_connector)

    bot.run()
