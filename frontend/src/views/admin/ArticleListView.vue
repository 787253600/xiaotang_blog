<template>
  <div class="article-list-view">
    <div class="list-header">
      <h1>文章管理</h1>
      <RouterLink to="/admin/articles/new" class="btn btn-primary">新建文章</RouterLink>
    </div>

    <SkeletonLoader v-if="loading" :lines="5" />
    <table v-else-if="result" class="article-table">
      <thead>
        <tr>
          <th>标题</th>
          <th>分类</th>
          <th>状态</th>
          <th>创建时间</th>
          <th>操作</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="article in result.items" :key="article.id">
          <td>{{ article.title }}</td>
          <td>{{ article.category?.name ?? '未分类' }}</td>
          <td>
            <span :class="article.is_published ? 'badge-published' : 'badge-draft'">
              {{ article.is_published ? '已发布' : '草稿' }}
            </span>
          </td>
          <td>{{ formatDate(article.created_at) }}</td>
          <td>
            <RouterLink :to="`/admin/articles/${article.id}/edit`" class="icon-action-btn" title="编辑">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
              </svg>
            </RouterLink>
            <button class="icon-action-btn delete" @click="handleDelete(article.id)" title="删除">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="3 6 5 6 21 6"/><path d="M19 6l-1 14H6L5 6"/><path d="M10 11v6"/><path d="M14 11v6"/><path d="M9 6V4h6v2"/>
              </svg>
            </button>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- 移动端：卡片列表 -->
    <div v-if="result" class="article-cards-mobile">
      <div v-for="article in result.items" :key="article.id" class="admin-article-card">
        <div class="admin-card-main">
          <span class="admin-card-title">{{ article.title }}</span>
          <span class="admin-card-category">{{ article.category?.name ?? '未分类' }}</span>
        </div>
        <div class="admin-card-right">
          <span :class="article.is_published ? 'badge-published' : 'badge-draft'">
            {{ article.is_published ? '已发布' : '草稿' }}
          </span>
        </div>
      </div>
    </div>

    <AppPagination
      v-if="result && result.total_pages > 1"
      :current-page="page"
      :total-pages="result.total_pages"
      @change="page = $event"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { RouterLink } from 'vue-router'
import { articlesApi } from '@/api/articles'
import AppPagination from '@/components/common/AppPagination.vue'
import type { Paginated } from '@/types/api'
import type { ArticleSummary } from '@/types/article'
import { useConfirm } from '@/composables/useConfirm'
import { useToastStore } from '@/stores/toast'
import SkeletonLoader from '@/components/common/SkeletonLoader.vue'
const { confirm } = useConfirm()
const toastStore = useToastStore()

const page = ref(1)
const result = ref<Paginated<ArticleSummary> | null>(null)
const loading = ref(false)

async function load(): Promise<void> {
  loading.value = true
  try {
    const res = await articlesApi.list({ page: page.value, page_size: 20 })
    result.value = res.data
  } finally {
    loading.value = false
  }
}

watch(page, load, { immediate: true })

async function handleDelete(id: number): Promise<void> {
  const ok = await confirm({
    title: '确认删除',
    message: '删除后无法恢复，确认删除此文章？',
    confirmText: '删除',
  })
  if (!ok) return
  await articlesApi.delete(id)
  toastStore.add('文章已删除', 'success')
  await load()
}

function formatDate(iso: string): string {
  return new Date(iso).toLocaleDateString('zh-CN')
}
</script>

<style scoped>
.article-table tbody tr:nth-child(even) { background: var(--color-bg-hover); }
.article-table tbody tr:hover { background: var(--color-bg-hover); }
.icon-action-btn {
  width: 32px;
  height: 32px;
  border-radius: var(--radius-sm);
  background: none;
  border: none;
  cursor: pointer;
  color: var(--color-text-muted);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  transition: background 0.15s, color 0.15s;
  text-decoration: none;
}
.icon-action-btn:hover { background: var(--color-bg-hover); color: var(--color-text); }
.icon-action-btn.delete:hover { color: var(--color-danger); }

.article-cards-mobile { display: none; }

@media (max-width: 639px) {
  .article-table { display: none; }
  .article-cards-mobile {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
  }
  .admin-article-card {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.75rem 1rem;
    background: var(--color-bg-secondary);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
  }
  .admin-card-main {
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
  }
  .admin-card-title {
    font-weight: 500;
    color: var(--color-text);
  }
  .admin-card-category {
    font-size: var(--font-size-sm);
    color: var(--color-text-muted);
  }
  .badge-published {
    font-size: 0.75rem;
    padding: 2px 8px;
    border-radius: 9999px;
    background: rgba(63,185,80,0.15);
    color: var(--color-success);
  }
  .badge-draft {
    font-size: 0.75rem;
    padding: 2px 8px;
    border-radius: 9999px;
    background: var(--color-bg-hover);
    color: var(--color-text-muted);
  }
}
</style>
