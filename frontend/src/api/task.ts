import { mockTasks } from '@/mock/data'

export const getTasksApi = () => Promise.resolve([...mockTasks])

export const getTaskApi = (id: string) => Promise.resolve(mockTasks.find((t) => t.id === id) || null)

export const createTaskApi = (data: Record<string, unknown>) =>
  Promise.resolve({ id: Date.now().toString(), ...data })

export const updateTaskApi = (id: string, data: Record<string, unknown>) =>
  Promise.resolve({ id, ...data })

export const updateTaskStatusApi = (id: string, status: string) =>
  Promise.resolve({ id, status })

export const batchUpdateTaskSortApi = (updates: Array<{ id: string; status: string; sort_order: number }>) =>
  Promise.resolve({ success: true, count: updates.length })

export const addTaskCommentApi = (taskId: string, content: string) =>
  Promise.resolve({ id: Date.now().toString(), task_id: taskId, content, created_at: new Date().toISOString() })
