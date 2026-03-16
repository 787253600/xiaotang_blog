/**
 * 认证状态 Store
 * - 管理 access_token（localStorage）
 * - 管理当前用户信息
 */
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authApi } from '@/api/auth'
import type { UserInfo, LoginRequest } from '@/types/user'

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(localStorage.getItem('access_token'))
  const user = ref<UserInfo | null>(null)

  const isLoggedIn = computed(() => !!token.value)

  async function login(data: LoginRequest): Promise<void> {
    const res = await authApi.login(data)
    const accessToken = res.data.data?.access_token
    if (accessToken) {
      token.value = accessToken
      localStorage.setItem('access_token', accessToken)
      await fetchMe()
    }
  }

  async function logout(): Promise<void> {
    try {
      await authApi.logout()
    } finally {
      token.value = null
      user.value = null
      localStorage.removeItem('access_token')
    }
  }

  async function fetchMe(): Promise<void> {
    try {
      const res = await authApi.me()
      user.value = res.data.data ?? null
    } catch {
      user.value = null
    }
  }

  // 应用启动时恢复登录状态
  async function init(): Promise<void> {
    if (token.value) {
      await fetchMe()
    }
  }

  return { token, user, isLoggedIn, login, logout, fetchMe, init }
})
