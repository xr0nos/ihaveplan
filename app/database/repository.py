
from datetime import date
from typing import Optional

from database.database import Database
from database.models import User, PriorityEnum, Task


class UserRepository:
    def __init__(self, db: Database):
        self.db = db

    def add_user(self, name: str, user_info: str = None, tasks_info: str = None) -> int:
        session = self.db.get_session()
        try:
            user = User(name=name, user_info=user_info, tasks_info=tasks_info)
            session.add(user)
            session.commit()
            return user.id
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def update_user(self, user_id: int, name: str = None, user_info: str = None, tasks_info: str = None):
        session = self.db.get_session()
        try:
            user = session.query(User).filter_by(id=user_id).first()
            if user:
                if name is not None:
                    user.name = name
                if user_info is not None:
                    user.user_info = user_info
                if tasks_info is not None:
                    user.tasks_info = tasks_info
                session.commit()
            return user
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def delete_user(self, user_id: int):
        session = self.db.get_session()
        try:
            user = session.query(User).filter_by(id=user_id).first()
            if user:
                session.delete(user)
                session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def get_user(self, user_id: int) -> User:
        session = self.db.get_session()
        try:
            return session.query(User).filter_by(id=user_id).first()
        finally:
            session.close()

class TaskRepository:
    def __init__(self, db: Database):
        self.db = db

    def add_task(self, user_id: int, title: str, start_time: str = None, 
                 end_time: str = None, priority: str = "medium", completed: bool = False, 
                 date: date = None, ai_notes: str = None) -> int:
        session = self.db.get_session()
        try:
            priority_enum = PriorityEnum(priority.lower())
            task = Task(
                user_id=user_id, title=title, start_time=start_time, end_time=end_time,
                priority=priority_enum, completed=completed, date=date, ai_notes=ai_notes
            )
            session.add(task)
            session.commit()
            return task.id
        except ValueError as e:
            raise ValueError(f"Недопустимое значение приоритета: {priority}. Должно быть 'low', 'medium' или 'high'")
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def update_task(self, task_id: int, title: str = None, start_time: str = None, 
                    end_time: str = None, priority: str = None, completed: bool = None, 
                    date: date = None, ai_notes: str = None):
        session = self.db.get_session()
        try:
            task = session.query(Task).filter_by(id=task_id).first()
            if task:
                if title is not None:
                    task.title = title
                if start_time is not None:
                    task.start_time = start_time
                if end_time is not None:
                    task.end_time = end_time
                if priority is not None:
                    task.priority = PriorityEnum(priority.lower())
                if completed is not None:
                    task.completed = completed
                if date is not None:
                    task.date = date
                if ai_notes is not None:
                    task.ai_notes = ai_notes
                session.commit()
            return task
        except ValueError as e:
            raise ValueError(f"Недопустимое значение приоритета: {priority}. \
                             Должно быть 'low', 'medium' или 'high'")
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def delete_task(self, task_id: int):
        session = self.db.get_session()
        try:
            task = session.query(Task).filter_by(id=task_id).first()
            if task:
                session.delete(task)
                session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def get_tasks_by_user(self, user_id: int) -> list[Task]:
        session = self.db.get_session()
        try:
            return session.query(Task).filter_by(user_id=user_id).all()
        finally:
            session.close()

    def get_tasks_by_time_range(self, user_id: int, start_range: date, end_range: date) -> list[Task]:
        session = self.db.get_session()
        try:
            if start_range > end_range:
                raise ValueError("start_range должен быть раньше или равен end_range")
            
            tasks = session.query(Task).filter(
                Task.user_id == user_id,
                Task.date.between(start_range, end_range)
            ).all()
            return tasks
        except Exception as e:
            raise e
        finally:
            session.close()

    def get_task(self, task_id: int) -> Optional[Task]:
        session = self.db.get_session()
        try:
            return session.query(Task).filter(Task.id == task_id).first()
        finally:
            session.close()