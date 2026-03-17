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

<style scoped>
.search-bar form {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}

.search-bar input[type='search'] {
  flex: 1;
  padding: 0.4rem 0.75rem;
  font-size: var(--font-size-sm);
  color: var(--color-text);
  border-radius: 8px;
  border: 1px solid var(--color-border);
  background: var(--color-bg-hover);
  transition: border-color 0.15s, box-shadow 0.15s;
}

.search-bar input[type='search']:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(88, 166, 255, 0.15);
}

.search-bar button[type='submit'] {
  padding: 0.4rem 0.85rem;
  font-size: var(--font-size-sm);
  border: none;
  border-radius: 8px;
  background: var(--color-primary);
  color: #fff;
  cursor: pointer;
  transition: opacity 0.15s;
}

.search-bar button[type='submit']:hover {
  opacity: 0.85;
}
</style>
