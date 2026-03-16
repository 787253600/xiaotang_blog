<template>
  <div class="search-view">
    <SearchBar :initial-query="query" @search="handleSearch" />

    <div v-if="loading" class="loading">搜索中...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else-if="results">
      <p class="result-count">找到 {{ results.total }} 篇相关文章</p>
      <ArticleList
        :articles="results.items"
        :total="results.total"
        :total-pages="results.total_pages"
        :current-page="page"
        @page-change="handlePageChange"
      />
    </div>
    <div v-else-if="query" class="no-result">没有找到相关文章</div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useSearch } from '@/composables/useSearch'
import SearchBar from '@/components/search/SearchBar.vue'
import ArticleList from '@/components/article/ArticleList.vue'

const route = useRoute()
const router = useRouter()
const { query, results, loading, error, search } = useSearch()
const page = ref(1)

onMounted(() => {
  const q = route.query.q as string
  if (q) search(q)
})

watch(() => route.query.q, (q) => {
  if (q) search(q as string)
})

function handleSearch(q: string): void {
  router.push({ path: '/search', query: { q } })
  page.value = 1
  search(q)
}

function handlePageChange(p: number): void {
  page.value = p
  search(query.value, p)
}
</script>
