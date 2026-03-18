<template>
  <div class="edit-view">
    <div class="grain" aria-hidden="true"></div>

    <!-- top bar -->
    <header class="edit-header">
      <div class="edit-meta">
        <span class="edit-label">{{ isEdit ? 'EDITING' : 'NEW ARTICLE' }}</span>
        <span v-if="lastSavedText" class="draft-status">
          <span class="draft-dot"></span>{{ lastSavedText }}
        </span>
      </div>
      <div class="edit-header-actions">
        <button type="button" class="ghost-btn" @click="triggerMdImport">
          ↑ 导入 .md
        </button>
        <input ref="mdFileInput" type="file" accept=".md" hidden @change="handleMdImport" />
      </div>
    </header>

    <form @submit.prevent="handleSubmit" class="edit-form">
      <!-- title — large display -->
      <div class="title-field">
        <input
          v-model="form.title"
          type="text"
          placeholder="文章标题…"
          required
          maxlength="300"
          class="title-input"
          autocomplete="off"
          spellcheck="false"
        />
      </div>

      <!-- meta row -->
      <div class="meta-row">
        <div class="meta-field">
          <label class="meta-label">SLUG</label>
          <input
            v-model="form.slug"
            type="text"
            required
            pattern="[a-z0-9-]+"
            placeholder="url-slug（将根据标题自动生成）"
            class="meta-input"
            autocomplete="off"
            spellcheck="false"
            @input="slugManuallyEdited = true"
          />
        </div>
        <div class="meta-field">
          <label class="meta-label">CATEGORY</label>
          <select v-model="form.category_id" class="meta-select">
            <option :value="null">未分类</option>
            <option v-for="cat in categories" :key="cat.id" :value="cat.id">
              {{ cat.name }}
            </option>
          </select>
        </div>
        <div class="meta-field meta-field--publish">
          <label class="publish-toggle" :class="{ active: form.is_published }">
            <input v-model="form.is_published" type="checkbox" hidden />
            <span class="toggle-track">
              <span class="toggle-dot"></span>
            </span>
            <span class="toggle-label">{{ form.is_published ? 'PUBLISHED' : 'DRAFT' }}</span>
          </label>
        </div>
      </div>

      <!-- excerpt -->
      <div class="excerpt-field">
        <label class="meta-label">EXCERPT</label>
        <textarea
          v-model="form.excerpt"
          maxlength="500"
          rows="2"
          placeholder="文章摘要（选填）…"
          class="excerpt-input"
        />
      </div>

      <!-- editor -->
      <div class="editor-wrap">
        <label class="meta-label editor-label">CONTENT</label>
        <div id="vditor-editor" class="vditor-host"></div>
      </div>

      <!-- error -->
      <p v-if="error" class="field-error">⚠ {{ error }}</p>

      <!-- sticky footer -->
      <div class="form-footer">
        <button type="button" class="footer-btn footer-btn--ghost" @click="router.back()">
          取消
        </button>
        <button type="submit" class="footer-btn footer-btn--primary" :disabled="saving">
          <span v-if="saving" class="saving-dots">
            <span></span><span></span><span></span>
          </span>
          <span v-else>保存文章</span>
        </button>
      </div>
    </form>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import Vditor from 'vditor'
import 'vditor/dist/index.css'
import { articlesApi } from '@/api/articles'
import { categoriesApi } from '@/api/categories'
import type { Category } from '@/types/category'
import { useToastStore } from '@/stores/toast'
import { useDraftSave } from '@/composables/useDraftSave'

const toastStore = useToastStore()
const route = useRoute()
const router = useRouter()

const isEdit = !!route.params.id
const draftKey = isEdit ? `draft-article-${route.params.id}` : 'draft-article-new'
const { save: saveDraft, load: loadDraft, clear: clearDraft, startAutoSave, lastSavedText } =
  useDraftSave(draftKey)

const saving = ref(false)
const error = ref<string | null>(null)
const categories = ref<Category[]>([])
const mdFileInput = ref<HTMLInputElement | null>(null)
let vditor: Vditor | null = null

const form = reactive({
  title: '',
  slug: '',
  content: '',
  excerpt: '',
  category_id: null as number | null,
  is_published: false,
})

// 自动生成 slug：将标题转换为 URL 友好格式
// 新建模式下，若 slug 未被手动编辑则跟随标题自动变化
let slugManuallyEdited = false

function generateSlug(title: string): string {
  const latin = title
    .toLowerCase()
    .replace(/[\s_]+/g, '-')          // 空格/下划线 → 连字符
    .replace(/[^a-z0-9-]/g, '')       // 去掉非 ASCII 字符
    .replace(/-{2,}/g, '-')           // 合并多个连字符
    .replace(/^-|-$/g, '')            // 去掉首尾连字符
  if (latin.length >= 3) return latin
  // 标题全是中文时用日期时间戳生成唯一 slug
  const now = new Date()
  return `article-${now.getFullYear()}${String(now.getMonth() + 1).padStart(2, '0')}${String(now.getDate()).padStart(2, '0')}`
}

if (!isEdit) {
  watch(
    () => form.title,
    (newTitle) => {
      if (!slugManuallyEdited) {
        form.slug = generateSlug(newTitle)
      }
    },
  )
}

onMounted(async () => {
  const catRes = await categoriesApi.list()
  categories.value = catRes.data.data ?? []

  const token = localStorage.getItem('access_token')
  vditor = new Vditor('vditor-editor', {
    height: 520,
    mode: 'wysiwyg',
    toolbarConfig: { pin: true },
    theme: 'dark',
    upload: {
      url: '/api/v1/upload/image',
      headers: token ? { Authorization: `Bearer ${token}` } : {},
      format(_files, responseText) {
        try {
          const res = JSON.parse(responseText)
          const url: string = res.data?.url ?? ''
          const fileName = url.split('/').pop() ?? 'image'
          return JSON.stringify({
            code: 0,
            data: { succMap: { [fileName]: url } },
          })
        } catch {
          return responseText
        }
      },
    },
    after: async () => {
      if (isEdit) {
        const id = Number(route.params.id)
        const res = await articlesApi.get(id)
        const article = res.data.data
        if (article) {
          form.title = article.title
          form.slug = article.slug
          form.excerpt = article.excerpt ?? ''
          form.category_id = article.category?.id ?? null
          form.is_published = article.is_published
          vditor?.setValue(article.content)
        }
      } else {
        const draft = loadDraft<typeof form & { content: string }>()
        if (draft) {
          const restore = confirm('检测到未提交的草稿，是否恢复？')
          if (restore) {
            form.title = draft.title ?? ''
            form.slug = draft.slug ?? ''
            form.excerpt = draft.excerpt ?? ''
            form.category_id = draft.category_id ?? null
            form.is_published = draft.is_published ?? false
            vditor?.setValue(draft.content ?? '')
          }
        }
      }
      startAutoSave(() => ({ ...form, content: vditor?.getValue() ?? '' }))
    },
  })
})

function triggerMdImport(): void {
  mdFileInput.value?.click()
}

function handleMdImport(event: Event): void {
  const file = (event.target as HTMLInputElement).files?.[0]
  if (!file) return
  const reader = new FileReader()
  reader.onload = () => {
    vditor?.setValue(reader.result as string)
    toastStore.add('已导入 .md 文件', 'success')
  }
  reader.readAsText(file)
  ;(event.target as HTMLInputElement).value = ''
}

async function handleSubmit(): Promise<void> {
  saving.value = true
  error.value = null
  try {
    form.content = vditor?.getValue() ?? ''
    if (!form.content.trim()) {
      error.value = '正文不能为空'
      return
    }
    if (isEdit) {
      await articlesApi.update(Number(route.params.id), form)
    } else {
      await articlesApi.create(form)
    }
    clearDraft()
    toastStore.add(isEdit ? '文章已更新' : '文章已发布', 'success')
    router.push('/admin/articles')
  } catch {
    error.value = '保存失败，请检查输入'
  } finally {
    saving.value = false
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Crimson+Pro:ital,wght@0,300;0,400;0,600;1,300&family=IBM+Plex+Mono:wght@400;500&display=swap');

/* ── root ── */
.edit-view {
  --ink: #0d0d0d;
  --paper: #f2ede4;
  --amber: #c8863a;
  --smoke: #1a1a1a;
  --line: rgba(242, 237, 228, 0.1);
  --muted: rgba(242, 237, 228, 0.4);
  --danger: #b84c2b;

  position: relative;
  min-height: 100vh;
  background: var(--ink);
  color: var(--paper);
  font-family: 'IBM Plex Mono', monospace;
  padding: 2rem 2.5rem 6rem;
}

.grain {
  pointer-events: none;
  position: fixed;
  inset: -50%;
  width: 200%;
  height: 200%;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 512 512' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.75' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='1'/%3E%3C/svg%3E");
  opacity: 0.04;
  z-index: 0;
  animation: grain-drift 8s steps(1) infinite;
}

@keyframes grain-drift {
  0%   { transform: translate(0,0); }
  25%  { transform: translate(-2%,-2%); }
  50%  { transform: translate(2%,1%); }
  75%  { transform: translate(-1%,2%); }
  100% { transform: translate(0,0); }
}

/* ── header ── */
.edit-header {
  position: relative;
  z-index: 1;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid var(--line);
}

.edit-meta {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.edit-label {
  font-size: 0.6rem;
  letter-spacing: 0.25em;
  color: var(--amber);
}

.draft-status {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  font-size: 0.6rem;
  color: var(--muted);
  letter-spacing: 0.1em;
}

.draft-dot {
  width: 5px;
  height: 5px;
  border-radius: 50%;
  background: var(--amber);
  animation: blink 2s ease-in-out infinite;
}

@keyframes blink {
  0%, 100% { opacity: 1; }
  50%       { opacity: 0.2; }
}

.ghost-btn {
  background: none;
  border: 1px solid var(--line);
  color: var(--muted);
  font-family: inherit;
  font-size: 0.65rem;
  letter-spacing: 0.1em;
  padding: 0.4rem 0.8rem;
  cursor: pointer;
  transition: border-color 0.2s, color 0.2s;
}

.ghost-btn:hover {
  border-color: var(--amber);
  color: var(--amber);
}

/* ── form ── */
.edit-form {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  gap: 1.75rem;
}

/* title */
.title-field {
  border-bottom: 1px solid var(--line);
  padding-bottom: 0.5rem;
}

.title-input {
  width: 100%;
  background: transparent;
  border: none;
  outline: none;
  color: var(--paper);
  font-family: 'Crimson Pro', serif;
  font-size: clamp(1.8rem, 4vw, 3rem);
  font-style: italic;
  font-weight: 300;
  letter-spacing: -0.02em;
  padding: 0;
}

.title-input::placeholder {
  color: rgba(242, 237, 228, 0.2);
}

/* meta row */
.meta-row {
  display: flex;
  gap: 1.5rem;
  flex-wrap: wrap;
  align-items: flex-end;
}

.meta-field {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
  flex: 1;
  min-width: 140px;
}

.meta-field--publish {
  flex: 0 0 auto;
}

.meta-label {
  font-size: 0.55rem;
  letter-spacing: 0.2em;
  color: var(--amber);
}

.meta-input,
.meta-select {
  background: var(--smoke);
  border: 1px solid var(--line);
  color: var(--paper);
  font-family: 'IBM Plex Mono', monospace;
  font-size: 0.75rem;
  padding: 0.55rem 0.75rem;
  outline: none;
  transition: border-color 0.2s;
  appearance: none;
  -webkit-appearance: none;
  border-radius: 0;
}

.meta-input:focus,
.meta-select:focus {
  border-color: var(--amber);
}

.meta-input::placeholder {
  color: var(--muted);
}

/* toggle */
.publish-toggle {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  cursor: pointer;
  user-select: none;
  padding: 0.55rem 0;
}

.toggle-track {
  width: 32px;
  height: 18px;
  background: var(--smoke);
  border: 1px solid var(--line);
  border-radius: 9px;
  position: relative;
  transition: background 0.25s, border-color 0.25s;
}

.publish-toggle.active .toggle-track {
  background: var(--amber);
  border-color: var(--amber);
}

.toggle-dot {
  position: absolute;
  top: 2px;
  left: 2px;
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: var(--muted);
  transition: transform 0.25s cubic-bezier(0.4, 0, 0.2, 1), background 0.25s;
}

.publish-toggle.active .toggle-dot {
  transform: translateX(14px);
  background: var(--ink);
}

.toggle-label {
  font-size: 0.6rem;
  letter-spacing: 0.15em;
  color: var(--muted);
  transition: color 0.2s;
}

.publish-toggle.active .toggle-label {
  color: var(--amber);
}

/* excerpt */
.excerpt-input {
  background: var(--smoke);
  border: 1px solid var(--line);
  border-top: none;
  color: var(--paper);
  font-family: 'IBM Plex Mono', monospace;
  font-size: 0.75rem;
  padding: 0.75rem;
  resize: vertical;
  outline: none;
  display: block;
  width: 100%;
  box-sizing: border-box;
  transition: border-color 0.2s;
  border-radius: 0;
}

.excerpt-input:focus {
  border-color: var(--amber);
}

.excerpt-input::placeholder {
  color: var(--muted);
}

/* editor wrap */
.editor-wrap {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.editor-label {
  margin-bottom: 0;
}

/* override vditor for dark theme alignment */
.vditor-host :deep(.vditor) {
  border: 1px solid var(--line) !important;
  border-radius: 0 !important;
  background: var(--smoke) !important;
}

.vditor-host :deep(.vditor-toolbar) {
  background: #111 !important;
  border-bottom: 1px solid var(--line) !important;
}

/* error */
.field-error {
  font-size: 0.7rem;
  color: var(--danger);
  letter-spacing: 0.05em;
  margin: 0;
}

/* ── footer ── */
.form-footer {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  z-index: 100;
  display: flex;
  justify-content: flex-end;
  gap: 1px;
  background: var(--line);
  border-top: 1px solid var(--line);
}

.footer-btn {
  padding: 1rem 2rem;
  font-family: 'IBM Plex Mono', monospace;
  font-size: 0.7rem;
  letter-spacing: 0.15em;
  border: none;
  cursor: pointer;
  transition: background 0.18s, color 0.18s;
}

.footer-btn--ghost {
  background: var(--ink);
  color: var(--muted);
}

.footer-btn--ghost:hover {
  background: var(--smoke);
  color: var(--paper);
}

.footer-btn--primary {
  background: var(--amber);
  color: var(--ink);
  min-width: 120px;
}

.footer-btn--primary:hover:not(:disabled) {
  background: var(--paper);
  color: var(--ink);
}

.footer-btn--primary:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

/* saving dots */
.saving-dots {
  display: inline-flex;
  gap: 3px;
  align-items: center;
}

.saving-dots span {
  width: 4px;
  height: 4px;
  border-radius: 50%;
  background: var(--ink);
  animation: dot-bounce 1s ease-in-out infinite;
}

.saving-dots span:nth-child(2) { animation-delay: 0.15s; }
.saving-dots span:nth-child(3) { animation-delay: 0.30s; }

@keyframes dot-bounce {
  0%, 100% { transform: translateY(0); opacity: 0.5; }
  50%       { transform: translateY(-4px); opacity: 1; }
}

/* ── responsive ── */
@media (max-width: 600px) {
  .edit-view { padding: 1.5rem 1rem 5rem; }
  .meta-row  { flex-direction: column; gap: 1rem; }
  .meta-field { min-width: auto; }
  .footer-btn { padding: 1rem; }
}
</style>
