<template>
  <div class="category-filter">
    <h3>分类</h3>
    <ul>
      <li>
        <button
          :class="['category-btn', { active: !selected }]"
          @click="emit('select', undefined)"
        >
          全部
        </button>
      </li>
      <li v-for="cat in categories" :key="cat.id">
        <button
          :class="['category-btn', { active: selected === cat.id }]"
          @click="emit('select', cat.id)"
        >
          {{ cat.name }}
          <span class="count">{{ cat.article_count }}</span>
        </button>
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { categoriesApi } from '@/api/categories'
import type { Category } from '@/types/category'

defineProps<{ selected?: number }>()
const emit = defineEmits<{ select: [id: number | undefined] }>()

const categories = ref<Category[]>([])
onMounted(async () => {
  const res = await categoriesApi.list()
  categories.value = res.data.data ?? []
})
</script>

<style scoped>
.category-filter h3 {
  font-size: var(--font-size-sm);
  font-weight: 600;
  color: var(--color-text-muted);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 0.5rem;
}

.category-filter ul {
  list-style: none;
  margin: 0;
  padding: 0;
}

.category-filter li {
  margin-bottom: 2px;
}

.category-btn {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  padding: 0.5rem 0.75rem;
  border-radius: var(--radius-sm);
  border: none;
  background: none;
  color: var(--color-text-muted);
  cursor: pointer;
  text-align: left;
  border-left: 3px solid transparent;
  transition: all 0.15s;
  font-size: var(--font-size-sm);
}

.category-btn.active,
.category-btn:hover {
  border-left-color: var(--color-primary);
  background: var(--color-bg-hover);
  color: var(--color-text);
}

.count {
  margin-left: auto;
  font-size: 0.75rem;
  color: var(--color-text-muted);
  background: var(--color-bg-hover);
  padding: 1px 6px;
  border-radius: 9999px;
}
</style>
