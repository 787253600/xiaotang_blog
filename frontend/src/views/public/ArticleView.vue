<template>
  <div class="article-view">
    <div v-if="loading" class="loading">加载中...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <article v-else-if="article" class="article-detail">
      <header class="article-header">
        <h1>{{ article.title }}</h1>
        <ArticleMeta :article="article" />
      </header>

      <!-- Vditor 渲染 Markdown 内容 -->
      <div id="vditor-preview" class="article-content"></div>

      <footer class="article-footer">
        <button class="like-btn" @click="handleLike">
          👍 {{ article.like_count }}
        </button>
      </footer>

      <CommentList :article-id="article.id" />
    </article>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import Vditor from 'vditor'
import 'vditor/dist/index.css'
import { useArticlesStore } from '@/stores/articles'
import { articlesApi } from '@/api/articles'
import ArticleMeta from '@/components/article/ArticleMeta.vue'
import CommentList from '@/components/article/CommentList.vue'
import type { Article } from '@/types/article'

const route = useRoute()
const store = useArticlesStore()

const article = ref<Article | null>(null)
const loading = ref(true)
const error = ref<string | null>(null)

onMounted(async () => {
  try {
    const id = Number(route.params.id)
    article.value = await store.getDetail(id)
    if (article.value) {
      // 使用 Vditor 渲染 Markdown
      Vditor.preview(
        document.getElementById('vditor-preview') as HTMLDivElement,
        article.value.content,
        { mode: 'light' }
      )
    }
  } catch {
    error.value = '文章不存在或加载失败'
  } finally {
    loading.value = false
  }
})

async function handleLike(): Promise<void> {
  if (!article.value) return
  await articlesApi.like(article.value.id)
  article.value.like_count++
}
</script>
