'use client'

import { useState, useEffect, useRef } from 'react'
import styles from './page.module.css'

import TelegramWebApp from '../components/TelegramWebApp/TelegramWebApp'
import DateRange from '../components/DateRange/DateRange'
import BottomBar from '../components/BottomBar/BottomBar'
import TaskModal from '../components/TaskModal/TaskModal'
import CalendarSwiper from '../components/CalendarSwiper/CalendarSwiper'
import { fetchUserTasks, updateTaskCompletion } from '../tools/tasksApi'
import { useWebSocket } from '../tools/useWebSocket'

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

  // Загрузка сохраненного вида при монтировании компонента
  useEffect(() => {
    const savedView = localStorage.getItem('calendarView');
    if (savedView) {
      handleViewChange(savedView);
    }
  }, []);

  // Получение задач из API
  useEffect(() => {
    if (!userId) return;
    fetchUserTasks(userId)
      .then((formattedTasks) => {
        setTasks(formattedTasks);
      })
      .catch((err) => console.error('Fetch error:', err));
  }, [userId]);

  // WebSocket для обновления задач в реальном времени
  useWebSocket(userId, (newTasks) => {
    setTasks(newTasks);
  });

  const handleViewChange = (newView) => {
    setView(newView);
    localStorage.setItem('calendarView', newView);
    if (currentCalendarRef.current) currentCalendarRef.current.getApi().changeView(newView);
    if (prevCalendarRef.current) prevCalendarRef.current.getApi().changeView(newView);
    if (nextCalendarRef.current) nextCalendarRef.current.getApi().changeView(newView);
    updateCalendars(newView);
  };

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
      currentApi.gotoDate(currentDate);
    }
  };

  const handleTodayClick = () => {
    if (currentCalendarRef.current) {
      currentCalendarRef.current.getApi().today();
      setDate(new Date());
      updateCalendars(view);
      swiperRef.current.swiper.slideTo(1);
    }
  };

  const handleSlideChange = (swiper) => {
    const direction = swiper.activeIndex - 1;
    if (direction !== 0 && currentCalendarRef.current) {
      const api = currentCalendarRef.current.getApi();
      if (direction > 0) api.next();
      else api.prev();
      setDate(api.getDate());
      updateCalendars(view);
      swiper.slideTo(1, 0);
    }
  };

  const handleTaskClick = (info) => {
    const task = tasks.find(t => t.id === +info.event.id);
    if (task) {
      setSelectedTask(task);
      setIsModalOpen(true);
    }
  };

  const handleToggleComplete = async () => {
    if (!selectedTask) return;

    try {
      await updateTaskCompletion(selectedTask.id, !selectedTask.completed);
      
      const updatedTasks = tasks.map(task => 
        task.id === selectedTask.id 
          ? { ...task, completed: !task.completed }
          : task
      );
      setTasks(updatedTasks);
      
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

      <CalendarSwiper
        swiperRef={swiperRef}
        currentCalendarRef={currentCalendarRef}
        prevCalendarRef={prevCalendarRef}
        nextCalendarRef={nextCalendarRef}
        view={view}
        events={events}
        onSlideChange={handleSlideChange}
        onTaskClick={handleTaskClick}
      />

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