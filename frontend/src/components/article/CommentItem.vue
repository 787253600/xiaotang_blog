<template>
  <div class="comment-item">
    <div class="comment-avatar">{{ comment.author_name[0].toUpperCase() }}</div>
    <div class="comment-body">
      <div class="comment-meta">
        <span class="comment-author">{{ comment.author_name }}</span>
        <span class="comment-time">{{ relativeTime(comment.created_at) }}</span>
      </div>
      <p class="comment-content">{{ comment.content }}</p>
      <button v-if="depth < 2" class="reply-btn" @click="showReplyForm = !showReplyForm">回复</button>
      <form v-if="showReplyForm" class="reply-form" @submit.prevent="handleReply">
        <input v-model="replyContent" type="text" placeholder="写下回复..." required />
        <input v-model="replyName" type="text" placeholder="昵称" required maxlength="50" />
        <div class="reply-actions">
          <button type="button" @click="showReplyForm = false">取消</button>
          <button type="submit" :disabled="replying">{{ replying ? '提交中...' : '回复' }}</button>
        </div>
      </form>
      <div v-if="comment.replies?.length" class="comment-replies">
        <CommentItem
          v-for="reply in comment.replies"
          :key="reply.id"
          :comment="reply"
          :article-id="articleId"
          :depth="depth + 1"
          @reply-submitted="emit('reply-submitted')"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import client from '@/api/client'
import type { ApiResponse } from '@/types/api'

interface Comment {
  id: number
  author_name: string
  content: string
  created_at: string
  parent_id: number | null
  replies: Comment[]
}

const props = withDefaults(
  defineProps<{ comment: Comment; articleId: number; depth?: number }>(),
  { depth: 0 }
)
const emit = defineEmits<{ 'reply-submitted': [] }>()

const showReplyForm = ref(false)
const replyContent = ref('')
const replyName = ref('')
const replying = ref(false)

function relativeTime(iso: string): string {
  const diff = Date.now() - new Date(iso).getTime()
  const minutes = Math.floor(diff / 60000)
  if (minutes < 1) return '刚刚'
  if (minutes < 60) return `${minutes} 分钟前`
  const hours = Math.floor(minutes / 60)
  if (hours < 24) return `${hours} 小时前`
  return `${Math.floor(hours / 24)} 天前`
}

async function handleReply(): Promise<void> {
  replying.value = true
  try {
    await client.post<ApiResponse<Comment>>(
      `/articles/${props.articleId}/comments`,
      { author_name: replyName.value, content: replyContent.value, parent_id: props.comment.id }
    )
    showReplyForm.value = false
    replyContent.value = ''
    replyName.value = ''
    emit('reply-submitted')
  } finally {
    replying.value = false
  }
}
</script>

<style scoped>
.comment-item { display: flex; gap: 0.75rem; padding: 0.75rem 0; border-bottom: 1px solid var(--color-border); }
.comment-avatar { width: 36px; height: 36px; border-radius: 50%; background: var(--color-primary); color: white; display: flex; align-items: center; justify-content: center; font-weight: 600; font-size: var(--font-size-sm); flex-shrink: 0; }
.comment-body { flex: 1; }
.comment-meta { display: flex; gap: 0.5rem; align-items: baseline; margin-bottom: 0.25rem; }
.comment-author { font-weight: 600; font-size: var(--font-size-sm); }
.comment-time { font-size: 0.75rem; color: var(--color-text-muted); }
.comment-content { line-height: 1.6; }
.reply-btn { margin-top: 0.25rem; background: none; border: none; color: var(--color-primary); cursor: pointer; font-size: var(--font-size-sm); padding: 0; min-height: unset; }
.reply-form { margin-top: 0.5rem; display: flex; flex-direction: column; gap: 0.5rem; }
.reply-form input { padding: 0.4rem 0.75rem; border: 1px solid var(--color-border); border-radius: var(--radius-sm); background: var(--color-bg-hover); color: var(--color-text); font-size: var(--font-size-sm); }
.reply-actions { display: flex; gap: 0.5rem; justify-content: flex-end; }
.comment-replies { margin-top: 0.5rem; padding-left: 1rem; border-left: 2px solid var(--color-border); }
</style>
