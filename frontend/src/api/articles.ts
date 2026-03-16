import client from './client'
import type { ApiResponse, Paginated } from '@/types/api'
import type { Article, ArticleCreate, ArticleSummary, ArticleUpdate } from '@/types/article'

export const articlesApi = {
  list(params: { page?: number; page_size?: number; category_id?: number; tag_id?: number }) {
    return client.get<Paginated<ArticleSummary>>('/articles', { params })
  },

  get(id: number) {
    return client.get<ApiResponse<Article>>(`/articles/${id}`)
  },

  search(q: string, params: { page?: number; page_size?: number } = {}) {
    return client.get<Paginated<ArticleSummary>>('/articles/search', { params: { q, ...params } })
  },

  create(data: ArticleCreate) {
    return client.post<ApiResponse<Article>>('/articles', data)
  },

  update(id: number, data: ArticleUpdate) {
    return client.put<ApiResponse<Article>>(`/articles/${id}`, data)
  },

  delete(id: number) {
    return client.delete<ApiResponse<null>>(`/articles/${id}`)
  },

  like(id: number) {
    return client.post<ApiResponse<null>>(`/articles/${id}/likes`)
  },
}
