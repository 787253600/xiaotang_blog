<template>
  <article class="article-card">
    <RouterLink :to="`/articles/${article.id}`" class="card-title">
      <h2>{{ article.title }}</h2>
    </RouterLink>
    <ArticleMeta :article="article" />
    <p v-if="article.excerpt" class="card-excerpt">{{ article.excerpt }}</p>
    <RouterLink :to="`/articles/${article.id}`" class="read-more">阅读全文 →</RouterLink>
  </article>
</template>

<script setup lang="ts">
import { RouterLink } from 'vue-router'
import ArticleMeta from './ArticleMeta.vue'
import type { ArticleSummary } from '@/types/article'

defineProps<{ article: ArticleSummary }>()
</script>
