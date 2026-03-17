<template>
  <div class="home-view">
    <button v-if="!isDesktop" class="sidebar-toggle" @click="sidebarOpen = !sidebarOpen">
      {{ sidebarOpen ? '收起筛选' : '展开筛选' }}
    </button>

    <div class="sidebar" v-show="sidebarOpen || isDesktop">
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
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import SearchBar from '@/components/search/SearchBar.vue'
import ArticleList from '@/components/article/ArticleList.vue'
import CategoryFilter from '@/components/article/CategoryFilter.vue'

const router = useRouter()
const searchQuery = ref('')
const selectedCategory = ref<number | undefined>(undefined)

const sidebarOpen = ref(false)
const windowWidth = ref(typeof window !== 'undefined' ? window.innerWidth : 1024)

function onResize() { windowWidth.value = window.innerWidth }
onMounted(() => window.addEventListener('resize', onResize))
onUnmounted(() => window.removeEventListener('resize', onResize))

const isDesktop = computed(() => windowWidth.value >= 1024)

function handleSearch(q: string): void {
  router.push({ path: '/search', query: { q } })
}

function selectCategory(id: number | undefined): void {
  selectedCategory.value = id
}
</script>

<style scoped>
.sidebar-toggle {
  display: block;
  width: 100%;
  margin-bottom: var(--spacing-md);
  background: var(--color-bg-secondary);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: 0.5rem 1rem;
  color: var(--color-text);
  cursor: pointer;
  text-align: left;
}

@media (min-width: 1024px) {
  .sidebar-toggle { display: none; }
}
</style>
