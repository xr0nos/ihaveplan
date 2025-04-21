from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from datetime import date
from typing import List, Optional
from enum import Enum

from database.database import Database
from database.models import Task
from database.repository import UserRepository,TaskRepository

app = FastAPI()

# Инициализация базы данных и репозиториев
db = Database()
user_repo = UserRepository(db)
task_repo = TaskRepository(db)


# Pydantic модели для запросов и ответов
class PriorityEnum(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class UserBase(BaseModel):
    name: str
    user_info: Optional[str] = None
    tasks_info: Optional[str] = None


class UserCreate(UserBase):
    pass


class UserResponse(UserBase):
    id: int

    class Config:
        orm_mode = True


class TaskBase(BaseModel):
    title: str
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    priority: PriorityEnum = PriorityEnum.medium
    completed: bool = False
    date: Optional[date] = None
    ai_notes: Optional[str] = None


class TaskCreate(TaskBase):
    user_id: int


class TaskResponse(TaskBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True


# Эндпоинты для пользователей
@app.post("/users/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate):
    try:
        user_id = user_repo.add_user(
            name=user.name,
            user_info=user.user_info,
            tasks_info=user.tasks_info
        )
        return user_repo.get_user(user_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@app.get("/users/{user_id}", response_model=UserResponse)
def read_user(user_id: int):
    user = user_repo.get_user(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


# Эндпоинты для задач
@app.post("/tasks/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate):
    # Проверяем существует ли пользователь
    if not user_repo.get_user(task.user_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    try:
        task_id = task_repo.add_task(
            user_id=task.user_id,
            title=task.title,
            start_time=task.start_time,
            end_time=task.end_time,
            priority=task.priority.value,
            completed=task.completed,
            date=task.date,
            ai_notes=task.ai_notes
        )
        return task_repo.get_task(task_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@app.get("/tasks/{task_id}", response_model=TaskResponse)
def read_task(task_id: int):
    task = task_repo.get_task(task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return task


@app.get("/users/{user_id}/tasks/", response_model=List[TaskResponse])
def read_user_tasks(user_id: int):
    if not user_repo.get_user(user_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return task_repo.get_tasks_by_user(user_id)


@app.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task: TaskBase):
    try:
        updated_task = task_repo.update_task(
            task_id=task_id,
            title=task.title,
            start_time=task.start_time,
            end_time=task.end_time,
            priority=task.priority.value,
            completed=task.completed,
            date=task.date,
            ai_notes=task.ai_notes
        )
        if not updated_task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
        return updated_task
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int):
    task = task_repo.get_task(task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    task_repo.delete_task(task_id)
    return None

