'use client'
//import CalendarSwiper from './CalendarSwiper'

import { Swiper, SwiperSlide } from 'swiper/react'
import FullCalendar from '@fullcalendar/react'
import dayGridPlugin from '@fullcalendar/daygrid'
import timeGridPlugin from '@fullcalendar/timegrid'
import interactionPlugin from '@fullcalendar/interaction'
import styles from './CalendarView.module.css'
import 'swiper/css'

export default function CalendarView({ view, events, loading, currentCalendarRef, 
  prevCalendarRef, nextCalendarRef, swiperRef, onSlideChange }) {

  return (
    <Swiper
      ref={swiperRef}
      slidesPerView={1}
      initialSlide={1}
      speed={180}
      threshold={0}
      onSlideChangeTransitionEnd={onSlideChange}
      followFinger={true}
      resistanceRatio={0.85}
      simulateTouch={true}
      touchRatio={1}
      className={styles.swiper}
    >
      <SwiperSlide>
        <FullCalendar
          ref={prevCalendarRef}
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
        />
      </SwiperSlide>
      <SwiperSlide>
        {loading ? (
          <p>Загрузка...</p>
        ) : (
          <FullCalendar
            ref={currentCalendarRef}
            plugins={[dayGridPlugin, timeGridPlugin, interactionPlugin]}
            initialView={view}
            events={events}
            headerToolbar={false}
            locale="ru"
            firstDay={1}
            slotMinTime="06:00:00"
            slotMaxTime="30:00:00"
            height="100%"
            eventClick={(info) =>
              alert(`${info.event.title}\n${info.event.extendedProps.startTime} - ${info.event.extendedProps.endTime}`)
            }
            className={styles.fullScreenCalendar}
            navLinks={false}
            editable={false}
            selectable={false}
            dayMaxEvents={2}
            eventLimit={true}
            allDaySlot={false}
          />
        )}
      </SwiperSlide>
      <SwiperSlide>
        <FullCalendar
          ref={nextCalendarRef}
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
        />
      </SwiperSlide>
    </Swiper>
  )
}