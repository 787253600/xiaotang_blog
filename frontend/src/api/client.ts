/**
 * axios 实例：统一拦截器配置
 * - 自动携带 Authorization Bearer Token
 * - 401 时自动尝试 refresh token，失败则跳转登录
 */
import axios, { type AxiosInstance, type AxiosRequestConfig } from 'axios'
import { useAuthStore } from '@/stores/auth'

const client: AxiosInstance = axios.create({
  baseURL: '/api/v1',
  timeout: 15000,
  withCredentials: true,  // 携带 httpOnly Cookie（refresh_token）
})

// 请求拦截：注入 access_token
client.interceptors.request.use((config) => {
  // 动态获取，避免循环引用
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// 响应拦截：处理 401，自动刷新 token
let isRefreshing = false
let pendingQueue: Array<(token: string) => void> = []

client.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config as AxiosRequestConfig & { _retry?: boolean }

    if (error.response?.status === 401 && !originalRequest._retry) {
      if (isRefreshing) {
        // 等待刷新完成后重试
        return new Promise((resolve) => {
          pendingQueue.push((token) => {
            originalRequest.headers = { ...originalRequest.headers, Authorization: `Bearer ${token}` }
            resolve(client(originalRequest))
          })
        })
      }

      originalRequest._retry = true
      isRefreshing = true

      try {
        const { data } = await axios.post('/api/v1/auth/refresh', {}, { withCredentials: true })
        const newToken = data.data.access_token
        localStorage.setItem('access_token', newToken)
        pendingQueue.forEach((cb) => cb(newToken))
        pendingQueue = []
        originalRequest.headers = { ...originalRequest.headers, Authorization: `Bearer ${newToken}` }
        return client(originalRequest)
      } catch {
        // refresh 失败，跳转登录
        localStorage.removeItem('access_token')
        pendingQueue = []
        window.location.href = '/admin/login'
      } finally {
        isRefreshing = false
      }
    }

    return Promise.reject(error)
  }
)

export default client
