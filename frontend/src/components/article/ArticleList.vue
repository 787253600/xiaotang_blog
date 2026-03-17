<template>
  <div class="article-list">
    <SkeletonLoader v-if="loading" :lines="4" />
    <div v-else-if="error" class="error">{{ error }}</div>
    <template v-else-if="data">
      <EmptyState v-if="data.items.length === 0" title="暂无文章" description="还没有任何文章，敬请期待" />
      <ArticleCard
        v-for="article in data.items"
        :key="article.id"
        :article="article"
      />
      <AppPagination
        v-if="data.total_pages > 1"
        :current-page="page"
        :total-pages="data.total_pages"
        @change="page = $event"
      />
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { useArticlesStore } from '@/stores/articles'
import { articlesApi } from '@/api/articles'
import ArticleCard from './ArticleCard.vue'
import AppPagination from '@/components/common/AppPagination.vue'
import SkeletonLoader from '@/components/common/SkeletonLoader.vue'
import EmptyState from '@/components/common/EmptyState.vue'
import type { Paginated } from '@/types/api'
import type { ArticleSummary } from '@/types/article'

const props = defineProps<{
  categoryId?: number
  tagId?: number
  pageSize?: number
  searchQuery?: string
}>()

const store = useArticlesStore()
const page = ref(1)
const data = ref<Paginated<ArticleSummary> | null>(null)
const loading = ref(false)
const error = ref<string | null>(null)

async function load(): Promise<void> {
  loading.value = true
  error.value = null
  try {
    if (props.searchQuery) {
      const res = await articlesApi.search(props.searchQuery, { page: page.value, page_size: props.pageSize })
      data.value = res.data
    } else {
      data.value = await store.getList({
        page: page.value,
        page_size: props.pageSize ?? 10,
        category_id: props.categoryId,
        tag_id: props.tagId,
      })
    }
  } catch {
    error.value = '加载失败，请稍后重试'
  } finally {
    loading.value = false
  }
}

watch([page, () => props.categoryId, () => props.tagId, () => props.searchQuery], () => {
  page.value = 1
  load()
}, { immediate: true })
</script>
