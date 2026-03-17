<template>
  <div class="search-view">
    <SearchBar :initial-query="query" @search="handleSearch" />
    <SkeletonLoader v-if="loading" :lines="4" />
    <div v-else-if="error" class="error">{{ error }}</div>
    <template v-else-if="results !== null">
      <p class="result-count">找到 {{ total }} 篇相关文章</p>
      <EmptyState v-if="results.length === 0" title="没有找到相关文章" description="换个关键词试试" />
      <template v-else>
        <ArticleCard v-for="article in results" :key="article.id" :article="article" />
        <AppPagination v-if="totalPages > 1" :current-page="page" :total-pages="totalPages" @change="handlePageChange" />
      </template>
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { articlesApi } from '@/api/articles'
import SearchBar from '@/components/search/SearchBar.vue'
import ArticleCard from '@/components/article/ArticleCard.vue'
import AppPagination from '@/components/common/AppPagination.vue'
import EmptyState from '@/components/common/EmptyState.vue'
import SkeletonLoader from '@/components/common/SkeletonLoader.vue'
import type { ArticleSummary } from '@/types/article'

const route = useRoute()
const router = useRouter()

const query = ref('')
const results = ref<ArticleSummary[] | null>(null)
const total = ref(0)
const totalPages = ref(1)
const page = ref(1)
const loading = ref(false)
const error = ref<string | null>(null)

async function doSearch(q: string, p: number): Promise<void> {
  if (!q.trim()) return
  loading.value = true
  error.value = null
  try {
    const res = await articlesApi.search(q, { page: p })
    results.value = res.data.items
    total.value = res.data.total
    totalPages.value = res.data.total_pages
  } catch {
    error.value = '搜索失败，请稍后重试'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  const q = route.query.q as string
  if (q) { query.value = q; doSearch(q, 1) }
})

watch(() => route.query.q, (q) => {
  if (q) { query.value = q as string; doSearch(q as string, 1) }
})

function handleSearch(q: string): void {
  router.push({ path: '/search', query: { q } })
  query.value = q
  page.value = 1
  doSearch(q, 1)
}

function handlePageChange(p: number): void {
  page.value = p
  doSearch(query.value, p)
}
</script>
