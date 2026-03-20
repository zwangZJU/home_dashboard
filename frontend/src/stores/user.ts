import { defineStore } from 'pinia'
import { ref } from 'vue'
import { mockLogin } from '@/api/auth'

export const useUserStore = defineStore('user', () => {
  const token = ref(localStorage.getItem('token') || '')
  const userInfo = ref<any>(null)

  const login = async (username: string, _password: string) => {
    // Mock login
    const res = mockLogin(username)
    token.value = res.token
    userInfo.value = res.user
    localStorage.setItem('token', res.token)
    localStorage.setItem('user', JSON.stringify(res.user))
    return res
  }

  const logout = () => {
    token.value = ''
    userInfo.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('user')
  }

  // Restore from localStorage
  const savedUser = localStorage.getItem('user')
  if (savedUser) {
    try { userInfo.value = JSON.parse(savedUser) } catch { /* ignore */ }
  }

  return { token, userInfo, login, logout }
})
