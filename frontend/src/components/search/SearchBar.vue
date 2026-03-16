<template>
  <div class="search-bar">
    <form @submit.prevent="handleSubmit">
      <input
        v-model="query"
        type="search"
        placeholder="搜索文章..."
        @input="handleInput"
      />
      <button type="submit">搜索</button>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'

const props = defineProps<{ initialQuery?: string }>()
const emit = defineEmits<{ search: [q: string] }>()

const query = ref(props.initialQuery ?? '')
let debounceTimer: ReturnType<typeof setTimeout> | null = null

watch(() => props.initialQuery, (val) => {
  if (val !== undefined) query.value = val
})

function handleInput(): void {
  if (debounceTimer) clearTimeout(debounceTimer)
  debounceTimer = setTimeout(() => {
    if (query.value.trim()) emit('search', query.value.trim())
  }, 300)
}

function handleSubmit(): void {
  if (debounceTimer) clearTimeout(debounceTimer)
  if (query.value.trim()) emit('search', query.value.trim())
}
</script>
