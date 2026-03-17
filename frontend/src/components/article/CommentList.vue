<template>
  <div class="comment-section">
    <h3>评论 ({{ comments.length }})</h3>
    <form class="comment-form" @submit.prevent="handleSubmit">
      <input v-model="form.author_name" type="text" placeholder="昵称" required maxlength="50" />
      <input v-model="form.author_email" type="email" placeholder="邮箱（可选）" maxlength="200" />
      <textarea v-model="form.content" placeholder="写下你的评论..." required maxlength="2000" rows="4" />
      <button type="submit" :disabled="submitting">{{ submitting ? '提交中...' : '发表评论' }}</button>
    </form>
    <div class="comments">
      <CommentItem
        v-for="comment in comments"
        :key="comment.id"
        :comment="comment"
        :article-id="articleId"
        :depth="0"
        @reply-submitted="fetchComments"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, reactive } from 'vue'
import client from '@/api/client'
import CommentItem from './CommentItem.vue'
import type { ApiResponse } from '@/types/api'

interface Comment {
  id: number
  author_name: string
  content: string
  created_at: string
  parent_id: number | null
  replies: Comment[]
}

const props = defineProps<{ articleId: number }>()
const comments = ref<Comment[]>([])
const submitting = ref(false)
const form = reactive({ author_name: '', author_email: '', content: '' })

async function fetchComments(): Promise<void> {
  const res = await client.get<ApiResponse<Comment[]>>(`/articles/${props.articleId}/comments`)
  comments.value = res.data.data ?? []
}

onMounted(fetchComments)

async function handleSubmit(): Promise<void> {
  submitting.value = true
  try {
    const res = await client.post<ApiResponse<Comment>>(`/articles/${props.articleId}/comments`, form)
    if (res.data.data) {
      comments.value.push(res.data.data)
      form.author_name = ''
      form.author_email = ''
      form.content = ''
    }
  } finally {
    submitting.value = false
  }
}
</script>
