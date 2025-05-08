from typing import Dict, List
from fastapi import WebSocket, WebSocketDisconnect

class WebSocketManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(WebSocketManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self.active_connections: Dict[int, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, telegram_id: int):
        await websocket.accept()
        if telegram_id not in self.active_connections:
            self.active_connections[telegram_id] = []
        self.active_connections[telegram_id].append(websocket)

    def disconnect(self, websocket: WebSocket, telegram_id: int):
        if telegram_id in self.active_connections:
            self.active_connections[telegram_id].remove(websocket)
            if not self.active_connections[telegram_id]:
                del self.active_connections[telegram_id]

    async def notify_task_update(self, telegram_id: int):
        """Отправляет уведомление о том, что список задач обновился"""
        if telegram_id in self.active_connections:
            for connection in self.active_connections[telegram_id]:
                try:
                    await connection.send_json({"type": "tasks_updated"})
                except WebSocketDisconnect:
                    self.disconnect(connection, telegram_id) 