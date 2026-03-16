/**
 * 文章列表逻辑复用
 */
import { ref, watch } from 'vue'
import { useArticlesStore } from '@/stores/articles'
import type { ArticleSummary } from '@/types/article'
import type { Paginated } from '@/types/api'

export function useArticles(params: {
  categoryId?: number
  tagId?: number
  pageSize?: number
}) {
  const store = useArticlesStore()
  const page = ref(1)
  const result = ref<Paginated<ArticleSummary> | null>(null)
  const error = ref<string | null>(null)

  async function load(): Promise<void> {
    error.value = null
    try {
      result.value = await store.getList({
        page: page.value,
        page_size: params.pageSize ?? 10,
        category_id: params.categoryId,
        tag_id: params.tagId,
      })
    } catch (e) {
      error.value = '加载失败，请稍后重试'
    }
  }

  watch(page, load, { immediate: true })

  return { page, result, loading: store.loading, error, load }
}
