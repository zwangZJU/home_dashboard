import { mockRequirements } from '@/mock/data'

export const getRequirementsApi = (params?: Record<string, unknown>) => {
  // TODO: replace with real API call
  // return request.get('/requirements', { params })
  let list = [...mockRequirements]
  if (params?.status && params.status !== 'all') {
    list = list.filter((r) => r.status === params.status)
  }
  if (params?.search) {
    const s = String(params.search).toLowerCase()
    list = list.filter((r) => r.title.toLowerCase().includes(s))
  }
  return Promise.resolve(list)
}

export const getRequirementApi = (id: string) => {
  return Promise.resolve(mockRequirements.find((r) => r.id === id) || null)
}

export const createRequirementApi = (data: Record<string, unknown>) => {
  return Promise.resolve({ id: Date.now().toString(), ...data, created_at: new Date().toISOString() })
}

export const updateRequirementApi = (id: string, data: Record<string, unknown>) => {
  return Promise.resolve({ id, ...data })
}
