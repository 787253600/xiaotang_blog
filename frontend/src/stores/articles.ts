/**
 * 文章列表 Store
 * - 前端内存缓存（Map，TTL=5min）
 * - 避免短时间内重复请求
 */
import { defineStore } from 'pinia'
import { ref } from 'vue'
import { articlesApi } from '@/api/articles'
import type { ArticleSummary, Article } from '@/types/article'
import type { Paginated } from '@/types/api'

const CACHE_TTL = 5 * 60 * 1000  // 5 分钟

interface CacheEntry<T> {
  data: T
  expiredAt: number
}

export const useArticlesStore = defineStore('articles', () => {
  // 详情缓存：key = article id
  const detailCache = new Map<number, CacheEntry<Article>>()
  const loading = ref(false)

  function isExpired(entry: CacheEntry<unknown>): boolean {
    return Date.now() > entry.expiredAt
  }

  async function getDetail(id: number): Promise<Article | null> {
    const cached = detailCache.get(id)
    if (cached && !isExpired(cached)) {
      return cached.data
    }

    loading.value = true
    try {
      const res = await articlesApi.get(id)
      const article = res.data.data
      if (article) {
        detailCache.set(id, { data: article, expiredAt: Date.now() + CACHE_TTL })
      }
      return article ?? null
    } finally {
      loading.value = false
    }
  }

  async function getList(params: {
    page?: number
    page_size?: number
    category_id?: number
    tag_id?: number
  }): Promise<Paginated<ArticleSummary>> {
    loading.value = true
    try {
      const res = await articlesApi.list(params)
      return res.data
    } finally {
      loading.value = false
    }
  }

  function invalidate(id: number): void {
    detailCache.delete(id)
  }

  return { loading, getDetail, getList, invalidate }
})
