from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

Base = declarative_base()


class Database:
    def __init__(self, dotenv_path=None):
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
        return self.SessionFactory()