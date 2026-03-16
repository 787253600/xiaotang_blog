import client from './client'
import type { ApiResponse } from '@/types/api'
import type { LoginRequest, TokenResponse, UserInfo } from '@/types/user'

export const authApi = {
  login(data: LoginRequest) {
    return client.post<ApiResponse<TokenResponse>>('/auth/login', data)
  },

  logout() {
    return client.post<ApiResponse<null>>('/auth/logout')
  },

  refresh() {
    return client.post<ApiResponse<TokenResponse>>('/auth/refresh')
  },

  me() {
    return client.get<ApiResponse<UserInfo>>('/auth/me')
  },
}
