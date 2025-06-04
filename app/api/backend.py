from fastapi import FastAPI, Depends, HTTPException, status, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import date
from typing import List, Optional, Dict
from enum import Enum
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from database.database import Database
from database.models import Task
from database.repository import UserRepository,TaskRepository
from .websocket_manager import WebSocketManager

class HTTPSRedirectMiddleware(BaseHTTPMiddleware):
    """Middleware для автоматического перенаправления HTTP-запросов на HTTPS."""
    async def dispatch(self, request: Request, call_next):
        """
        Обрабатывает входящие запросы и модифицирует Location-заголовок для HTTPS.
        """
        response = await call_next(request)
        if response.status_code == 307 and 'location' in response.headers:
            location = response.headers['location']
            parts = location.split('/')
            location = "https://ihaveplan.andaran.fun/api/" + "/".join(parts[3:])
            response.headers['location'] = location
        return response

app = FastAPI()

# Инициализация базы данных и репозиториев
db = Database()
user_repo = UserRepository(db)
task_repo = TaskRepository(db)
websocket_manager = WebSocketManager()

origins = [
    "http://localhost:3000",
    "https://ihaveplan.andaran.fun",
]

# Добавляем middleware для обработки HTTPS
app.add_middleware(HTTPSRedirectMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic модели для запросов и ответов
class PriorityEnum(str, Enum):
    """Приоритет задачи."""
    low = "low"
    medium = "medium"
    high = "high"


class UserBase(BaseModel):
    """Базовая модель пользователя."""
    name: str
    user_info: Optional[str] = None
    telegram_id: int


class UserCreate(UserBase):
    """Модель для создания пользователя."""
    pass


class UserResponse(UserBase):
    """Модель ответа с данными пользователя."""
    id: int

    class Config:
        orm_mode = True


class TaskBase(BaseModel):
    """Базовая модель задачи."""
    title: str
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    priority: PriorityEnum = PriorityEnum.medium
    completed: bool = False
    date: date
    ai_notes: Optional[str] = None


class TaskCreate(TaskBase):
    """Модель для создания задачи."""
    user_id: int


class TaskUpdate(TaskBase):
    """Модель для обновления задачи."""
    title: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    priority: Optional[PriorityEnum] = None
    completed: Optional[bool] = None
    date: Optional[date] = None
    ai_notes: Optional[str] = None


class TaskResponse(TaskBase):
    """Модель ответа с данными задачи."""
    id: int
    user_id: int

    class Config:
        orm_mode = True


@app.websocket("/ws/{telegram_id}")
async def websocket_endpoint(websocket: WebSocket, telegram_id: int):
    """WebSocket-эндпоинт для уведомлений о задачах."""
    await websocket_manager.connect(websocket, telegram_id)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        websocket_manager.disconnect(websocket, telegram_id)

@app.post("/tasks/", response_model=TaskResponse)

async def create_task(task: TaskCreate):
    """Создаёт новую задачу."""
    try:
        task_id = task_repo.add_task(
            user_id=task.user_id,
            title=task.title,
            date=task.date,
            start_time=task.start_time,
            end_time=task.end_time,
            priority=task.priority,
            completed=task.completed,
            ai_notes=task.ai_notes
        )
        new_task = task_repo.get_task(task_id)
        user = user_repo.get_user(task.user_id)
        await websocket_manager.notify_task_update(user.telegram_id)
        return new_task
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

# Модифицируем существующие эндпоинты для отправки уведомлений
@app.post("/users/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    """Создаёт нового пользователя."""
    try:
        user_id = user_repo.add_user(
            name=user.name,
            user_info=user.user_info,
            telegram_id=user.telegram_id
        )
        return user_repo.get_user(user_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@app.get("/users/{user_id}", response_model=UserResponse)
def read_user(user_id: int):
    """Получает данные пользователя по ID."""
    user = user_repo.get_user(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


@app.get("/users_tg/{telegram_id}", response_model=UserResponse)
def read_user_by_telegram_id(telegram_id: int):
    """Получает данные пользователя по Telegram ID."""
    user = user_repo.get_user_by_telegram_id(telegram_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


# Эндпоинты для задач
@app.get("/tasks/{task_id}", response_model=TaskResponse)
def read_task(task_id: int):
    """Получает задачу по ID."""
    task = task_repo.get_task(task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return task


@app.get("/users/{user_id}/tasks/", response_model=List[TaskResponse])
def read_user_tasks(user_id: int):
    """ Получает все задачи пользователя."""
    if not user_repo.get_user(user_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return task_repo.get_tasks_by_user(user_id)


@app.get("/users_tg/{telegram_id}/tasks/", response_model=List[TaskResponse])
def read_user_tasks(telegram_id: int):
    """Получает все задачи пользователя по Telegram ID."""
    user = user_repo.get_user_by_telegram_id(telegram_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return task_repo.get_tasks_by_user(user.id)


@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: TaskUpdate):
    """Обновляет задачу."""
    existing_task = task_repo.get_task(task_id)
    if not existing_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    try:
        updated_task = task_repo.update_task(
            task_id=task_id,
            **task.model_dump(exclude_unset=True)
        )
        return updated_task
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int):
    """Удаляет задачу."""
    task = task_repo.get_task(task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    task_repo.delete_task(task_id)
    return None


@app.post("/notify_task_update/{telegram_id}")
async def notify_task_update(telegram_id: int):
    """Эндпоинт для уведомления о новых задачах"""
    await websocket_manager.notify_task_update(telegram_id)
    return {"status": "ok"}
