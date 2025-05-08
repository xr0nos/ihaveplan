import React from 'react';
import { Swiper, SwiperSlide } from 'swiper/react';
import 'swiper/css';
import styles from './CalendarSwiper.module.css';
import CalendarView from '../CalendarView/CalendarView';

const CalendarSwiper = ({
  swiperRef,
  currentCalendarRef,
  prevCalendarRef,
  nextCalendarRef,
  view,
  events,
  onSlideChange,
  onTaskClick
}) => {
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
        <CalendarView
          calendarRef={prevCalendarRef}
          view={view}
          events={events}
        />
      </SwiperSlide>
      <SwiperSlide>
        <CalendarView
          calendarRef={currentCalendarRef}
          view={view}
          events={events}
          onEventClick={onTaskClick}
          isCurrent={true}
        />
      </SwiperSlide>
      <SwiperSlide>
        <CalendarView
          calendarRef={nextCalendarRef}
          view={view}
          events={events}
        />
      </SwiperSlide>
    </Swiper>
  );
};

export default CalendarSwiper; 