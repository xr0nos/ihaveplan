'use client'

import { useState, useEffect, useRef } from 'react'
import FullCalendar from '@fullcalendar/react'
import dayGridPlugin from '@fullcalendar/daygrid'
import timeGridPlugin from '@fullcalendar/timegrid'
import interactionPlugin from '@fullcalendar/interaction'
import { Swiper, SwiperSlide } from 'swiper/react'
import 'swiper/css'
import styles from './page.module.css'
import axios from 'axios'

export default function Home() {
  const [date, setDate] = useState(new Date());
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(false);
  const [view, setView] = useState('timeGridDay');
  const currentCalendarRef = useRef(null);
  const prevCalendarRef = useRef(null);
  const nextCalendarRef = useRef(null);
  const swiperRef = useRef(null);

  // Настройка Telegram Web App
  useEffect(() => {
    const script = document.createElement('script');
    script.src = 'https://telegram.org/js/telegram-web-app.js';
    script.async = true;
    script.onload = () => {
      if (window.Telegram?.WebApp) {
        const webApp = window.Telegram.WebApp;
        webApp.ready();
        webApp.expand();
        webApp.setHeaderColor('#f5f7fa');
        webApp.setBackgroundColor('#f5f7fa');
      } else {
        alert("error");
      }
    };
    document.head.appendChild(script);
  }, []);

  // Получение задач из API
  useEffect(() => {
    const fetchTasks = async () => {
      setLoading(true);
      try {
        setTasks([
          {
            id: 1,
            title: 'Утренняя зарядка',
            startTime: '08:00',
            endTime: '08:30',
            priority: 'low',
            completed: false,
            date: new Date().toISOString().split('T')[0],
          },
          {
            id: 2,
            title: 'Встреча',
            startTime: '10:30',
            endTime: '11:30',
            priority: 'high',
            completed: false,
            date: new Date().toISOString().split('T')[0],
          }
        ]);
      } catch (error) {
        console.error('Error fetching tasks:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchTasks();
    handleViewChange(view);
  }, [date]);

  const handleViewChange = (newView) => {
    setView(newView);
    if (currentCalendarRef.current) currentCalendarRef.current.getApi().changeView(newView);
    if (prevCalendarRef.current) prevCalendarRef.current.getApi().changeView(newView);
    if (nextCalendarRef.current) nextCalendarRef.current.getApi().changeView(newView);
    updateCalendars(newView);
  };

  // Принимаем вид как параметр, чтобы использовать актуальное значение
  const updateCalendars = (currentView) => {
    if (currentCalendarRef.current && prevCalendarRef.current && nextCalendarRef.current) {
      const currentApi = currentCalendarRef.current.getApi();
      const prevApi = prevCalendarRef.current.getApi();
      const nextApi = nextCalendarRef.current.getApi();
      const currentDate = new Date(currentApi.getDate());

      let prevDate, nextDate;
      switch (currentView) {
        case 'dayGridMonth':
          prevDate = new Date(currentDate.getFullYear(), currentDate.getMonth() - 1, 1);
          nextDate = new Date(currentDate.getFullYear(), currentDate.getMonth() + 1, 1);
          break;
        case 'timeGridWeek':
          prevDate = new Date(currentDate.getTime() - 7 * 24 * 60 * 60 * 1000);
          nextDate = new Date(currentDate.getTime() + 7 * 24 * 60 * 60 * 1000);
          break;
        case 'timeGridDay':
          prevDate = new Date(currentDate.getTime() - 24 * 60 * 60 * 1000);
          nextDate = new Date(currentDate.getTime() + 24 * 60 * 60 * 1000);
          break;
        default:
          return;
      }

      prevApi.gotoDate(prevDate);
      nextApi.gotoDate(nextDate);
      currentApi.gotoDate(currentDate); // Убеждаемся, что текущий календарь остаётся на месте
    }
  };

  const handleTodayClick = () => {
    if (currentCalendarRef.current) {
      currentCalendarRef.current.getApi().today();
      setDate(new Date());
      updateCalendars(view);
      swiperRef.current.swiper.slideTo(1); // Возвращаем в центр только при "Сегодня"
    }
  };

  const handleSlideChange = (swiper) => {
    const direction = swiper.activeIndex - 1; // -1 (prev), 0 (current), 1 (next)
    if (direction !== 0 && currentCalendarRef.current) {
      const api = currentCalendarRef.current.getApi();
      if (direction > 0) api.next();
      else api.prev();
      setDate(api.getDate());
      updateCalendars(view);
      swiper.slideTo(1, 0); // Возвращаем в центр без анимации
    }
  };

  const events = tasks.map((task) => ({
    id: task.id,
    title: task.title,
    start: `${task.date}T${task.startTime}:00`,
    end: `${task.date}T${task.endTime}:00`,
    className: styles[task.priority],
    extendedProps: {
      priority: task.priority,
      startTime: task.startTime,
      endTime: task.endTime,
      completed: task.completed,
    },
  }));

  const formatDateRange = () => {
    if (!currentCalendarRef.current) return '';
    const calendarApi = currentCalendarRef.current.getApi();
    const start = calendarApi.view.activeStart;
  
    const options = { day: 'numeric', month: 'long', year: 'numeric' };
    if (view === 'dayGridMonth') {
      const currentDate = new Date(calendarApi.getDate());
      return currentDate.toLocaleDateString('ru-RU', { month: 'long', year: 'numeric' });
    } else if (view === 'timeGridDay') {
      return start.toLocaleDateString('ru-RU', options);
    } else {
      const end = calendarApi.view.activeEnd;
      return `${start.toLocaleDateString('ru-RU', { day: 'numeric', month: 'long' })} – 
        ${end.toLocaleDateString('ru-RU', options)}`;
    }
  };

  return (
    <main className={styles.main}>
      <div className={styles.dateRange}>{formatDateRange()}</div>
      <Swiper
        ref={swiperRef}
        slidesPerView={1}
        initialSlide={1}
        speed={180}
        threshold={0}
        onSlideChangeTransitionEnd={handleSlideChange}
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
      <div className={styles.bottomBar}>
        <div className={styles.viewToggle}>
          <button
            onClick={() => handleViewChange('dayGridMonth')}
            className={`${styles.toggleButton} ${view === 'dayGridMonth' ? styles.active : ''}`}
          >
            М
          </button>
          <button
            onClick={() => handleViewChange('timeGridWeek')}
            className={`${styles.toggleButton} ${view === 'timeGridWeek' ? styles.active : ''}`}
          >
            Н
          </button>
          <button
            onClick={() => handleViewChange('timeGridDay')}
            className={`${styles.toggleButton} ${view === 'timeGridDay' ? styles.active : ''}`}
          >
            Д
          </button>
        </div>
        <button onClick={handleTodayClick} className={styles.todayButton}>
          Сегодня
        </button>
      </div>
    </main>
  );
}