from datetime import datetime
from database.repository import UserRepository, TaskRepository


class CommandsEngine:
    """
    Движок для выполнения команд, полученных от ИИ-ассистента.

    Обеспечивает:
    - Валидацию входящих команд
    - Добавление, удаление и обновление задач
    - Обновление информации о пользователе
    - Обработку ошибок выполнения команд
    """

    def __init__(self, user_repo: UserRepository, task_repo: TaskRepository):
        """
        Инициализация движка команд.

        Аргументы:
            user_repo: Репозиторий для работы с пользователями
            task_repo: Репозиторий для работы с задачами
        """
        self._user_repo = user_repo
        self._task_repo = task_repo

    def _add_task(self, telegram_id, command: dict):
        """
        Добавляет новую задачу для пользователя.

        Аргументы:
            telegram_id: ID пользователя в Telegram
            command: Словарь

        Логика работы:
            1. Проверяет наличие всех обязательных параметров
            2. Проверяет типы параметров
            3. Находит пользователя по telegram_id
            4. Преобразует дату из строки в объект date
            5. Добавляет задачу через репозиторий
        """
        required_params = {
            "title": str,
            "start_time": str,
            "end_time": str,
            "date": str,
            "ai_notes": str
        }
        for param, param_type in required_params.items():
            if param not in command:
                raise ValueError(f"Missing parameter: {param}")
            if not isinstance(command[param], param_type):
                raise ValueError(f"Invalid type for parameter: {param}. Expected {param_type.__name__}.")
        
        # Получаем ID пользователя
        user = self._user_repo.get_user_by_telegram_id(telegram_id)
        if not user:
            raise ValueError(f"User with telegram ID {telegram_id} not found.")
        
        # Добавляем задачу
        try:
            date_obj = datetime.strptime(command["date"], "%Y-%m-%d")
        except ValueError:
            raise ValueError("Invalid date format. Expected YYYY-MM-DD.")

        task = self._task_repo.add_task(
            user_id=user.id,
            title=command["title"],
            start_time=command["start_time"],
            end_time=command["end_time"],
            date=date_obj,
            ai_notes=command["ai_notes"]
        )


    def _delete_task(self, telegram_id, command: dict):
        """
        Удаляет задачу пользователя.

        Аргументы:
            telegram_id: ID пользователя в Telegram
            command: Словарь

        Логика работы:
            1. Проверяет наличие task_id
            2. Проверяет тип task_id
            3. Находит пользователя
            4. Проверяет существование задачи
            5. Проверяет принадлежность задачи пользователю
            6. Удаляет задачу через репозиторий
        """

        if "task_id" not in command:
            raise ValueError("Missing parameter: task_id")
        if not isinstance(command["task_id"], int):
            raise ValueError("Invalid type for parameter: task_id. Expected int.")
        
        # Получаем ID пользователя
        user_id = self._user_repo.get_user_by_telegram_id(telegram_id).id
        if not user_id:
            raise ValueError(f"User with telegram ID {telegram_id} not found.")
        
        # Удаляем задачу
        task = self._task_repo.get_task(command["task_id"])
        if not task:
            raise ValueError(f"Task with ID {command['task_id']} not found.")
        if task.user_id != user_id:
            raise ValueError(f"Task with ID {command['task_id']} does not belong to user with telegram ID {telegram_id}.")
        self._task_repo.delete_task(command["task_id"])
        

    def _update_user_info(self, telegram_id, command: dict):
        """
        Обновляет информацию о пользователе.

        Аргументы:
            telegram_id: ID пользователя в Telegram
            command: Словарь

        Логика работы:
            1. Проверяет наличие user_info
            2. Проверяет тип user_info
            3. Находит пользователя
            4. Обновляет информацию через репозиторий
        """
        # Валидация параметров
        if "user_info" not in command:
            raise ValueError("Missing parameter: user_info")
        if not isinstance(command["user_info"], str):
            raise ValueError("Invalid type for parameter: user_info. Expected str.")
        
        # Получаем ID пользователя
        user = self._user_repo.get_user_by_telegram_id(telegram_id)
        if not user:
            raise ValueError(f"User with telegram ID {telegram_id} not found.")
        
        # Обновляем информацию о пользователе
        self._user_repo.update_user(user.id, user_info=command["user_info"])

    def execute(self, telegram_id, command: dict):
        """
        Основной метод для выполнения команд.

        Аргументы:
            telegram_id: ID пользователя в Telegram
            command: Словарь с командой


        Логика работы:
            1. Определяет тип команды
            2. Вызывает соответствующий метод
            3. Логирует выполнение команды

        """
        print(f"Executing command: {command['command']} for user: {telegram_id}")
        match command["command"]:
            case "add_task":
                self._add_task(telegram_id, command["params"])
            case "delete_task":
                self._delete_task(telegram_id, command["params"])
            case "update_user_info":
                self._update_user_info(telegram_id, command["params"])
            case _:
                raise ValueError(f"Unknown command: {command['command']}")
