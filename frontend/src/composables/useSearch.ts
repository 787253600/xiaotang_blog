/**
 * 搜索防抖逻辑（300ms）
 */
import { ref } from 'vue'
import { articlesApi } from '@/api/articles'
import type { ArticleSummary } from '@/types/article'
import type { Paginated } from '@/types/api'

export function useSearch() {
  const query = ref('')
  const results = ref<Paginated<ArticleSummary> | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)
  let timer: ReturnType<typeof setTimeout> | null = null

  function search(q: string, page = 1): void {
    query.value = q
    if (timer) clearTimeout(timer)

    if (!q.trim()) {
      results.value = null
      return
    }

    timer = setTimeout(async () => {
      loading.value = true
      error.value = null
      try {
        const res = await articlesApi.search(q, { page })
        results.value = res.data
      } catch {
        error.value = '搜索失败，请稍后重试'
      } finally {
        loading.value = false
      }
    }, 300)
  }

  function clear(): void {
    query.value = ''
    results.value = null
    error.value = null
  }

  return { query, results, loading, error, search, clear }
}
