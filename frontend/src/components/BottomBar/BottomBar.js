'use client'

import styles from './BottomBar.module.css'

export default function BottomBar({ view, onViewChange, onTodayClick }) {
  return (
    <div className={styles.bottomBar}>
      <div className={styles.viewToggle}>
          <button
            onClick={() => onViewChange('dayGridMonth')}
            className={`${styles.toggleButton} ${view === 'dayGridMonth' ? styles.active : ''}`}
          >
            М
          </button>
          <button
            onClick={() => onViewChange('timeGridWeek')}
            className={`${styles.toggleButton} ${view === 'timeGridWeek' ? styles.active : ''}`}
          >
            Н
          </button>
          <button
            onClick={() => onViewChange('timeGridDay')}
            className={`${styles.toggleButton} ${view === 'timeGridDay' ? styles.active : ''}`}
          >
            Д
          </button>
        </div>
        <button onClick={onTodayClick} className={styles.todayButton}>
          Сегодня
        </button>
    </div>
  )
}