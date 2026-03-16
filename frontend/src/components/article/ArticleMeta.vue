<template>
  <div class="article-meta">
    <time :datetime="article.created_at">
      {{ formatDate(article.created_at) }}
    </time>
    <span v-if="article.category" class="meta-category">
      <RouterLink :to="`/?category=${article.category.id}`">
        {{ article.category.name }}
      </RouterLink>
    </span>
    <span class="meta-tags">
      <RouterLink
        v-for="tag in article.tags"
        :key="tag.id"
        :to="`/tags/${tag.id}?name=${tag.name}`"
        class="tag"
      >
        #{{ tag.name }}
      </RouterLink>
    </span>
    <span class="meta-views">👁 {{ article.view_count }}</span>
  </div>
</template>

<script setup lang="ts">
import { RouterLink } from 'vue-router'
import type { ArticleSummary } from '@/types/article'

defineProps<{ article: ArticleSummary }>()

function formatDate(iso: string): string {
  return new Date(iso).toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  })
}
</script>
