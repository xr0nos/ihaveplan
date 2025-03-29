import { useState, useEffect } from 'react'

export default function useTasks(date) {
  const [tasks, setTasks] = useState([])
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    const fetchTasks = async () => {
      setLoading(true)
      try {
        // TODO: Сделать запрос к API
        setTasks([
          {
            id: 1,
            title: 'Утренняя зарядка',
            startTime: '08:00',
            endTime: '08:30',
            priority: 'low',
            completed: false,
            date: date.toISOString().split('T')[0],
          },
          {
            id: 2,
            title: 'Встреча',
            startTime: '10:30',
            endTime: '11:30',
            priority: 'high',
            completed: false,
            date: date.toISOString().split('T')[0],
          }
        ])
      } catch (error) {
        console.error('Error fetching tasks:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchTasks()
  }, [date])

  return { tasks, loading }
}