<template>
  <article class="article-card" :style="{ '--card-accent': accentColor }">
    <RouterLink :to="`/articles/${article.id}`" class="card-title">
      <h2>{{ article.title }}</h2>
    </RouterLink>
    <ArticleMeta :article="article" />
    <p v-if="article.excerpt" class="card-excerpt">{{ article.excerpt }}</p>
    <RouterLink :to="`/articles/${article.id}`" class="read-more">阅读全文 →</RouterLink>
  </article>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { RouterLink } from 'vue-router'
import ArticleMeta from './ArticleMeta.vue'
import type { ArticleSummary } from '@/types/article'

const props = defineProps<{ article: ArticleSummary }>()

const CATEGORY_COLORS = ['#58a6ff', '#3fb950', '#f78166', '#d2a8ff', '#ffa657']
const accentColor = computed(() =>
  CATEGORY_COLORS[(props.article.category?.id ?? 0) % CATEGORY_COLORS.length]
)
</script>
