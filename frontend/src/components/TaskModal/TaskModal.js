import React from 'react';
import styles from './TaskModal.module.css';

const TaskModal = ({ task, isOpen, onClose, onToggleComplete }) => {
  if (!isOpen) return null;

  const formatDate = (dateStr) => {
    const date = new Date(dateStr);
    return date.toLocaleDateString('ru-RU', {
      day: 'numeric',
      month: 'long',
      year: 'numeric'
    });
  };

  return (
    <div className={styles.modalOverlay} onClick={onClose}>
      <div className={styles.modalContent} onClick={e => e.stopPropagation()}>
        <h2 className={styles.title}>{task.title}</h2>
        
        <div className={styles.timeInfo}>
          <p className={styles.date}>{formatDate(task.date)}</p>
          <p className={styles.timeInterval}>
            {task.startTime} — {task.endTime}
          </p>
        </div>

        <div className={styles.completionToggle}>
          <label className={styles.switch}>
            <input
              type="checkbox"
              checked={task.completed}
              onChange={onToggleComplete}
            />
            <span className={styles.slider}></span>
          </label>
          <span className={styles.statusText}>
            {task.completed ? 'Выполнено' : 'Не выполнено'}
          </span>
        </div>

        <button className={styles.closeButton} onClick={onClose}>
          ✕
        </button>
      </div>
    </div>
  );
};

export default TaskModal; 