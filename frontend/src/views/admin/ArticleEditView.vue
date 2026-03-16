<template>
  <div class="article-edit-view">
    <h1>{{ isEdit ? '编辑文章' : '新建文章' }}</h1>

    <form @submit.prevent="handleSubmit" class="edit-form">
      <div class="field">
        <label>标题</label>
        <input v-model="form.title" type="text" required maxlength="300" />
      </div>
      <div class="field">
        <label>Slug（URL 标识）</label>
        <input v-model="form.slug" type="text" required pattern="[a-z0-9-]+" />
      </div>
      <div class="field">
        <label>摘要</label>
        <textarea v-model="form.excerpt" maxlength="500" rows="2" />
      </div>
      <div class="field">
        <label>分类</label>
        <select v-model="form.category_id">
          <option :value="null">未分类</option>
          <option v-for="cat in categories" :key="cat.id" :value="cat.id">
            {{ cat.name }}
          </option>
        </select>
      </div>
      <div class="field">
        <label>正文（Markdown）</label>
        <!-- Vditor 编辑器挂载点 -->
        <div id="vditor-editor"></div>
      </div>
      <div class="field-inline">
        <label>
          <input v-model="form.is_published" type="checkbox" />
          立即发布
        </label>
      </div>

      <p v-if="error" class="error">{{ error }}</p>
      <div class="form-actions">
        <button type="submit" :disabled="saving">
          {{ saving ? '保存中...' : '保存' }}
        </button>
        <RouterLink to="/admin/articles" class="btn-cancel">取消</RouterLink>
      </div>
    </form>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref, onMounted } from 'vue'
import { useRoute, useRouter, RouterLink } from 'vue-router'
import Vditor from 'vditor'
import 'vditor/dist/index.css'
import { articlesApi } from '@/api/articles'
import { categoriesApi } from '@/api/categories'
import type { Category } from '@/types/category'

const route = useRoute()
const router = useRouter()

const isEdit = !!route.params.id
const saving = ref(false)
const error = ref<string | null>(null)
const categories = ref<Category[]>([])
let vditor: Vditor | null = null

const form = reactive({
  title: '',
  slug: '',
  content: '',
  excerpt: '',
  category_id: null as number | null,
  is_published: false,
})

onMounted(async () => {
  // 加载分类列表
  const catRes = await categoriesApi.list()
  categories.value = catRes.data.data ?? []

  // 初始化 Vditor 编辑器
  vditor = new Vditor('vditor-editor', {
    height: 500,
    mode: 'wysiwyg',
    toolbarConfig: { pin: true },
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
      }
    },
  })
})

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
    router.push('/admin/articles')
  } catch (e: unknown) {
    error.value = '保存失败，请检查输入'
  } finally {
    saving.value = false
  }
}
</script>
