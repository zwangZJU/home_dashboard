import request from './request'
import { mockUsers } from '@/mock/data'

export const loginApi = (data: { username: string; password: string }) =>
  request.post('/auth/login', data)

export const registerApi = (data: { username: string; password: string; email: string }) =>
  request.post('/auth/register', data)

export const getUsersApi = () => request.get('/users')

// Mock fallback
export const mockLogin = (username: string) => ({
  token: 'mock-jwt-token-' + username,
  user: mockUsers.find((u) => u.username === username) || mockUsers[0],
})
