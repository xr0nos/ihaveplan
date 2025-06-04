from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey, Enum, BigInteger
from sqlalchemy.orm import relationship

import enum

from database.database import Base


class User(Base):
    """
    Модель пользователя системы.

    Атрибуты:
        id (int): Первичный ключ
        telegram_id (int): Уникальный идентификатор Telegram
        name (str): Имя пользователя
        user_info (str, optional): Дополнительная информация о пользователе
        tasks (relationship): Связь с задачами пользователя
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(BigInteger, nullable=False, unique=True)
    name = Column(String, nullable=False)
    user_info = Column(String, nullable=True)

    tasks = relationship("Task", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}')>"


class PriorityEnum(enum.Enum):
    """
    Перечисление для приоритетов задач.
    
    Значения:
        LOW: Низкий приоритет
        MEDIUM: Средний приоритет (по умолчанию)
        HIGH: Высокий приоритет
    """
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Task(Base):
    """
    Модель задачи пользователя.

    Атрибуты:
        id (int): Первичный ключ
        title (str): Название задачи
        start_time (str, optional): Время начала (формат HH:MM)
        end_time (str, optional): Время окончания (формат HH:MM)
        priority (PriorityEnum): Приоритет задачи
        completed (bool): Статус выполнения
        date (date): Дата выполнения задачи
        ai_notes (str, optional): Заметки ИИ
        user_id (int): Внешний ключ пользователя
        user (relationship): Связь с пользователем
    """
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    start_time = Column(String, nullable=True)
    end_time = Column(String, nullable=True)
    priority = Column(Enum(PriorityEnum), default=PriorityEnum.MEDIUM, nullable=False)
    completed = Column(Boolean, default=False, nullable=False)
    date = Column(Date, nullable=True)
    ai_notes = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    user = relationship("User", back_populates="tasks")

    def __repr__(self):
        return f"<Task(id={self.id}, title='{self.title}', date={self.date}, user_id={self.user_id})>"