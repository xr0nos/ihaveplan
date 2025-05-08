'use client'

import { useState, useEffect } from 'react'
import styles from './DateRange.module.css'

export default function DateRange({ calendarRef, view, date }) {
  const [dateRange, setDateRange] = useState('')

  const updateDateRange = () => {
    if (!calendarRef.current) return
    const calendarApi = calendarRef.current.getApi()
    const start = calendarApi.view.activeStart

    if (view === 'dayGridMonth') {
      const currentDate = new Date(calendarApi.getDate())
      setDateRange(currentDate.toLocaleDateString('ru-RU', { month: 'long', year: 'numeric' }))
    } else if (view === 'timeGridDay') {
      setDateRange(start.toLocaleDateString('ru-RU', { day: 'numeric', month: 'long' }))
    } else {
      const end = calendarApi.view.activeEnd
      setDateRange(
        `${start.toLocaleDateString('ru-RU', { day: 'numeric', month: 'long' })} – ${end.toLocaleDateString('ru-RU', { day: 'numeric', month: 'long' })}`
      )
    }
  }

  useEffect(() => {
    // Вызываем обновление при изменении view или date
    updateDateRange()

    // Подписываемся на событие datesSet
    const calendarApi = calendarRef.current?.getApi()
    if (calendarApi) {
      calendarApi.on('datesSet', updateDateRange)
      return () => calendarApi.off('datesSet', updateDateRange)
    }
  }, [calendarRef, view, date])

  return <div className={styles.dateRange}>{dateRange}</div>
}