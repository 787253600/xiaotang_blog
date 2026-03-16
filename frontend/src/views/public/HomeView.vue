<template>
  <div class="home-view">
    <div class="sidebar">
      <SearchBar @search="handleSearch" />
      <CategoryFilter :selected="selectedCategory" @select="selectCategory" />
    </div>

    <div class="content">
      <ArticleList
        v-if="!searchQuery"
        :category-id="selectedCategory"
        :page-size="10"
      />
      <div v-else>
        <h2 class="search-title">搜索："{{ searchQuery }}"</h2>
        <ArticleList :search-query="searchQuery" :page-size="10" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import SearchBar from '@/components/search/SearchBar.vue'
import ArticleList from '@/components/article/ArticleList.vue'
import CategoryFilter from '@/components/article/CategoryFilter.vue'

const router = useRouter()
const searchQuery = ref('')
const selectedCategory = ref<number | undefined>(undefined)

function handleSearch(q: string): void {
  router.push({ path: '/search', query: { q } })
}

function selectCategory(id: number | undefined): void {
  selectedCategory.value = id
}
</script>
