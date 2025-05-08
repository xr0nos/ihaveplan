import { useEffect, useRef, useCallback } from 'react';
import { fetchUserTasks } from './tasksApi';

export const useWebSocket = (userId, onTasksUpdate) => {
  const ws = useRef(null);
  const onTasksUpdateRef = useRef(onTasksUpdate);

  // Обновляем ref при изменении колбэка
  useEffect(() => {
    onTasksUpdateRef.current = onTasksUpdate;
  }, [onTasksUpdate]);

  const handleMessage = useCallback(async (event) => {
    const data = JSON.parse(event.data);
    if (data.type === 'tasks_updated') {
      try {
        const updatedTasks = await fetchUserTasks(userId);
        onTasksUpdateRef.current(updatedTasks);
      } catch (err) {
        console.error('Error fetching updated tasks:', err);
      }
    }
  }, [userId]);

  useEffect(() => {
    if (!userId) return;

    // Создаем WebSocket соединение
    ws.current = new WebSocket(`ws://localhost:8000/ws/${userId}`);

    // Обработчики событий
    ws.current.onopen = () => {
      console.log('WebSocket соединение установлено');
    };

    ws.current.onmessage = handleMessage;

    ws.current.onerror = (error) => {
      console.error('WebSocket ошибка:', error);
    };

    ws.current.onclose = () => {
      console.log('WebSocket соединение закрыто');
    };

    // Очистка при размонтировании
    return () => {
      if (ws.current) {
        ws.current.close();
      }
    };
  }, [userId, handleMessage]);

  return ws.current;
}; 