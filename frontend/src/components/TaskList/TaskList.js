import styles from './TaskList.module.css'

export default function TaskList({ tasks, setTasks }) {
  const handleToggleComplete = (taskId) => {
    setTasks(tasks.map(task => 
      task.id === taskId 
        ? { ...task, completed: !task.completed }
        : task
    ))
  }

  return (
    <div className={styles.taskList}>
      {tasks.length === 0 ? (
        <p>На этот день задач нет</p>
      ) : (
        <ul>
          {tasks.map(task => (
            <li 
              key={task.id}
              className={`${styles.taskItem} ${task.completed ? styles.completed : ''}`}
            >
              <div className={styles.taskInfo}>
                <input
                  type="checkbox"
                  checked={task.completed}
                  onChange={() => handleToggleComplete(task.id)}
                />
                <span className={styles.time}>{task.time}</span>
                <span className={styles.title}>{task.title}</span>
              </div>
              <span className={`${styles.priority} ${styles[task.priority]}`}>
                {task.priority === 'high' ? 'Важно' : 
                 task.priority === 'medium' ? 'Средне' : 'Не важно'}
              </span>
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}