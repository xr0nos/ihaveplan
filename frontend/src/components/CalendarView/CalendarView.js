import React from 'react';
import FullCalendar from '@fullcalendar/react';
import dayGridPlugin from '@fullcalendar/daygrid';
import timeGridPlugin from '@fullcalendar/timegrid';
import interactionPlugin from '@fullcalendar/interaction';
import styles from './CalendarView.module.css';

const CalendarView = ({ 
  calendarRef, 
  view, 
  events, 
  onEventClick,
  isCurrent = false 
}) => {
  return (
    <FullCalendar
      ref={calendarRef}
      plugins={[dayGridPlugin, timeGridPlugin, interactionPlugin]}
      initialView={view}
      events={events}
      headerToolbar={false}
      locale="ru"
      firstDay={1}
      slotMinTime="06:00:00"
      slotMaxTime="30:00:00"
      height="100%"
      eventClick={isCurrent ? onEventClick : undefined}
      className={styles.fullScreenCalendar}
      navLinks={false}
      editable={false}
      selectable={false}
      dayMaxEvents={2}
      eventLimit={true}
      allDaySlot={false}
    />
  );
};

export default CalendarView; 