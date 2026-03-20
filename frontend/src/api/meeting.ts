import { mockMeetings } from '@/mock/data'

export const getMeetingsApi = () => Promise.resolve([...mockMeetings])

export const getMeetingApi = (id: string) => Promise.resolve(mockMeetings.find((m) => m.id === id) || null)

export const createMeetingApi = (data: Record<string, unknown>) =>
  Promise.resolve({ id: Date.now().toString(), ...data })

export const updateMeetingApi = (id: string, data: Record<string, unknown>) =>
  Promise.resolve({ id, ...data })

export const toggleDecisionApi = (meetingId: string, decisionId: string, is_resolved: boolean) =>
  Promise.resolve({ meetingId, decisionId, is_resolved })
