<template>
  <div class="mgr-shell">
    <div class="grain" aria-hidden="true"></div>

    <!-- ── left: category panel ── -->
    <aside class="cat-panel">
      <header class="cat-panel__head">
        <span class="cat-panel__label">CATEGORIES</span>
      </header>

      <nav class="cat-list">
        <!-- 全部 -->
        <button
          class="cat-item"
          :class="{ 'cat-item--active': selectedCategoryId === null }"
          @click="selectCategory(null)"
        >
          <span class="cat-item__name">全部文章</span>
          <span class="cat-item__count">{{ totalCount }}</span>
        </button>

        <!-- 各分类 -->
        <div
          v-for="cat in categories"
          :key="cat.id"
          class="cat-item-wrap"
        >
          <!-- view mode -->
          <button
            v-if="editingCatId !== cat.id"
            class="cat-item"
            :class="{ 'cat-item--active': selectedCategoryId === cat.id }"
            @click="selectCategory(cat.id)"
          >
            <span class="cat-item__name">{{ cat.name }}</span>
            <span class="cat-item__count">{{ cat.article_count }}</span>
            <span class="cat-item__actions">
              <button class="cat-icon-btn" title="编辑" @click.stop="startEditCat(cat)">
                <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                  <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
                  <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
                </svg>
              </button>
              <button class="cat-icon-btn cat-icon-btn--danger" title="删除" @click.stop="handleDeleteCat(cat.id, cat.name)">
                <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                  <polyline points="3 6 5 6 21 6"/>
                  <path d="M19 6l-1 14H6L5 6"/>
                  <path d="M10 11v6"/><path d="M14 11v6"/>
                  <path d="M9 6V4h6v2"/>
                </svg>
              </button>
            </span>
          </button>

          <!-- inline edit mode -->
          <form v-else class="cat-inline-form" @submit.prevent="saveEditCat(cat.id)">
            <input
              v-model="editForm.name"
              class="cat-input"
              placeholder="分类名称"
              required
              autofocus
            />
            <div class="cat-inline-actions">
              <button type="submit" class="cat-save-btn">保存</button>
              <button type="button" class="cat-cancel-btn" @click="cancelEdit">取消</button>
            </div>
          </form>
        </div>
      </nav>

      <!-- new category form -->
      <div class="cat-new-wrap">
        <button
          v-if="!showNewForm"
          class="cat-new-trigger"
          @click="showNewForm = true"
        >
          <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
            <line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/>
          </svg>
          新建分类
        </button>
        <form v-else class="cat-new-form" @submit.prevent="handleCreateCat">
          <input
            v-model="newCatName"
            class="cat-input"
            placeholder="分类名称"
            required
            autofocus
          />
          <div class="cat-inline-actions">
            <button type="submit" class="cat-save-btn" :disabled="savingCat">
              {{ savingCat ? '…' : '创建' }}
            </button>
            <button type="button" class="cat-cancel-btn" @click="showNewForm = false; newCatName = ''">
              取消
            </button>
          </div>
        </form>
      </div>
    </aside>

    <!-- ── right: article panel ── -->
    <main class="art-panel">
      <header class="art-panel__head">
        <div class="art-panel__title">
          <span class="art-panel__label">ARTICLES</span>
          <h1 class="art-panel__heading">
            {{ selectedCategoryId === null ? '全部文章' : (selectedCatName ?? '文章管理') }}
          </h1>
        </div>
        <RouterLink to="/admin/articles/new" class="new-art-btn">
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
            <line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/>
          </svg>
          撰写新文章
        </RouterLink>
      </header>

      <!-- mobile category chips (hidden on desktop) -->
      <div class="cat-chips">
        <button
          class="cat-chip"
          :class="{ 'cat-chip--active': selectedCategoryId === null }"
          @click="selectCategory(null)"
        >全部</button>
        <button
          v-for="cat in categories"
          :key="cat.id"
          class="cat-chip"
          :class="{ 'cat-chip--active': selectedCategoryId === cat.id }"
          @click="selectCategory(cat.id)"
        >{{ cat.name }}</button>
      </div>

      <!-- table area -->
      <div class="art-table-wrap">
        <SkeletonLoader v-if="loading" :lines="6" />

        <template v-else-if="result && result.items.length > 0">
          <table class="art-table">
            <thead>
              <tr>
                <th>标题</th>
                <th class="col-cat">分类</th>
                <th class="col-status">状态</th>
                <th class="col-date">日期</th>
                <th class="col-actions"></th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="(article, idx) in result.items"
                :key="article.id"
                :style="{ '--row-delay': `${idx * 0.04}s` }"
                class="art-row"
              >
                <td class="col-title">
                  <span class="art-title">{{ article.title }}</span>
                </td>
                <td class="col-cat">
                  <span class="art-cat-tag">{{ article.category?.name ?? '未分类' }}</span>
                </td>
                <td class="col-status">
                  <span class="status-dot" :class="article.is_published ? 'status-dot--pub' : 'status-dot--draft'">
                    {{ article.is_published ? 'LIVE' : 'DRAFT' }}
                  </span>
                </td>
                <td class="col-date">{{ formatDate(article.created_at) }}</td>
                <td class="col-actions">
                  <RouterLink :to="`/admin/articles/${article.id}/edit`" class="row-btn" title="编辑">
                    <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
                      <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
                    </svg>
                  </RouterLink>
                  <button class="row-btn row-btn--del" @click="handleDelete(article.id)" title="删除">
                    <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <polyline points="3 6 5 6 21 6"/>
                      <path d="M19 6l-1 14H6L5 6"/>
                      <path d="M10 11v6"/><path d="M14 11v6"/>
                      <path d="M9 6V4h6v2"/>
                    </svg>
                  </button>
                </td>
              </tr>
            </tbody>
          </table>

          <AppPagination
            v-if="result.total_pages > 1"
            :current-page="page"
            :total-pages="result.total_pages"
            @change="page = $event"
          />
        </template>

        <div v-else-if="result" class="art-empty">
          <span class="art-empty__icon">◌</span>
          <p class="art-empty__msg">该分类下暂无文章</p>
          <RouterLink to="/admin/articles/new" class="new-art-btn">撰写第一篇</RouterLink>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import { articlesApi } from '@/api/articles'
import { categoriesApi } from '@/api/categories'
import AppPagination from '@/components/common/AppPagination.vue'
import SkeletonLoader from '@/components/common/SkeletonLoader.vue'
import type { Paginated } from '@/types/api'
import type { ArticleSummary } from '@/types/article'
import type { Category } from '@/types/category'
import { useConfirm } from '@/composables/useConfirm'
import { useToastStore } from '@/stores/toast'

const { confirm } = useConfirm()
const toastStore = useToastStore()

// ── categories ──────────────────────────────────────────
const categories = ref<Category[]>([])
const selectedCategoryId = ref<number | null>(null)
const showNewForm = ref(false)
const newCatName = ref('')
const savingCat = ref(false)
const editingCatId = ref<number | null>(null)
const editForm = ref({ name: '', slug: '' })

const selectedCatName = computed(
  () => categories.value.find((c) => c.id === selectedCategoryId.value)?.name,
)

const totalCount = computed(() =>
  categories.value.reduce((acc, c) => acc + c.article_count, 0),
)

async function loadCategories() {
  const res = await categoriesApi.list()
  categories.value = res.data.data ?? []
}

function selectCategory(id: number | null) {
  selectedCategoryId.value = id
  page.value = 1
}

function generateSlug(name: string): string {
  const latin = name.toLowerCase().replace(/\s+/g, '-').replace(/[^a-z0-9-]/g, '')
  return latin.length >= 2 ? latin : `cat-${Date.now()}`
}

async function handleCreateCat() {
  if (!newCatName.value.trim()) return
  savingCat.value = true
  try {
    await categoriesApi.create({
      name: newCatName.value.trim(),
      slug: generateSlug(newCatName.value.trim()),
    })
    toastStore.add(`分类「${newCatName.value}」已创建`, 'success')
    newCatName.value = ''
    showNewForm.value = false
    await loadCategories()
  } catch {
    toastStore.add('创建失败', 'error')
  } finally {
    savingCat.value = false
  }
}

function startEditCat(cat: Category) {
  editingCatId.value = cat.id
  editForm.value = { name: cat.name, slug: cat.slug }
}

function cancelEdit() {
  editingCatId.value = null
}

async function saveEditCat(id: number) {
  if (!editForm.value.name.trim()) return
  try {
    await categoriesApi.update(id, {
      name: editForm.value.name.trim(),
      slug: generateSlug(editForm.value.name.trim()),
    })
    toastStore.add('分类已更新', 'success')
    editingCatId.value = null
    await loadCategories()
  } catch {
    toastStore.add('更新失败', 'error')
  }
}

async function handleDeleteCat(id: number, name: string) {
  const ok = await confirm({
    title: '删除分类',
    message: `删除「${name}」后，该分类下的文章将变为未分类。确认删除？`,
    confirmText: '删除',
  })
  if (!ok) return
  try {
    await categoriesApi.delete(id)
    toastStore.add('分类已删除', 'success')
    if (selectedCategoryId.value === id) selectCategory(null)
    await loadCategories()
  } catch {
    toastStore.add('删除失败', 'error')
  }
}

// ── articles ─────────────────────────────────────────────
const page = ref(1)
const result = ref<Paginated<ArticleSummary> | null>(null)
const loading = ref(false)

async function loadArticles() {
  loading.value = true
  try {
    const res = await articlesApi.list({
      page: page.value,
      page_size: 20,
      category_id: selectedCategoryId.value ?? undefined,
    })
    result.value = res.data
  } finally {
    loading.value = false
  }
}

watch([page, selectedCategoryId], loadArticles, { immediate: true })

async function handleDelete(id: number) {
  const ok = await confirm({
    title: '确认删除',
    message: '删除后无法恢复，确认删除此文章？',
    confirmText: '删除',
  })
  if (!ok) return
  await articlesApi.delete(id)
  toastStore.add('文章已删除', 'success')
  await loadArticles()
}

function formatDate(iso: string): string {
  return new Date(iso).toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
  })
}

onMounted(loadCategories)
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Crimson+Pro:ital,wght@0,300;0,400;0,600;1,300&family=IBM+Plex+Mono:wght@400;500&display=swap');

/* ── root ── */
.mgr-shell {
  --ink: #0d0d0d;
  --paper: #f2ede4;
  --amber: #c8863a;
  --smoke: #181818;
  --dim: #0a0a0a;
  --line: rgba(242, 237, 228, 0.08);
  --muted: rgba(242, 237, 228, 0.38);
  --active-bg: rgba(200, 134, 58, 0.1);

  position: relative;
  display: grid;
  grid-template-columns: 210px 1fr;
  min-height: calc(100vh - 60px);
  background: var(--ink);
  color: var(--paper);
  font-family: 'IBM Plex Mono', monospace;
}

/* grain */
.grain {
  pointer-events: none;
  position: fixed;
  inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 512 512' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.75' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
  opacity: 0.03;
  z-index: 0;
}

/* ── left: category panel ── */
.cat-panel {
  position: sticky;
  top: 0;
  height: 100vh;
  overflow-y: auto;
  scrollbar-width: none;
  z-index: 1;
  background: var(--dim);
  border-right: 1px solid var(--line);
  display: flex;
  flex-direction: column;
}
.cat-panel::-webkit-scrollbar { display: none; }

.cat-panel__head {
  padding: 2rem 1.25rem 1rem;
  border-bottom: 1px solid var(--line);
  flex-shrink: 0;
}

.cat-panel__label {
  font-size: 0.55rem;
  letter-spacing: 0.28em;
  color: var(--amber);
}

/* category list */
.cat-list {
  flex: 1;
  padding: 0.5rem 0;
}

.cat-item-wrap { position: relative; }

.cat-item {
  width: 100%;
  display: flex;
  align-items: center;
  padding: 0.6rem 1.25rem;
  background: none;
  border: none;
  cursor: pointer;
  color: var(--muted);
  font-family: 'IBM Plex Mono', monospace;
  font-size: 0.7rem;
  text-align: left;
  transition: color 0.15s, background 0.15s;
  position: relative;
  gap: 0;
}

.cat-item:hover { color: var(--paper); background: rgba(242, 237, 228, 0.04); }

.cat-item--active {
  color: var(--amber) !important;
  background: var(--active-bg) !important;
}

.cat-item--active::before {
  content: '';
  position: absolute;
  left: 0;
  top: 22%;
  bottom: 22%;
  width: 2px;
  background: var(--amber);
}

.cat-item__name {
  flex: 1;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.cat-item__count {
  font-size: 0.58rem;
  color: var(--muted);
  margin-left: 0.4rem;
  flex-shrink: 0;
}

.cat-item--active .cat-item__count { color: rgba(200, 134, 58, 0.7); }

/* hover actions on category row */
.cat-item__actions {
  display: none;
  gap: 1px;
  margin-left: 0.25rem;
  flex-shrink: 0;
}

.cat-item-wrap:hover .cat-item__actions,
.cat-item--active .cat-item__actions { display: flex; }

.cat-icon-btn {
  width: 20px;
  height: 20px;
  background: none;
  border: none;
  cursor: pointer;
  color: rgba(242, 237, 228, 0.25);
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 2px;
  transition: color 0.15s, background 0.15s;
  padding: 0;
}
.cat-icon-btn:hover { color: var(--paper); background: rgba(242,237,228,0.08); }
.cat-icon-btn--danger:hover { color: #c0392b; }

/* inline forms */
.cat-inline-form,
.cat-new-form {
  padding: 0.5rem 1.25rem;
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.cat-input {
  background: rgba(242, 237, 228, 0.04);
  border: 1px solid var(--line);
  color: var(--paper);
  font-family: 'IBM Plex Mono', monospace;
  font-size: 0.7rem;
  padding: 0.4rem 0.6rem;
  outline: none;
  width: 100%;
  box-sizing: border-box;
  transition: border-color 0.18s;
  border-radius: 0;
}
.cat-input:focus { border-color: var(--amber); }
.cat-input::placeholder { color: rgba(242,237,228,0.2); }

.cat-inline-actions {
  display: flex;
  gap: 0.35rem;
}

.cat-save-btn {
  flex: 1;
  background: var(--amber);
  color: var(--ink);
  border: none;
  font-family: 'IBM Plex Mono', monospace;
  font-size: 0.62rem;
  letter-spacing: 0.08em;
  padding: 0.35rem 0;
  cursor: pointer;
  transition: opacity 0.15s;
}
.cat-save-btn:disabled { opacity: 0.45; cursor: not-allowed; }
.cat-save-btn:not(:disabled):hover { opacity: 0.82; }

.cat-cancel-btn {
  background: none;
  border: 1px solid var(--line);
  color: var(--muted);
  font-family: 'IBM Plex Mono', monospace;
  font-size: 0.62rem;
  padding: 0.35rem 0.6rem;
  cursor: pointer;
  transition: color 0.15s;
}
.cat-cancel-btn:hover { color: var(--paper); }

/* new category trigger */
.cat-new-wrap {
  padding: 0.9rem 1.25rem;
  border-top: 1px solid var(--line);
  margin-top: auto;
  flex-shrink: 0;
}

.cat-new-trigger {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: none;
  border: none;
  color: var(--muted);
  font-family: 'IBM Plex Mono', monospace;
  font-size: 0.62rem;
  letter-spacing: 0.12em;
  cursor: pointer;
  padding: 0.3rem 0;
  transition: color 0.15s;
  width: 100%;
}
.cat-new-trigger:hover { color: var(--amber); }

/* ── right: article panel ── */
.art-panel {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  min-height: 0;
}

.art-panel__head {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  padding: 2rem 2rem 1.25rem;
  border-bottom: 1px solid var(--line);
  flex-shrink: 0;
}

.art-panel__label {
  display: block;
  font-size: 0.55rem;
  letter-spacing: 0.28em;
  color: var(--amber);
  margin-bottom: 0.3rem;
}

.art-panel__heading {
  font-family: 'Crimson Pro', serif;
  font-size: 1.8rem;
  font-weight: 300;
  font-style: italic;
  letter-spacing: -0.02em;
  margin: 0;
  line-height: 1;
}

.new-art-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background: var(--amber);
  color: var(--ink);
  text-decoration: none;
  font-family: 'IBM Plex Mono', monospace;
  font-size: 0.62rem;
  letter-spacing: 0.1em;
  padding: 0.5rem 0.9rem;
  border: none;
  cursor: pointer;
  transition: opacity 0.15s;
  white-space: nowrap;
  flex-shrink: 0;
}
.new-art-btn:hover { opacity: 0.82; }

/* mobile chips */
.cat-chips { display: none; }

/* article table wrapper */
.art-table-wrap {
  flex: 1;
  padding: 0 2rem 2rem;
  overflow-x: auto;
}

.art-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1.5rem;
}

.art-table thead tr { border-bottom: 1px solid var(--line); }

.art-table th {
  font-size: 0.52rem;
  letter-spacing: 0.22em;
  color: var(--amber);
  text-align: left;
  padding: 0 1rem 0.7rem 0;
  font-weight: 400;
}

.art-row {
  border-bottom: 1px solid var(--line);
  animation: row-in 0.3s cubic-bezier(0.22, 1, 0.36, 1) both;
  animation-delay: var(--row-delay, 0s);
  transition: background 0.12s;
}
.art-row:hover { background: rgba(242, 237, 228, 0.03); }

@keyframes row-in {
  from { opacity: 0; transform: translateY(5px); }
  to   { opacity: 1; transform: translateY(0); }
}

.art-table td {
  padding: 0.8rem 1rem 0.8rem 0;
  font-size: 0.72rem;
  color: var(--paper);
  vertical-align: middle;
}

.art-title {
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
  font-size: 0.78rem;
}

.art-cat-tag {
  font-size: 0.58rem;
  letter-spacing: 0.1em;
  color: var(--muted);
  border: 1px solid var(--line);
  padding: 2px 6px;
}

.status-dot {
  font-size: 0.52rem;
  letter-spacing: 0.16em;
  padding: 3px 7px;
}
.status-dot--pub   { color: #5db97c; background: rgba(93, 185, 124, 0.1); }
.status-dot--draft { color: var(--muted); background: rgba(242, 237, 228, 0.04); }

.col-cat     { width: 100px; }
.col-status  { width: 76px; }
.col-date    { width: 96px; }
.col-date td { color: var(--muted) !important; font-size: 0.62rem !important; }
.col-actions { width: 64px; text-align: right; }

.row-btn {
  width: 28px;
  height: 28px;
  background: none;
  border: none;
  cursor: pointer;
  color: rgba(242, 237, 228, 0.28);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 2px;
  text-decoration: none;
  transition: color 0.15s, background 0.15s;
}
.row-btn:hover { color: var(--paper); background: rgba(242,237,228,0.07); }
.row-btn--del:hover { color: #c0392b; }

/* empty */
.art-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  padding: 5rem 0;
  color: var(--muted);
}
.art-empty__icon { font-size: 2.5rem; opacity: 0.25; }
.art-empty__msg  { font-size: 0.7rem; letter-spacing: 0.1em; margin: 0; }

/* ── responsive ── */
@media (max-width: 760px) {
  .mgr-shell { grid-template-columns: 1fr; }
  .cat-panel { display: none; }

  .cat-chips {
    display: flex;
    gap: 5px;
    overflow-x: auto;
    scrollbar-width: none;
    padding: 0.75rem 1rem;
    border-bottom: 1px solid var(--line);
    flex-shrink: 0;
  }
  .cat-chips::-webkit-scrollbar { display: none; }

  .cat-chip {
    flex-shrink: 0;
    background: none;
    border: 1px solid var(--line);
    color: var(--muted);
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 0.1em;
    padding: 0.3rem 0.65rem;
    cursor: pointer;
    transition: color 0.15s, border-color 0.15s;
  }
  .cat-chip--active { color: var(--amber); border-color: var(--amber); }

  .art-panel__head { padding: 1.25rem 1rem 1rem; }
  .art-table-wrap { padding: 0 1rem 2rem; }
  .col-cat, .col-date { display: none; }
}
</style>
