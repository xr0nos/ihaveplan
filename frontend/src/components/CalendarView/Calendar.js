'use client'

import { forwardRef } from 'react'
import FullCalendar from '@fullcalendar/react'
import dayGridPlugin from '@fullcalendar/daygrid'
import timeGridPlugin from '@fullcalendar/timegrid'
import interactionPlugin from '@fullcalendar/interaction'
import styles from './CalendarView.module.css'

const Calendar = forwardRef(({ view, events, interactive = false }, ref) => (
  <FullCalendar
    ref={ref}
    plugins={[dayGridPlugin, timeGridPlugin, interactionPlugin]}
    initialView={view}
    events={events}
    headerToolbar={false}
    locale="ru"
    firstDay={1}
    slotMinTime="06:00:00"
    slotMaxTime="30:00:00"
    height="100%"
    className={styles.fullScreenCalendar}
    navLinks={false}
    editable={false}
    selectable={false}
    dayMaxEvents={2}
    eventLimit={true}
    allDaySlot={false}
    eventClick={interactive ? (info) => 
      alert(`${info.event.title}\n${info.event.extendedProps.startTime} - ${info.event.extendedProps.endTime}`)
      : undefined
    }
  />
))

export default Calendar