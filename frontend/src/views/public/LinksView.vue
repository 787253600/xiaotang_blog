<template>
  <div class="links-view">
    <h1 class="page-title">友情链接</h1>

    <div v-if="loading" class="hint">加载中...</div>
    <div v-else-if="links.length === 0" class="hint">暂无链接</div>

    <div v-else class="links-grid">
      <a
        v-for="link in links"
        :key="link.id"
        :href="link.url"
        target="_blank"
        rel="noopener noreferrer"
        class="link-card"
      >
        <div class="link-name">{{ link.name }}</div>
        <div v-if="link.description" class="link-desc">{{ link.description }}</div>
      </a>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { linksApi } from '@/api/links'
import type { Link } from '@/types/link'

const links = ref<Link[]>([])
const loading = ref(true)

onMounted(async () => {
  const res = await linksApi.list()
  links.value = res.data
  loading.value = false
})
</script>

<style scoped>
.links-view {
  max-width: 800px;
  margin: 0 auto;
  padding: var(--spacing-lg);
}

.page-title {
  font-size: var(--font-size-2xl);
  margin-bottom: var(--spacing-lg);
}

.hint {
  color: var(--color-text-muted);
}

.links-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: var(--spacing-md);
}

.link-card {
  display: block;
  padding: var(--spacing-md);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  text-decoration: none;
  color: var(--color-text);
  transition: border-color 0.15s;
}

.link-card:hover {
  border-color: var(--color-primary);
}

.link-name {
  font-weight: 600;
  margin-bottom: 0.25rem;
}

.link-desc {
  font-size: var(--font-size-sm);
  color: var(--color-text-muted);
}
</style>
