const API_BASE_URL = 'http://localhost:8000';

export const fetchUserTasks = async (userId) => {
  try {
    const response = await fetch(`${API_BASE_URL}/users_tg/${userId}/tasks/`);
    if (!response.ok) throw new Error('Network error');
    const data = await response.json();
    
    return data.map((task) => ({
      id: task.id,
      title: task.title,
      startTime: task.start_time,
      endTime: task.end_time,
      priority: task.priority,
      completed: task.completed,
      date: task.date,
    }));
  } catch (err) {
    console.error('Fetch error:', err);
    throw err;
  }
};

export const updateTaskCompletion = async (taskId, completed) => {
  try {
    const response = await fetch(`${API_BASE_URL}/tasks/${taskId}/`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ completed }),
    });

    if (!response.ok) throw new Error('Network error');
    return response.json();
  } catch (err) {
    console.error('Update error:', err);
    throw err;
  }
}; 