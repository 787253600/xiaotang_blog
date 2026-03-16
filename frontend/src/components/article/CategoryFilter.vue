<template>
  <div class="category-filter">
    <h3>分类</h3>
    <ul>
      <li>
        <button
          :class="{ active: !selected }"
          @click="emit('select', undefined)"
        >
          全部
        </button>
      </li>
      <li v-for="cat in categories" :key="cat.id">
        <button
          :class="{ active: selected === cat.id }"
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
