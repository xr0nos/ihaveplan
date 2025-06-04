from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

Base = declarative_base()


class Database:
    """
    Класс для управления подключением к базе данных и сессиями SQLAlchemy.

    Реализует:
    - Подключение к БД на основе переменных окружения
    - Создание сессий для работы с БД
    - Автоматическое создание таблиц (если не существуют)
    - Контекстный менеджер для сессий

    Args:
        dotenv_path (Optional[str]): Путь к .env файлу (если не стандартный)
    """
    def __init__(self, dotenv_path=None):
        """
        Инициализирует подключение к базе данных.

        Raises:
            ValueError: Если не найдена переменная DB_URL в .env файле
            sqlalchemy.exc.SQLAlchemyError: При ошибках подключения к БД
        """
        if dotenv_path:
            load_dotenv(dotenv_path=dotenv_path)
        else:
            load_dotenv()

        db_url = os.getenv("DB_URL")
        if not db_url:
            raise ValueError("Переменная DB_URL не найдена в .env файле")

        self.engine = create_engine(db_url, echo=False)
        Base.metadata.create_all(self.engine)
        self.SessionFactory = sessionmaker(bind=self.engine)

    def get_session(self):
        """
        Создает и возвращает новую сессию для работы с БД.

        Returns:
            sqlalchemy.orm.Session: Объект сессии SQLAlchemy

        Note:
            Не забывайте закрывать сессию после использования!
            Лучше использовать контекстный менеджер session_scope().
        """
        return self.SessionFactory()