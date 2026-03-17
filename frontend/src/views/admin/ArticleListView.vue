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
</style>
