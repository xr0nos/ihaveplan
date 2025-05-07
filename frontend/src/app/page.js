'use client'

import { useState, useEffect, useRef } from 'react'
import FullCalendar from '@fullcalendar/react'
import dayGridPlugin from '@fullcalendar/daygrid'
import timeGridPlugin from '@fullcalendar/timegrid'
import interactionPlugin from '@fullcalendar/interaction'
import { Swiper, SwiperSlide } from 'swiper/react'
import 'swiper/css'
import styles from './page.module.css'

import TelegramWebApp from '../components/TelegramWebApp/TelegramWebApp'
import DateRange from '../components/DateRange/DateRange'
import BottomBar from '../components/BottomBar/BottomBar'
import TaskModal from '../components/TaskModal/TaskModal'

export default function Home() {
  const [date, setDate] = useState(new Date());
  const [tasks, setTasks] = useState([]);
  const [view, setView] = useState('timeGridDay');
  const [userId, setUserId] = useState(null);
  const [selectedTask, setSelectedTask] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const currentCalendarRef = useRef(null);
  const prevCalendarRef = useRef(null);
  const nextCalendarRef = useRef(null);
  const swiperRef = useRef(null);

  // Получение задач из API
  useEffect(() => {
    if (!userId) return;
    fetch(`http://localhost:8000/users_tg/${userId}/tasks/`)
      .then((response) => {
        if (!response.ok) throw new Error('Network error');
        return response.json();
      })
      .then((data) => {
        const formattedTasks = data.map((task) => ({
          id: task.id,
          title: task.title,
          startTime: task.start_time,
          endTime: task.end_time,
          priority: task.priority,
          completed: task.completed,
          date: task.date,
        }));
        setTasks(formattedTasks);
      })
      .catch((err) => console.error('Fetch error:', err));
  }, [userId]);

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

  const handleTaskClick = (info) => {
    console.log('Task clicked:', info.event.id, tasks);
    const task = tasks.find(t => t.id === +info.event.id);
    if (task) {
      setSelectedTask(task);
      setIsModalOpen(true);
    }
  };

  const handleToggleComplete = async () => {
    if (!selectedTask) return;

    try {
      const response = await fetch(`http://localhost:8000/tasks/${selectedTask.id}/`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          completed: !selectedTask.completed
        }),
      });

      if (!response.ok) throw new Error('Network error');

      // Обновляем состояние задачи в списке
      const updatedTasks = tasks.map(task => 
        task.id === selectedTask.id 
          ? { ...task, completed: !task.completed }
          : task
      );
      setTasks(updatedTasks);
      
      // Обновляем состояние выбранной задачи
      const updatedTask = updatedTasks.find(task => task.id === selectedTask.id);
      setSelectedTask(updatedTask);
    } catch (err) {
      console.error('Update error:', err);
    }
  };

  const events = tasks.map((task) => ({
    id: task.id,
    title: task.title,
    start: `${task.date}T${task.startTime}:00`,
    end: `${task.date}T${task.endTime}:00`,
    className: `completed-${task.completed}`,
    extendedProps: {
      priority: task.priority,
      startTime: task.startTime,
      endTime: task.endTime,
      completed: task.completed,
    },
  }));

  return (
    <main className={styles.main}>

      <TelegramWebApp onUserIdDetected={setUserId} />
      <DateRange calendarRef={currentCalendarRef} view={view} date={date} />

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
            eventClick={handleTaskClick}
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

      <BottomBar
        view={view}
        onViewChange={handleViewChange}
        onTodayClick={handleTodayClick}
      />

      {selectedTask && (
        <TaskModal
          task={selectedTask}
          isOpen={isModalOpen}
          onClose={() => setIsModalOpen(false)}
          onToggleComplete={handleToggleComplete}
        />
      )}
    </main>
  );
}