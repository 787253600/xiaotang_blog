/** 统一 API 响应格式 */
export interface ApiResponse<T> {
  code: number
  message: string
  data: T | null
}

/** 分页响应格式 */
export interface Paginated<T> {
  items: T[]
  total: number
  page: number
  page_size: number
  total_pages: number
}
