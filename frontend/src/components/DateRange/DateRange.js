'use client'

import styles from './DateRange.module.css'

export default function DateRange({ calendarRef, view }) {
  const formatDateRange = () => {
    if (!calendarRef.current) return ''
    const calendarApi = calendarRef.current.getApi()
    const start = calendarApi.view.activeStart
  
    const options = { day: 'numeric', month: 'long', year: 'numeric' }
    if (view === 'dayGridMonth') {
      const currentDate = new Date(calendarApi.getDate())
      return currentDate.toLocaleDateString('ru-RU', { month: 'long', year: 'numeric' })
    } else if (view === 'timeGridDay') {
      return start.toLocaleDateString('ru-RU', options)
    } else {
      const end = calendarApi.view.activeEnd
      return `${start.toLocaleDateString('ru-RU', { day: 'numeric', month: 'long' })} – 
        ${end.toLocaleDateString('ru-RU', options)}`
    }
  }

  return <div className={styles.dateRange}>{formatDateRange()}</div>
}