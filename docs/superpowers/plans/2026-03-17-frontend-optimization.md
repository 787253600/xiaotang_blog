# Frontend Optimization Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 全面升级博客前端视觉（GitHub 技术风深色主题）、补全 UX 功能（骨架屏/Toast/弹窗/空状态）、修复已知 Bug，并实现移动优先响应式。

**Architecture:** 以设计 Token 重构为地基，分层逐步向上：先改全局 CSS 变量和主题系统，再新建共用 UX 组件，然后修复 Bug，最后逐组件完成视觉和移动端改造。每个 Task 独立提交，可单独验证。

**Tech Stack:** Vue 3 + TypeScript + Vite + Pinia + Vditor | CSS custom properties | @fontsource/inter

---

## 前置：开发环境确认

在开始前，确认前端开发服务器可以正常启动：

```bash
cd C:/Users/choub/Desktop/python/Xiaotangblog/frontend
npm install
npm run dev
```

浏览器访问 `http://localhost:3000`，确认页面能正常加载。

---

## Task 1: 安装依赖 + 设计 Token 重构

**Files:**
- Modify: `frontend/package.json`
- Modify: `frontend/src/styles/variables.css`
- Modify: `frontend/src/styles/main.css`
- Modify: `frontend/src/main.ts`
- Modify: `frontend/src/stores/ui.ts`
- Modify: `frontend/src/App.vue`

### Step 1.1: 安装 Inter 字体包

- [ ] 执行安装命令：
  ```bash
  cd C:/Users/choub/Desktop/python/Xiaotangblog/frontend
  npm install @fontsource/inter
  ```
  预期：`package.json` 中出现 `@fontsource/inter` 依赖。

### Step 1.2: 重写 variables.css

- [ ] 将 `frontend/src/styles/variables.css` 完整替换为：

  ```css
  :root {
    /* 深色主题（全局默认） */
    --color-bg:           #0d1117;
    --color-bg-secondary: #161b22;
    --color-bg-hover:     #21262d;
    --color-primary:      #58a6ff;
    --color-primary-hover:#79b8ff;
    --color-danger:       #f78166;
    --color-error:        var(--color-danger); /* 向后兼容别名 */
    --color-success:      #3fb950;
    --color-text:         #e6edf3;
    --color-text-muted:   #8b949e;
    --color-border:       #30363d;
    --shadow-sm: 0 1px 3px rgba(0,0,0,0.4);
    --shadow-md: 0 4px 12px rgba(0,0,0,0.5);
  
    /* 间距（保留不变） */
    --spacing-xs: 0.25rem;
    --spacing-sm: 0.5rem;
    --spacing-md: 1rem;
    --spacing-lg: 1.5rem;
    --spacing-xl: 2rem;
  
    /* 字体 */
    --font-sans: 'Inter', 'PingFang SC', system-ui, sans-serif;
    --font-mono: 'JetBrains Mono', 'Fira Code', Consolas, monospace;
    --font-size-sm: 0.875rem;
    --font-size-base: 1rem;
    --font-size-lg: 1.125rem;
    --font-size-xl: 1.25rem;
    --font-size-2xl: 1.5rem;
    --line-height-body: 1.7;
  
    /* 圆角（保留不变） */
    --radius-sm: 0.25rem;
    --radius-md: 0.5rem;
    --radius-lg: 0.75rem;
  
    /* 最大宽度（保留不变） */
    --max-width: 1200px;
    --content-width: 860px;
  }
  
  /* 浅色主题（.app-wrapper.light 触发） */
  .app-wrapper.light {
    --color-bg:           #ffffff;
    --color-bg-secondary: #f6f8fa;
    --color-bg-hover:     #eaeef2;
    --color-primary:      #0969da;
    --color-primary-hover:#0550ae;
    --color-danger:       #cf222e;
    --color-success:      #1a7f37;
    --color-text:         #1f2328;
    --color-text-muted:   #656d76;
    --color-border:       #d0d7de;
    --shadow-sm: 0 1px 3px rgba(0,0,0,0.1);
    --shadow-md: 0 4px 12px rgba(0,0,0,0.15);
  }
  ```

  注意：旧的 `.dark { ... }` 块已被删除，不要保留。

### Step 1.3: 修复 main.css 中的旧 token 引用

- [ ] 在 `frontend/src/styles/main.css` 中：
  - 将第 201–203 行 `.btn-danger { color: var(--color-error); border-color: var(--color-error); }` 改为 `var(--color-danger)`
  - 将第 217–219 行 `.error { color: var(--color-error); }` 改为 `var(--color-danger)`
  - 在文件顶部 `@import './variables.css';` 之后添加：
    ```css
    /* body 继承 :root token，无需修改 */
    body {
      line-height: var(--line-height-body);
    }
    ```

### Step 1.4: 修改 ui.ts 默认值

- [ ] 打开 `frontend/src/stores/ui.ts`，将第 8 行：
  ```typescript
  const isDark = ref(localStorage.getItem('theme') === 'dark')
  ```
  改为：
  ```typescript
  const isDark = ref(localStorage.getItem('theme') !== 'light')
  ```

### Step 1.5: 修改 App.vue 主题类 + 注册全局组件占位

- [ ] 将 `frontend/src/App.vue` 替换为：
  ```vue
  <template>
    <div :class="['app-wrapper', { light: !uiStore.isDark }]">
      <AppHeader />
      <main class="main-content">
        <RouterView />
      </main>
      <AppFooter />
      <!-- 全局单例组件（Task 2 新建后取消注释）
      <AppToast />
      <ConfirmModal />
      -->
    </div>
  </template>
  
  <script setup lang="ts">
  import { RouterView } from 'vue-router'
  import AppHeader from '@/components/common/AppHeader.vue'
  import AppFooter from '@/components/common/AppFooter.vue'
  import { useUiStore } from '@/stores/ui'
  // import AppToast from '@/components/common/AppToast.vue'
  // import ConfirmModal from '@/components/common/ConfirmModal.vue'
  
  const uiStore = useUiStore()
  </script>
  ```

### Step 1.6: 在 main.ts 中引入 Inter 字体

- [ ] 打开 `frontend/src/main.ts`，在顶部添加：
  ```typescript
  import '@fontsource/inter'
  ```

### Step 1.7: 验证

- [ ] 运行 `npm run dev`，访问 `http://localhost:3000`
- [ ] 预期：页面背景变为深色 `#0d1117`，文字为浅色；字体变为 Inter（更现代感）
- [ ] 浏览器 DevTools → Elements，确认 `.app-wrapper` 无 `.light` 类（深色默认）
- [ ] 点击主题切换按钮，确认切换为浅色（`.light` 类出现）

### Step 1.8: 提交

- [ ] ```bash
  git add frontend/package.json frontend/package-lock.json \
        frontend/src/styles/variables.css frontend/src/styles/main.css \
        frontend/src/main.ts frontend/src/stores/ui.ts frontend/src/App.vue
  git commit -m "feat: 重构设计 token，切换为深色默认主题"
  ```

---

## Task 2: 新建 UX 基础组件

**Files:**
- Create: `frontend/src/stores/toast.ts`
- Create: `frontend/src/components/common/AppToast.vue`
- Create: `frontend/src/composables/useConfirm.ts`
- Create: `frontend/src/components/common/ConfirmModal.vue`
- Create: `frontend/src/components/common/SkeletonLoader.vue`
- Create: `frontend/src/components/common/EmptyState.vue`
- Modify: `frontend/src/App.vue`

### Step 2.1: 创建 toast store

- [ ] 新建 `frontend/src/stores/toast.ts`：
  ```typescript
  import { defineStore } from 'pinia'
  import { ref } from 'vue'
  
  export interface Toast {
    id: string
    type: 'success' | 'error' | 'info'
    message: string
  }
  
  export const useToastStore = defineStore('toast', () => {
    const toasts = ref<Toast[]>([])
  
    function add(message: string, type: Toast['type'] = 'info'): void {
      if (toasts.value.length >= 3) {
        toasts.value.shift()
      }
      const id = Math.random().toString(36).slice(2)
      toasts.value.push({ id, type, message })
      setTimeout(() => remove(id), 3000)
    }
  
    function remove(id: string): void {
      const idx = toasts.value.findIndex(t => t.id === id)
      if (idx !== -1) toasts.value.splice(idx, 1)
    }
  
    return { toasts, add, remove }
  })
  ```

### Step 2.2: 创建 AppToast 组件

- [ ] 新建 `frontend/src/components/common/AppToast.vue`：
  ```vue
  <template>
    <Teleport to="body">
      <div class="toast-container">
        <TransitionGroup name="toast">
          <div
            v-for="toast in toastStore.toasts"
            :key="toast.id"
            :class="['toast', `toast-${toast.type}`]"
          >
            <span class="toast-icon">
              <span v-if="toast.type === 'success'">✓</span>
              <span v-else-if="toast.type === 'error'">✕</span>
              <span v-else>ℹ</span>
            </span>
            {{ toast.message }}
            <button class="toast-close" @click="toastStore.remove(toast.id)">×</button>
          </div>
        </TransitionGroup>
      </div>
    </Teleport>
  </template>
  
  <script setup lang="ts">
  import { useToastStore } from '@/stores/toast'
  const toastStore = useToastStore()
  </script>
  
  <style scoped>
  .toast-container {
    position: fixed;
    bottom: 1.5rem;
    right: 1.5rem;
    z-index: 9999;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .toast {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.75rem 1rem;
    border-radius: var(--radius-md);
    background: var(--color-bg-secondary);
    border: 1px solid var(--color-border);
    color: var(--color-text);
    font-size: var(--font-size-sm);
    min-width: 240px;
    max-width: 360px;
    box-shadow: var(--shadow-md);
  }
  
  .toast-success { border-left: 3px solid var(--color-success); }
  .toast-error   { border-left: 3px solid var(--color-danger); }
  .toast-info    { border-left: 3px solid var(--color-primary); }
  
  .toast-icon { font-weight: bold; flex-shrink: 0; }
  .toast-success .toast-icon { color: var(--color-success); }
  .toast-error   .toast-icon { color: var(--color-danger); }
  .toast-info    .toast-icon { color: var(--color-primary); }
  
  .toast-close {
    margin-left: auto;
    background: none;
    border: none;
    color: var(--color-text-muted);
    cursor: pointer;
    padding: 0;
    font-size: 1rem;
    line-height: 1;
    min-height: unset;
  }
  
  .toast-enter-active, .toast-leave-active { transition: all 0.3s ease; }
  .toast-enter-from { opacity: 0; transform: translateX(100%); }
  .toast-leave-to   { opacity: 0; transform: translateX(100%); }
  </style>
  ```

### Step 2.3: 创建 useConfirm composable

- [ ] 新建 `frontend/src/composables/useConfirm.ts`：
  ```typescript
  import { reactive } from 'vue'
  
  export interface ConfirmOptions {
    title: string
    message: string
    confirmText?: string
  }
  
  const state = reactive({
    visible: false,
    options: {} as ConfirmOptions,
    resolve: null as ((value: boolean) => void) | null,
  })
  
  export function useConfirm() {
    function confirm(options: ConfirmOptions): Promise<boolean> {
      state.options = options
      state.visible = true
      return new Promise(r => { state.resolve = r })
    }
  
    function accept(): void {
      state.resolve?.(true)
      state.visible = false
    }
  
    function cancel(): void {
      state.resolve?.(false)
      state.visible = false
    }
  
    return { confirm, accept, cancel, state }
  }
  ```

### Step 2.4: 创建 ConfirmModal 组件

- [ ] 新建 `frontend/src/components/common/ConfirmModal.vue`：
  ```vue
  <template>
    <Teleport to="body">
      <Transition name="modal">
        <div v-if="state.visible" class="modal-overlay" @click.self="cancel">
          <div class="modal-box">
            <div class="modal-icon">⚠️</div>
            <h3 class="modal-title">{{ state.options.title }}</h3>
            <p class="modal-message">{{ state.options.message }}</p>
            <div class="modal-actions">
              <button class="btn" @click="cancel">取消</button>
              <button class="btn btn-delete" @click="accept">
                {{ state.options.confirmText ?? '确认' }}
              </button>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>
  </template>
  
  <script setup lang="ts">
  import { useConfirm } from '@/composables/useConfirm'
  const { state, accept, cancel } = useConfirm()
  </script>
  
  <style scoped>
  .modal-overlay {
    position: fixed;
    inset: 0;
    background: rgba(0,0,0,0.6);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
  }
  
  .modal-box {
    background: var(--color-bg-secondary);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-lg);
    padding: 2rem;
    max-width: 400px;
    width: 90%;
    text-align: center;
    box-shadow: var(--shadow-md);
  }
  
  .modal-icon { font-size: 2rem; margin-bottom: 0.75rem; }
  .modal-title { font-size: var(--font-size-xl); margin-bottom: 0.5rem; }
  .modal-message { color: var(--color-text-muted); margin-bottom: 1.5rem; }
  
  .modal-actions { display: flex; gap: 0.75rem; justify-content: center; }
  
  .btn-delete {
    background: var(--color-danger);
    color: white;
    border-color: var(--color-danger);
  }
  
  .modal-enter-active, .modal-leave-active { transition: opacity 0.2s; }
  .modal-enter-from, .modal-leave-to { opacity: 0; }
  </style>
  ```

### Step 2.5: 创建 SkeletonLoader 组件

- [ ] 新建 `frontend/src/components/common/SkeletonLoader.vue`：
  ```vue
  <template>
    <div class="skeleton-wrapper">
      <div v-for="i in lines" :key="i" class="skeleton-line" :style="lineStyle(i)" />
    </div>
  </template>
  
  <script setup lang="ts">
  const props = withDefaults(defineProps<{ lines?: number }>(), { lines: 3 })
  
  function lineStyle(i: number) {
    // 最后一行短一些，增加真实感
    return { width: i === props.lines ? '60%' : '100%' }
  }
  </script>
  
  <style scoped>
  .skeleton-wrapper { display: flex; flex-direction: column; gap: 0.75rem; padding: 1.25rem; }
  
  .skeleton-line {
    height: 1rem;
    border-radius: var(--radius-sm);
    background: linear-gradient(
      90deg,
      var(--color-bg-hover) 25%,
      var(--color-border) 50%,
      var(--color-bg-hover) 75%
    );
    background-size: 200% 100%;
    animation: shimmer 1.5s infinite;
  }
  
  @keyframes shimmer {
    0%   { background-position: 200% 0; }
    100% { background-position: -200% 0; }
  }
  </style>
  ```

### Step 2.6: 创建 EmptyState 组件

- [ ] 新建 `frontend/src/components/common/EmptyState.vue`：
  ```vue
  <template>
    <div class="empty-state">
      <div v-if="icon" class="empty-icon" v-html="icon" />
      <p class="empty-title">{{ title }}</p>
      <p v-if="description" class="empty-desc">{{ description }}</p>
      <RouterLink v-if="actionText && actionTo" :to="actionTo" class="btn btn-primary empty-action">
        {{ actionText }}
      </RouterLink>
    </div>
  </template>
  
  <script setup lang="ts">
  import { RouterLink } from 'vue-router'
  defineProps<{
    icon?: string
    title: string
    description?: string
    actionText?: string
    actionTo?: string
  }>()
  </script>
  
  <style scoped>
  .empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 3rem 1rem;
    text-align: center;
    color: var(--color-text-muted);
  }
  
  .empty-icon { font-size: 3rem; margin-bottom: 1rem; opacity: 0.5; }
  .empty-title { font-size: var(--font-size-lg); font-weight: 500; color: var(--color-text); }
  .empty-desc { margin-top: 0.5rem; font-size: var(--font-size-sm); }
  .empty-action { margin-top: 1.25rem; }
  </style>
  ```

### Step 2.7: 在 App.vue 中挂载全局组件

- [ ] 取消注释 `frontend/src/App.vue` 中的 import 和模板标签：
  ```vue
  <template>
    <div :class="['app-wrapper', { light: !uiStore.isDark }]">
      <AppHeader />
      <main class="main-content">
        <RouterView />
      </main>
      <AppFooter />
      <AppToast />
      <ConfirmModal />
    </div>
  </template>
  
  <script setup lang="ts">
  import { RouterView } from 'vue-router'
  import AppHeader from '@/components/common/AppHeader.vue'
  import AppFooter from '@/components/common/AppFooter.vue'
  import AppToast from '@/components/common/AppToast.vue'
  import ConfirmModal from '@/components/common/ConfirmModal.vue'
  import { useUiStore } from '@/stores/ui'
  
  const uiStore = useUiStore()
  </script>
  ```

### Step 2.8: 验证

- [ ] `npm run dev`，确认无 TypeScript 编译错误
- [ ] 浏览器 Console 无报错

### Step 2.9: 提交

- [ ] ```bash
  git add frontend/src/stores/toast.ts \
        frontend/src/components/common/AppToast.vue \
        frontend/src/composables/useConfirm.ts \
        frontend/src/components/common/ConfirmModal.vue \
        frontend/src/components/common/SkeletonLoader.vue \
        frontend/src/components/common/EmptyState.vue \
        frontend/src/App.vue
  git commit -m "feat: 新增 Toast/ConfirmModal/SkeletonLoader/EmptyState 基础组件"
  ```

---

## Task 3: Bug 修复

**Files:**
- Create: `frontend/src/components/article/CommentItem.vue`
- Modify: `frontend/src/components/article/CommentList.vue`
- Modify: `frontend/src/views/public/SearchView.vue`

### Step 3.1: 新建 CommentItem 组件

- [ ] 新建 `frontend/src/components/article/CommentItem.vue`：
  ```vue
  <template>
    <div class="comment-item">
      <div class="comment-avatar">{{ comment.author_name[0].toUpperCase() }}</div>
      <div class="comment-body">
        <div class="comment-meta">
          <span class="comment-author">{{ comment.author_name }}</span>
          <span class="comment-time">{{ relativeTime(comment.created_at) }}</span>
        </div>
        <p class="comment-content">{{ comment.content }}</p>
        <button v-if="depth < 2" class="reply-btn" @click="showReplyForm = !showReplyForm">
          回复
        </button>
  
        <!-- 内联回复表单 -->
        <form v-if="showReplyForm" class="reply-form" @submit.prevent="handleReply">
          <input v-model="replyContent" type="text" placeholder="写下回复..." required />
          <input v-model="replyName" type="text" placeholder="昵称" required maxlength="50" />
          <div class="reply-actions">
            <button type="button" @click="showReplyForm = false">取消</button>
            <button type="submit" :disabled="replying">{{ replying ? '提交中...' : '回复' }}</button>
          </div>
        </form>
  
        <!-- 嵌套回复 -->
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
        {
          author_name: replyName.value,
          content: replyContent.value,
          parent_id: props.comment.id,
        }
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
  .comment-item {
    display: flex;
    gap: 0.75rem;
    padding: 0.75rem 0;
    border-bottom: 1px solid var(--color-border);
  }
  
  .comment-avatar {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    background: var(--color-primary);
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 600;
    font-size: var(--font-size-sm);
    flex-shrink: 0;
  }
  
  .comment-body { flex: 1; }
  
  .comment-meta {
    display: flex;
    gap: 0.5rem;
    align-items: baseline;
    margin-bottom: 0.25rem;
  }
  
  .comment-author { font-weight: 600; font-size: var(--font-size-sm); }
  .comment-time { font-size: 0.75rem; color: var(--color-text-muted); }
  .comment-content { line-height: 1.6; }
  
  .reply-btn {
    margin-top: 0.25rem;
    background: none;
    border: none;
    color: var(--color-primary);
    cursor: pointer;
    font-size: var(--font-size-sm);
    padding: 0;
    min-height: unset;
  }
  
  .reply-form {
    margin-top: 0.5rem;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .reply-form input {
    padding: 0.4rem 0.75rem;
    border: 1px solid var(--color-border);
    border-radius: var(--radius-sm);
    background: var(--color-bg-hover);
    color: var(--color-text);
    font-size: var(--font-size-sm);
  }
  
  .reply-actions { display: flex; gap: 0.5rem; justify-content: flex-end; }
  
  .comment-replies { margin-top: 0.5rem; padding-left: 1rem; border-left: 2px solid var(--color-border); }
  </style>
  ```

### Step 3.2: 修复 CommentList.vue

- [ ] 将 `frontend/src/components/article/CommentList.vue` 的 `<script setup>` 修改如下（提取 fetchComments + 添加 import + 添加 @reply-submitted）：

  ```vue
  <template>
    <div class="comment-section">
      <h3>评论 ({{ comments.length }})</h3>
  
      <form class="comment-form" @submit.prevent="handleSubmit">
        <input v-model="form.author_name" type="text" placeholder="昵称" required maxlength="50" />
        <input v-model="form.author_email" type="email" placeholder="邮箱（可选）" maxlength="200" />
        <textarea v-model="form.content" placeholder="写下你的评论..." required maxlength="2000" rows="4" />
        <button type="submit" :disabled="submitting">
          {{ submitting ? '提交中...' : '发表评论' }}
        </button>
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
    const res = await client.get<ApiResponse<Comment[]>>(
      `/articles/${props.articleId}/comments`
    )
    comments.value = res.data.data ?? []
  }
  
  onMounted(fetchComments)
  
  async function handleSubmit(): Promise<void> {
    submitting.value = true
    try {
      const res = await client.post<ApiResponse<Comment>>(
        `/articles/${props.articleId}/comments`,
        form
      )
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
  ```

### Step 3.3: 修复 SearchView.vue

- [ ] 将 `frontend/src/views/public/SearchView.vue` 完整替换为：

  ```vue
  <template>
    <div class="search-view">
      <SearchBar :initial-query="query" @search="handleSearch" />
  
      <div v-if="loading" class="loading">搜索中...</div>
      <div v-else-if="error" class="error">{{ error }}</div>
      <template v-else-if="results !== null">
        <p class="result-count">找到 {{ total }} 篇相关文章</p>
        <EmptyState v-if="results.length === 0" title="没有找到相关文章" description="换个关键词试试" />
        <template v-else>
          <ArticleCard v-for="article in results" :key="article.id" :article="article" />
          <AppPagination
            v-if="totalPages > 1"
            :current-page="page"
            :total-pages="totalPages"
            @change="handlePageChange"
          />
        </template>
      </template>
    </div>
  </template>
  
  <script setup lang="ts">
  import { ref, watch, onMounted } from 'vue'
  import { useRoute, useRouter } from 'vue-router'
  import { articlesApi } from '@/api/articles'
  import SearchBar from '@/components/search/SearchBar.vue'
  import ArticleCard from '@/components/article/ArticleCard.vue'
  import AppPagination from '@/components/common/AppPagination.vue'
  import EmptyState from '@/components/common/EmptyState.vue'
  import type { ArticleSummary } from '@/types/article'
  
  const route = useRoute()
  const router = useRouter()
  
  const query = ref('')
  const results = ref<ArticleSummary[] | null>(null)
  const total = ref(0)
  const totalPages = ref(1)
  const page = ref(1)
  const loading = ref(false)
  const error = ref<string | null>(null)
  
  async function doSearch(q: string, p: number): Promise<void> {
    if (!q.trim()) return
    loading.value = true
    error.value = null
    try {
      const res = await articlesApi.search(q, p)
      results.value = res.data.items
      total.value = res.data.total
      totalPages.value = res.data.total_pages
    } catch {
      error.value = '搜索失败，请稍后重试'
    } finally {
      loading.value = false
    }
  }
  
  onMounted(() => {
    const q = route.query.q as string
    if (q) { query.value = q; doSearch(q, 1) }
  })
  
  watch(() => route.query.q, (q) => {
    if (q) { query.value = q as string; doSearch(q as string, 1) }
  })
  
  function handleSearch(q: string): void {
    router.push({ path: '/search', query: { q } })
    query.value = q
    page.value = 1
    doSearch(q, 1)
  }
  
  function handlePageChange(p: number): void {
    page.value = p
    doSearch(query.value, p)  // 直接调用，无防抖
  }
  </script>
  ```

  > 注意：需确认 `articlesApi.search` 的签名。打开 `frontend/src/api/articles.ts`，确认 search 方法接受 `(query: string, page?: number)` 参数；若参数名不同，按实际调整。

### Step 3.4: 验证

- [ ] `npm run dev`，访问搜索页 `http://localhost:3000/search?q=test`
- [ ] 预期：搜索结果正常显示为 ArticleCard 列表，分页正常工作
- [ ] 访问任意文章详情页，确认评论区正常加载（不报 CommentItem 未定义错误）

### Step 3.5: 提交

- [ ] ```bash
  git add frontend/src/components/article/CommentItem.vue \
        frontend/src/components/article/CommentList.vue \
        frontend/src/views/public/SearchView.vue
  git commit -m "fix: 修复 SearchView props 不匹配、新建 CommentItem 组件"
  ```

---

## Task 4: AppHeader 视觉升级

**Files:**
- Modify: `frontend/src/components/common/AppHeader.vue`
- Modify: `frontend/src/styles/main.css`

### Step 4.1: 重写 AppHeader

- [ ] 将 `frontend/src/components/common/AppHeader.vue` 完整替换为：

  ```vue
  <template>
    <header class="app-header">
      <div class="header-inner">
        <RouterLink to="/" class="logo">
          <span class="logo-bracket">&lt;/&gt;</span> 小汤博客
        </RouterLink>
  
        <!-- 桌面端导航 -->
        <nav class="nav desktop-nav">
          <RouterLink to="/">首页</RouterLink>
          <RouterLink to="/search">搜索</RouterLink>
          <RouterLink v-if="authStore.isLoggedIn" to="/admin">后台</RouterLink>
        </nav>
  
        <div class="header-actions">
          <button class="icon-btn" @click="uiStore.toggleTheme" :title="uiStore.isDark ? '切换浅色' : '切换深色'">
            <!-- 太阳图标（浅色时显示，表示当前深色可切换到浅色） -->
            <svg v-if="uiStore.isDark" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/>
              <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/>
              <line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/>
              <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/>
            </svg>
            <!-- 月亮图标（深色时显示） -->
            <svg v-else xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>
            </svg>
          </button>
          <button v-if="authStore.isLoggedIn" class="icon-btn logout-btn" @click="handleLogout" title="退出">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/>
            </svg>
          </button>
          <!-- 移动端汉堡按钮 -->
          <button class="icon-btn hamburger" @click="mobileMenuOpen = !mobileMenuOpen" title="菜单">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="18" x2="21" y2="18"/>
            </svg>
          </button>
        </div>
      </div>
  
      <!-- 移动端导航抽屉 -->
      <Transition name="drawer">
        <nav v-if="mobileMenuOpen" class="mobile-nav" @click="mobileMenuOpen = false">
          <RouterLink to="/">首页</RouterLink>
          <RouterLink to="/search">搜索</RouterLink>
          <RouterLink v-if="authStore.isLoggedIn" to="/admin">后台</RouterLink>
        </nav>
      </Transition>
    </header>
  </template>
  
  <script setup lang="ts">
  import { ref } from 'vue'
  import { RouterLink, useRouter } from 'vue-router'
  import { useAuthStore } from '@/stores/auth'
  import { useUiStore } from '@/stores/ui'
  
  const authStore = useAuthStore()
  const uiStore = useUiStore()
  const router = useRouter()
  const mobileMenuOpen = ref(false)
  
  async function handleLogout(): Promise<void> {
    await authStore.logout()
    router.push('/')
  }
  </script>
  
  <style scoped>
  .app-header {
    position: sticky;
    top: 0;
    z-index: 100;
    background: rgba(13,17,23,0.85);
    backdrop-filter: blur(12px);
    border-bottom: 1px solid var(--color-border);
  }
  
  .light .app-header,
  :global(.app-wrapper.light) .app-header {
    background: rgba(255,255,255,0.85);
  }
  
  .header-inner {
    max-width: var(--max-width);
    margin: 0 auto;
    padding: 0.75rem var(--spacing-md);
    display: flex;
    align-items: center;
    gap: var(--spacing-lg);
  }
  
  .logo {
    font-family: var(--font-mono);
    font-size: var(--font-size-xl);
    font-weight: 700;
    color: var(--color-text);
    text-decoration: none;
    display: flex;
    align-items: center;
    gap: 0.4rem;
  }
  
  .logo-bracket { color: var(--color-primary); }
  
  .desktop-nav {
    display: flex;
    gap: var(--spacing-md);
    flex: 1;
  }
  
  .desktop-nav a {
    color: var(--color-text-muted);
    text-decoration: none;
    font-size: var(--font-size-sm);
    padding-bottom: 2px;
    border-bottom: 2px solid transparent;
    transition: color 0.15s, border-color 0.15s;
  }
  
  .desktop-nav a:hover,
  .desktop-nav a.router-link-active {
    color: var(--color-text);
    border-bottom-color: var(--color-primary);
  }
  
  .header-actions {
    display: flex;
    gap: 0.25rem;
    align-items: center;
  }
  
  .icon-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 36px;
    height: 36px;
    border-radius: var(--radius-md);
    background: none;
    border: none;
    color: var(--color-text-muted);
    cursor: pointer;
    transition: background 0.15s, color 0.15s;
    min-height: unset;
    padding: 0;
  }
  
  .icon-btn:hover { background: var(--color-bg-hover); color: var(--color-text); }
  
  .hamburger { display: none; }
  
  .mobile-nav {
    display: flex;
    flex-direction: column;
    padding: 0.5rem var(--spacing-md) 1rem;
    border-top: 1px solid var(--color-border);
  }
  
  .mobile-nav a {
    padding: 0.75rem 0;
    color: var(--color-text);
    text-decoration: none;
    border-bottom: 1px solid var(--color-border);
    min-height: 44px;
    display: flex;
    align-items: center;
  }
  
  .drawer-enter-active, .drawer-leave-active { transition: opacity 0.2s, transform 0.2s; }
  .drawer-enter-from, .drawer-leave-to { opacity: 0; transform: translateY(-8px); }
  
  @media (max-width: 639px) {
    .desktop-nav { display: none; }
    .hamburger { display: flex; }
  }
  </style>
  ```

  > 注意：`scoped` 样式中的 `.light .app-header` 不会跨组件生效，改用 `:global(.app-wrapper.light) .app-header` 或将背景色写为 CSS 变量（推荐：在 variables.css 中添加 `--header-bg` token，深色值为 `rgba(13,17,23,0.85)`，浅色值为 `rgba(255,255,255,0.85)`）。实际实现时，在 AppHeader 的 `<style scoped>` 中，直接使用 `:global(.app-wrapper.light) .app-header { background: rgba(255,255,255,0.85); }`。

### Step 4.2: 验证

- [ ] 页面顶部导航栏呈现毛玻璃效果（深色背景半透明）
- [ ] 主题切换按钮显示 SVG 图标而非 emoji
- [ ] 移动端（DevTools 模拟手机）hamburger 图标可见，点击展开导航

### Step 4.3: 提交

- [ ] ```bash
  git add frontend/src/components/common/AppHeader.vue
  git commit -m "feat: AppHeader 视觉升级，毛玻璃效果 + SVG 图标 + 移动端汉堡菜单"
  ```

---

## Task 5: ArticleCard 视觉升级

**Files:**
- Modify: `frontend/src/components/article/ArticleCard.vue`
- Modify: `frontend/src/styles/main.css`

### Step 5.1: 重写 ArticleCard

- [ ] 将 `frontend/src/components/article/ArticleCard.vue` 完整替换为：

  ```vue
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
  ```

### Step 5.2: 更新 main.css 中的文章卡片样式

- [ ] 在 `frontend/src/styles/main.css` 中，找到 `.article-card` 相关样式（第 93–121 行），替换为：

  ```css
  /* 文章卡片 */
  .article-card {
    padding: 1.25rem;
    border: 1px solid var(--color-border);
    border-left: 3px solid var(--card-accent, var(--color-primary));
    border-radius: var(--radius-md);
    margin-bottom: var(--spacing-md);
    background: var(--color-bg-secondary);
    transition: box-shadow 0.2s, transform 0.2s, border-color 0.2s;
  }
  
  .article-card:hover {
    box-shadow: var(--shadow-md);
    transform: translateY(-2px);
    border-color: var(--color-primary);
  }
  
  .card-title h2 {
    font-size: var(--font-size-xl);
    font-weight: 600;
    color: var(--color-text);
    transition: color 0.15s;
  }
  
  .card-title:hover h2 { color: var(--color-primary); }
  
  .card-excerpt {
    margin-top: var(--spacing-sm);
    color: var(--color-text-muted);
    line-height: var(--line-height-body);
  }
  
  .read-more {
    display: inline-block;
    margin-top: var(--spacing-sm);
    font-size: var(--font-size-sm);
    color: var(--color-primary);
  }
  ```

### Step 5.3: 验证

- [ ] 首页文章卡片左侧显示彩色竖线，悬浮时轻微上移

### Step 5.4: 提交

- [ ] ```bash
  git add frontend/src/components/article/ArticleCard.vue frontend/src/styles/main.css
  git commit -m "feat: ArticleCard 彩色左边框 + 悬浮动效"
  ```

---

## Task 6: ArticleList + 骨架屏 + 空状态集成

**Files:**
- Modify: `frontend/src/components/article/ArticleList.vue`

### Step 6.1: 查看当前 ArticleList.vue

- [ ] 阅读 `frontend/src/components/article/ArticleList.vue`，了解当前 loading/error 处理方式

### Step 6.2: 集成 SkeletonLoader 和 EmptyState

- [ ] 在 `ArticleList.vue` 中：
  - 添加 import：`import SkeletonLoader from '@/components/common/SkeletonLoader.vue'`
  - 添加 import：`import EmptyState from '@/components/common/EmptyState.vue'`
  - 将 `v-if="loading"` 的占位内容替换为 `<SkeletonLoader :lines="4" />`
  - 将空列表时的"暂无文章"替换为 `<EmptyState title="暂无文章" description="还没有任何文章，敬请期待" />`

### Step 6.3: 验证

- [ ] 刷新首页，观察加载过程中的骨架屏动画

### Step 6.4: 提交

- [ ] ```bash
  git add frontend/src/components/article/ArticleList.vue
  git commit -m "feat: ArticleList 接入骨架屏和空状态组件"
  ```

---

## Task 7: ArticleView 升级（Hero + Vditor 主题 + 代码复制）

**Files:**
- Modify: `frontend/src/views/public/ArticleView.vue`

### Step 7.1: 重写 ArticleView

- [ ] 将 `frontend/src/views/public/ArticleView.vue` 完整替换为：

  ```vue
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
  ```

### Step 7.2: 验证

- [ ] 打开任意文章详情页，确认顶部有大标题 + meta + 分隔线
- [ ] 代码块悬浮时出现"复制"按钮，点击后变为"已复制!"
- [ ] 切换深色/浅色主题，Vditor 内容随之切换主题

### Step 7.3: 提交

- [ ] ```bash
  git add frontend/src/views/public/ArticleView.vue
  git commit -m "feat: ArticleView Hero 区 + Vditor 主题同步 + 代码复制按钮"
  ```

---

## Task 8: 侧边栏组件视觉升级

**Files:**
- Modify: `frontend/src/components/article/CategoryFilter.vue`
- Modify: `frontend/src/components/search/SearchBar.vue`
- Modify: `frontend/src/components/common/AppFooter.vue`

### Step 8.1: 升级 CategoryFilter

- [ ] 阅读当前 `frontend/src/components/article/CategoryFilter.vue`
- [ ] 在 `<style>` 中添加/覆盖样式，实现列表样式 + active 左边框高亮：
  - `.category-btn` 改为 `display: flex; justify-content: space-between; align-items: center; width: 100%; padding: 0.5rem 0.75rem; border-radius: var(--radius-sm); border: none; background: none; color: var(--color-text-muted); cursor: pointer; text-align: left; border-left: 3px solid transparent; transition: all 0.15s;`
  - `.category-btn.active` 加 `border-left-color: var(--color-primary); background: var(--color-bg-hover); color: var(--color-text);`
  - 分类数量徽章：`margin-left: auto; font-size: 0.75rem; color: var(--color-text-muted); background: var(--color-bg-hover); padding: 1px 6px; border-radius: 9999px;`

### Step 8.2: 升级 SearchBar

- [ ] 阅读当前 `frontend/src/components/search/SearchBar.vue`
- [ ] 在 `<style>` 中更新 input 样式：
  - `border-radius: 8px`
  - `border: 1px solid var(--color-border)`
  - `background: var(--color-bg-hover)`
  - `transition: border-color 0.15s, box-shadow 0.15s`
  - `&:focus { outline: none; border-color: var(--color-primary); box-shadow: 0 0 0 3px rgba(88,166,255,0.15); }`

### Step 8.3: 简化 AppFooter

- [ ] 阅读当前 `frontend/src/components/common/AppFooter.vue`
- [ ] 确认 footer 样式：单行居中，`color: var(--color-text-muted)`，`font-size: var(--font-size-sm)`，`border-top: 1px solid var(--color-border)`

### Step 8.4: 提交

- [ ] ```bash
  git add frontend/src/components/article/CategoryFilter.vue \
        frontend/src/components/search/SearchBar.vue \
        frontend/src/components/common/AppFooter.vue
  git commit -m "feat: 侧边栏组件视觉升级，SearchBar 聚焦样式，CategoryFilter 列表样式"
  ```

---

## Task 9: 管理后台升级

**Files:**
- Modify: `frontend/src/views/admin/ArticleListView.vue`
- Modify: `frontend/src/views/admin/ArticleEditView.vue`
- Modify: `frontend/src/views/admin/LoginView.vue`

### Step 9.1: 升级 ArticleListView

- [ ] 修改 `frontend/src/views/admin/ArticleListView.vue`：

  1. 在 `<script setup>` 顶部添加：
     ```typescript
     import { useConfirm } from '@/composables/useConfirm'
     import { useToastStore } from '@/stores/toast'
     const { confirm } = useConfirm()
     const toastStore = useToastStore()
     ```

  2. 将 `handleDelete` 改为：
     ```typescript
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
     ```

  3. 在 `<template>` 中：
     - 加载状态改为 `<SkeletonLoader :lines="5" />`（添加 import）
     - 编辑按钮改为 SVG 图标按钮，删除按钮改为 SVG 图标按钮
     - 表格 `<tbody>` 中每行加 `:class="{ 'row-even': index % 2 === 1 }"`

  4. 在 `<style>` 中添加：
     ```css
     .article-table tbody tr:nth-child(even) { background: var(--color-bg-hover); }
     .article-table tbody tr:hover { background: var(--color-bg-hover); }
     .icon-action-btn {
       width: 32px; height: 32px; border-radius: var(--radius-sm);
       background: none; border: none; cursor: pointer;
       color: var(--color-text-muted); display: inline-flex;
       align-items: center; justify-content: center;
       transition: background 0.15s, color 0.15s;
     }
     .icon-action-btn:hover { background: var(--color-bg-hover); color: var(--color-text); }
     .icon-action-btn.delete:hover { color: var(--color-danger); }
     ```

### Step 9.2: 升级 ArticleEditView

- [ ] 阅读当前 `frontend/src/views/admin/ArticleEditView.vue`
- [ ] 在 `<script setup>` 顶部添加 toast store import：
  ```typescript
  import { useToastStore } from '@/stores/toast'
  const toastStore = useToastStore()
  ```
- [ ] 在提交成功后添加：
  ```typescript
  toastStore.add(isEdit ? '文章已更新' : '文章已发布', 'success')
  ```
- [ ] 在 `<template>` 底部的提交按钮区域，将其改为 sticky 底部操作栏：
  ```html
  <div class="form-actions">
    <button type="button" class="btn" @click="router.back()">取消</button>
    <button type="submit" class="btn btn-primary" :disabled="saving">
      {{ saving ? '保存中...' : '保存' }}
    </button>
  </div>
  ```
  ```css
  .form-actions {
    position: sticky;
    bottom: 0;
    background: var(--color-bg);
    border-top: 1px solid var(--color-border);
    padding: 1rem;
    display: flex;
    justify-content: flex-end;
    gap: 0.5rem;
    margin: 0 -1rem -1rem;
  }
  ```

### Step 9.3: 升级 LoginView

- [ ] 阅读当前 `frontend/src/views/admin/LoginView.vue`
- [ ] 确认 `login-card` 已有基本卡片样式，只需添加：
  - 卡片顶部加 Logo + 博客名（与 AppHeader Logo 保持一致风格）
  - 登录失败时调用 `toastStore.add('登录失败，请检查用户名和密码', 'error')` 而非只显示 inline error
  - 添加 import：`import { useToastStore } from '@/stores/toast'`

### Step 9.4: 验证

- [ ] 访问 `/admin/articles`，确认删除时弹出 ConfirmModal 而非浏览器 confirm
- [ ] 确认删除成功后右下角出现 Toast 通知
- [ ] 访问 `/admin/articles/new`，确认底部有固定操作栏

### Step 9.5: 提交

- [ ] ```bash
  git add frontend/src/views/admin/ArticleListView.vue \
        frontend/src/views/admin/ArticleEditView.vue \
        frontend/src/views/admin/LoginView.vue
  git commit -m "feat: 管理后台升级，ConfirmModal 删除确认 + Toast 通知 + sticky 操作栏"
  ```

---

## Task 10: 移动端响应式优化

**Files:**
- Modify: `frontend/src/views/public/HomeView.vue`
- Modify: `frontend/src/styles/main.css`
- Modify: `frontend/src/views/admin/ArticleListView.vue`

### Step 10.1: 阅读 HomeView.vue

- [ ] 阅读 `frontend/src/views/public/HomeView.vue`，了解当前侧边栏和内容区布局

### Step 10.2: HomeView 移动端侧边栏折叠

- [ ] 在 `HomeView.vue` 中添加折叠状态：
  ```typescript
  const sidebarOpen = ref(false)
  ```
- [ ] 在模板中，移动端显示折叠按钮 + 用 `v-show="sidebarOpen || isDesktop"` 控制侧边栏显隐
- [ ] 添加 `isDesktop` 计算属性（通过 `window.innerWidth >= 1024` 或 `matchMedia`）

### Step 10.3: main.css 全局移动端调整

- [ ] 在 `frontend/src/styles/main.css` 底部添加：
  ```css
  /* 移动端通用触摸区域 */
  @media (max-width: 639px) {
    button, .btn, a.btn { min-height: 44px; }
    .main-content { padding: var(--spacing-md) var(--spacing-sm); }
  }
  ```

### Step 10.4: ArticleListView 移动端卡片布局

- [ ] 在 `ArticleListView.vue` 中添加移动端卡片视图：
  ```html
  <!-- 移动端：卡片列表 -->
  <div class="article-cards-mobile">
    <div v-for="article in result.items" :key="article.id" class="admin-article-card">
      <div class="admin-card-main">
        <span class="admin-card-title">{{ article.title }}</span>
        <span class="admin-card-category">{{ article.category?.name ?? '未分类' }}</span>
      </div>
      <div class="admin-card-right">
        <span :class="article.is_published ? 'badge-published' : 'badge-draft'">
          {{ article.is_published ? '已发布' : '草稿' }}
        </span>
        <span class="admin-card-date">{{ formatDate(article.created_at) }}</span>
        <!-- 操作按钮 -->
      </div>
    </div>
  </div>
  ```

  控制显示：
  ```css
  .article-table { display: table; }
  .article-cards-mobile { display: none; }
  
  @media (max-width: 639px) {
    .article-table { display: none; }
    .article-cards-mobile { display: flex; flex-direction: column; gap: 0.75rem; }
    /* 卡片样式 */
    .admin-article-card {
      display: flex; justify-content: space-between; align-items: center;
      padding: 0.75rem 1rem; background: var(--color-bg-secondary);
      border: 1px solid var(--color-border); border-radius: var(--radius-md);
    }
  }
  ```

### Step 10.5: 验证

- [ ] DevTools 切换到手机视图（375px），首页侧边栏消失/折叠
- [ ] 管理后台文章列表在手机视图显示为卡片
- [ ] 所有按钮触摸区域 >= 44px

### Step 10.6: 提交

- [ ] ```bash
  git add frontend/src/views/public/HomeView.vue \
        frontend/src/styles/main.css \
        frontend/src/views/admin/ArticleListView.vue
  git commit -m "feat: 移动端优先响应式优化，侧边栏折叠 + 管理表格卡片化"
  ```

---

## Task 11: 最终检查 + 整理

### Step 11.1: TypeScript 编译检查

- [ ] ```bash
  cd C:/Users/choub/Desktop/python/Xiaotangblog/frontend
  npm run build
  ```
  预期：无 TypeScript 编译错误，build 成功。

### Step 11.2: 全功能回归测试

- [ ] 访问首页：骨架屏 → 文章列表 → 分类筛选 → 搜索
- [ ] 访问文章详情：Hero 区 → 正文 → 代码复制 → 点赞 → 评论
- [ ] 访问搜索页：搜索 → 分页
- [ ] 访问管理后台：登录 → 文章列表（ConfirmModal 删除）→ 编辑文章（sticky 操作栏）
- [ ] 切换主题：深色 ↔ 浅色，Vditor 内容同步切换
- [ ] 移动端（375px）：所有页面布局正常，导航可用

### Step 11.3: 最终提交

- [ ] ```bash
  git add .
  git commit -m "chore: 前端优化收尾，完成全功能验证"
  ```
