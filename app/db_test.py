from database.database import Database
from database.repository import UserRepository, TaskRepository
from datetime import date


if __name__ == "__main__":

    # База данных
    db = Database(dotenv_path="../.env")
    user_repo = UserRepository(db)
    task_repo = TaskRepository(db)

    # Добавляем пользователя
    user_repo.delete_user(1)
    user_id = user_repo.add_user("Андрей", user_info="Программист", telegram_id=123456789)
    # print(f"Добавлен пользователь с ID: {user_id}")

    # # Добавляем несколько задач
    # task1_id = task_repo.add_task(
    #     user_id=user_id, title="Написать код", start_time="09:00",
    #     end_time="12:00", priority="high", date=date(2025, 4, 1)
    # )
    # task2_id = task_repo.add_task(
    #     user_id=1, title="Тестирование", start_time="14:00",
    #     end_time="16:00", priority="medium", date=date(2025, 5, 10)
    # )
    # task3_id = task_repo.add_task(
    #     user_id=1, title="Планирование", start_time="10:00", end_time="11:00",
    #     priority="low", date=date(2025, 5, 11)
    # )

    # # Задаём диапазон дат
    # start_range = date(2025, 4, 1)  # 1 апреля
    # end_range = date(2025, 4, 2)    # 2 апреля

    # # Получаем задачи в заданном диапазоне
    # tasks_in_range = task_repo.get_tasks_by_time_range(user_id, start_range, end_range)
    # print(f"Задачи в диапазоне {start_range} - {end_range}:")
    # for task in tasks_in_range:
    #     print(task)

    # # Удаляем задачи и пользователя для очистки
    # task_repo.delete_task(task1_id)
    # task_repo.delete_task(task2_id)
    # task_repo.delete_task(task3_id)
    # user_repo.delete_user(1)

    # Обновить пользователя
    user = user_repo.update_user(2, name="Андрей", 
                                 user_info="Меня зовут Андрей. Запомни моё свободное время и никогда не добавляй задачи на часы, когда я занят. В понедельник свободен с 16 часов. Во вторник - с 17. В среду свободен весь день. В четверг и пятницу свободет только вечер с 20 часов (я уставший, назначать на это время дела в крайнем случае). В выходные свободен, но по воскресеньям стараюсь не работать. Все дела делаю до 23 часов. На домашку по ТПР у меня обычно уходит 4 часа.")
