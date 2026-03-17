<template>
  <div class="article-view">
    <SkeletonLoader v-if="loading" :lines="6" />
    <div v-else-if="error" class="error">{{ error }}</div>
    <article v-else-if="article" class="article-detail">
      <!-- Hero 区 -->
      <header class="article-hero">
        <h1 class="article-title">{{ article.title }}</h1>
        <ArticleMeta :article="article" />
        <hr class="hero-divider" />
      </header>

      <!-- 正文 + TOC 布局 -->
      <div class="article-layout">
        <div class="article-body">
          <div id="vditor-preview" class="article-content"></div>
        </div>
        <!-- TOC 占位（内容自动生成留待后续实现） -->
        <aside class="toc-placeholder">
          <p class="toc-label">目录</p>
        </aside>
      </div>

      <footer class="article-footer">
        <button class="like-btn" :class="{ liked }" @click="handleLike">
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24"
            :fill="liked ? 'currentColor' : 'none'" stroke="currentColor" stroke-width="2">
            <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/>
          </svg>
          {{ article.like_count }}
        </button>
      </footer>

      <CommentList :article-id="article.id" />
    </article>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import Vditor from 'vditor'
import 'vditor/dist/index.css'
import { useArticlesStore } from '@/stores/articles'
import { articlesApi } from '@/api/articles'
import { useUiStore } from '@/stores/ui'
import ArticleMeta from '@/components/article/ArticleMeta.vue'
import CommentList from '@/components/article/CommentList.vue'
import SkeletonLoader from '@/components/common/SkeletonLoader.vue'
import type { Article } from '@/types/article'

const route = useRoute()
const store = useArticlesStore()
const uiStore = useUiStore()

const article = ref<Article | null>(null)
const loading = ref(true)
const error = ref<string | null>(null)
const liked = ref(false)

function injectCopyButtons(container: HTMLElement): void {
  container.querySelectorAll('pre').forEach(pre => {
    if (pre.querySelector('.copy-btn')) return
    const btn = document.createElement('button')
    btn.className = 'copy-btn'
    btn.textContent = '复制'
    btn.onclick = () => {
      navigator.clipboard.writeText(pre.innerText)
      btn.textContent = '已复制!'
      setTimeout(() => { btn.textContent = '复制' }, 1500)
    }
    pre.style.position = 'relative'
    pre.appendChild(btn)
  })
}

async function renderContent(content: string): Promise<void> {
  const el = document.getElementById('vditor-preview') as HTMLDivElement
  if (!el) return
  await Vditor.preview(el, content, {
    mode: uiStore.isDark ? 'dark' : 'light',
  })
  injectCopyButtons(el)
}

onMounted(async () => {
  try {
    const id = Number(route.params.id)
    article.value = await store.getDetail(id)
    if (article.value) {
      await renderContent(article.value.content)
    }
  } catch {
    error.value = '文章不存在或加载失败'
  } finally {
    loading.value = false
  }
})

watch(() => uiStore.isDark, () => {
  if (article.value) renderContent(article.value.content)
})

async function handleLike(): Promise<void> {
  if (!article.value || liked.value) return
  await articlesApi.like(article.value.id)
  article.value.like_count++
  liked.value = true
}
</script>

<style scoped>
.article-hero { margin-bottom: 2rem; }
.article-title { font-size: 2rem; font-weight: 700; line-height: 1.3; margin-bottom: 0.75rem; }
.hero-divider { border: none; border-top: 1px solid var(--color-border); margin-top: 1rem; }

.article-layout {
  display: grid;
  grid-template-columns: 1fr 220px;
  gap: 2rem;
  align-items: start;
}

.article-body { max-width: 720px; }

.toc-placeholder {
  position: sticky;
  top: 5rem;
  padding: 1rem;
  background: var(--color-bg-secondary);
  border-radius: var(--radius-md);
  border: 1px solid var(--color-border);
  font-size: var(--font-size-sm);
}

.toc-label {
  font-weight: 600;
  color: var(--color-text-muted);
  margin-bottom: 0.5rem;
}

.article-footer { margin-top: 2rem; padding-top: 1rem; border-top: 1px solid var(--color-border); }

.like-btn {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  background: none;
  border: 1px solid var(--color-border);
  border-radius: 9999px;
  padding: 0.4rem 1rem;
  color: var(--color-text-muted);
  cursor: pointer;
  transition: all 0.2s;
}

.like-btn:hover { border-color: var(--color-danger); color: var(--color-danger); }
.like-btn.liked { color: var(--color-danger); border-color: var(--color-danger); }

/* 代码复制按钮（全局，注入到 vditor-preview） */
:global(#vditor-preview pre .copy-btn) {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
  padding: 2px 8px;
  font-size: 0.75rem;
  border-radius: var(--radius-sm);
  background: var(--color-bg-hover);
  border: 1px solid var(--color-border);
  color: var(--color-text-muted);
  cursor: pointer;
  opacity: 0;
  transition: opacity 0.2s;
}

:global(#vditor-preview pre:hover .copy-btn) { opacity: 1; }

@media (max-width: 1023px) {
  .article-layout { grid-template-columns: 1fr; }
  .toc-placeholder { display: none; }
}
</style>
