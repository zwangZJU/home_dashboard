import { mockDashboardStats, mockTrendData } from '@/mock/data'
import { mockTasks, mockRequirements, mockUsers } from '@/mock/data'

export const getDashboardStatsApi = () => Promise.resolve(mockDashboardStats)

export const getTrendDataApi = () => Promise.resolve(mockTrendData)

export const getTimelineDataApi = () => Promise.resolve(mockRequirements.filter((r) => r.expected_date).map((r) => ({
  id: r.id, name: r.req_no + ' ' + r.title,
  start: r.created_at?.split(' ')[0] || '2026-03-15',
  end: r.expected_date || '2026-04-15',
  status: r.status, progress: Math.round((r.children.filter((c) => c.status === 'done').length / Math.max(r.children.length, 1)) * 100),
})))

export const getBurndownDataApi = () => {
  const total = mockTasks.length
  const done = mockTasks.filter((t) => t.status === 'done').length
  const remaining = total - done
  const days = ['03-15', '03-16', '03-17', '03-18', '03-19', '03-20']
  const ideal = days.map((_, i) => total - (total / (days.length - 1)) * i)
  const actual = [total, total - 1, total - 2, total - 3, total - 3, remaining]
  return Promise.resolve({ days, ideal, actual })
}

export const getMemberWorkloadApi = () => Promise.resolve(
  mockUsers.filter((u) => u.role === 'member').map((u) => {
    const tasks = mockTasks.filter((t) => t.assignee_id === u.id)
    return { user: u, total: tasks.length, done: tasks.filter((t) => t.status === 'done').length, inProgress: tasks.filter((t) => t.status === 'in_progress').length }
  })
)
