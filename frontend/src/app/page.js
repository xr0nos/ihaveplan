'use client'

import { useState, useEffect, useRef } from 'react'
import FullCalendar from '@fullcalendar/react'
import dayGridPlugin from '@fullcalendar/daygrid'
import timeGridPlugin from '@fullcalendar/timegrid'
import interactionPlugin from '@fullcalendar/interaction'
import { useSwipeable } from 'react-swipeable'
import styles from './page.module.css'
import axios from 'axios'

export default function Home() {
  const [date, setDate] = useState(new Date())
  const [tasks, setTasks] = useState([])
  const [loading, setLoading] = useState(false)
  const [view, setView] = useState('timeGridWeek')
  const calendarRef = useRef(null)

  useEffect(() => {
    const fetchTasks = async () => {
      setLoading(true)
      try {
        setTasks([
          {
            id: 1,
            title: 'Утренняя зарядка',
            startTime: '08:00',
            endTime: '08:30',
            priority: 'low',
            completed: false,
            date: new Date().toISOString().split('T')[0]
          },
          {
            id: 2,
            title: 'Встреча',
            startTime: '10:30',
            endTime: '11:30',
            priority: 'high',
            completed: false,
            date: new Date().toISOString().split('T')[0]
          },
          {
            id: 3,
            title: 'Презентация',
            startTime: '14:00',
            endTime: '15:00',
            priority: 'medium',
            completed: false,
            date: new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString().split('T')[0]
          }
        ])
      } catch (error) {
        console.error('Error fetching tasks:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchTasks()
  }, [date])

  const handleDateChange = (info) => {
    setDate(info.view.currentStart)
  }

  const handleViewChange = (newView) => {
    setView(newView)
    if (calendarRef.current) {
      calendarRef.current.getApi().changeView(newView)
    }
  }

  const handlers = useSwipeable({
    onSwipedLeft: () => calendarRef.current?.getApi().next(),
    onSwipedRight: () => calendarRef.current?.getApi().prev(),
    trackTouch: true,
    delta: 5
  })

  // Упрощаем отображение задач — только заголовок
  const events = tasks.map(task => ({
    id: task.id,
    title: task.title, // Убираем время из заголовка
    start: `${task.date}T${task.startTime}:00`,
    end: `${task.date}T${task.endTime}:00`,
    className: styles[task.priority],
    extendedProps: {
      priority: task.priority,
      startTime: task.startTime, // Сохраняем время для всплывающей подсказки
      endTime: task.endTime,
      completed: task.completed
    }
  }))

  return (
    <main className={styles.main}>
      <div className={styles.viewSwitcher}>
        <button
          onClick={() => handleViewChange('dayGridMonth')}
          className={`${styles.viewButton} ${view === 'dayGridMonth' ? styles.active : ''}`}
        >
          М
        </button>
        <button
          onClick={() => handleViewChange('timeGridWeek')}
          className={`${styles.viewButton} ${view === 'timeGridWeek' ? styles.active : ''}`}
        >
          Н
        </button>
        <button
          onClick={() => handleViewChange('timeGridDay')}
          className={`${styles.viewButton} ${view === 'timeGridDay' ? styles.active : ''}`}
        >
          Д
        </button>
      </div>
      <div className={styles.calendarContainer} {...handlers}>
        {loading ? (
          <p>Загрузка...</p>
        ) : (
          <FullCalendar
            ref={calendarRef}
            plugins={[dayGridPlugin, timeGridPlugin, interactionPlugin]}
            initialView="timeGridWeek"
            events={events}
            headerToolbar={false} // Убираем верхнюю панель навигации
            locale="ru"
            firstDay={1}
            slotMinTime="06:00:00"
            slotMaxTime="22:00:00"
            height="100%"
            eventClick={(info) => {
              alert(`${info.event.title}\n${info.event.extendedProps.startTime} - ${info.event.extendedProps.endTime}`)
            }}
            datesSet={handleDateChange}
            className={styles.fullScreenCalendar}
            navLinks={false} // Убираем кликабельность дней
            editable={false}
            selectable={false}
            dayMaxEvents={2} // Ограничиваем до 2 событий в ячейке
            eventLimit={true}
            allDaySlot={false} // Убираем секцию "Весь день"
            titleFormat={{ month: 'long', day: 'numeric' }} // Упрощаем формат заголовка (если оставим панель)
          />
        )}
      </div>
    </main>
  )
}