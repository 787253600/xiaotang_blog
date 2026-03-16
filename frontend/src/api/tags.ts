import client from './client'
import type { ApiResponse } from '@/types/api'
import type { Tag } from '@/types/tag'

export const tagsApi = {
  list() {
    return client.get<ApiResponse<Tag[]>>('/tags')
  },

  create(data: { name: string; slug: string }) {
    return client.post<ApiResponse<Tag>>('/tags', data)
  },

  update(id: number, data: Partial<{ name: string; slug: string }>) {
    return client.put<ApiResponse<Tag>>(`/tags/${id}`, data)
  },

  delete(id: number) {
    return client.delete<ApiResponse<null>>(`/tags/${id}`)
  },
}
