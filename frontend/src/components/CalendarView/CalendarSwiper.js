'use client'

import { Swiper, SwiperSlide } from 'swiper/react'
import Calendar from './Calendar'
import 'swiper/css'
import styles from './CalendarView.module.css'

export default function CalendarSwiper({ view, events, loading, currentCalendarRef, prevCalendarRef, nextCalendarRef, onSlideChange }) {
  return (
    <Swiper
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
        <Calendar ref={prevCalendarRef} view={view} events={events} />
      </SwiperSlide>

      <SwiperSlide>
        {loading ? <p>Загрузка...</p> : <Calendar ref={currentCalendarRef} view={view} events={events} interactive />}
      </SwiperSlide>
      
      <SwiperSlide>
        <Calendar ref={nextCalendarRef} view={view} events={events} />
      </SwiperSlide>
    </Swiper>
  )
}