import client from './client'
import type { ApiResponse } from '@/types/api'
import type { Category } from '@/types/category'

export const categoriesApi = {
  list() {
    return client.get<ApiResponse<Category[]>>('/categories')
  },

  get(id: number) {
    return client.get<ApiResponse<Category>>(`/categories/${id}`)
  },

  create(data: { name: string; slug: string; description?: string }) {
    return client.post<ApiResponse<Category>>('/categories', data)
  },

  update(id: number, data: Partial<{ name: string; slug: string; description: string }>) {
    return client.put<ApiResponse<Category>>(`/categories/${id}`, data)
  },

  delete(id: number) {
    return client.delete<ApiResponse<null>>(`/categories/${id}`)
  },
}
