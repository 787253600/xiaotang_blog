<template>
  <div class="article-list-view">
    <div class="list-header">
      <h1>文章管理</h1>
      <RouterLink to="/admin/articles/new" class="btn btn-primary">新建文章</RouterLink>
    </div>

    <div v-if="loading" class="loading">加载中...</div>
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
            <RouterLink :to="`/admin/articles/${article.id}/edit`" class="btn-sm">编辑</RouterLink>
            <button class="btn-sm btn-danger" @click="handleDelete(article.id)">删除</button>
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
  if (!confirm('确认删除此文章？')) return
  await articlesApi.delete(id)
  await load()
}

function formatDate(iso: string): string {
  return new Date(iso).toLocaleDateString('zh-CN')
}
</script>
