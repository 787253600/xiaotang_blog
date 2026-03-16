<template>
  <nav class="pagination" aria-label="分页">
    <button :disabled="currentPage <= 1" @click="emit('change', currentPage - 1)">
      上一页
    </button>

    <span class="page-info">{{ currentPage }} / {{ totalPages }}</span>

    <button :disabled="currentPage >= totalPages" @click="emit('change', currentPage + 1)">
      下一页
    </button>
  </nav>
</template>

<script setup lang="ts">
defineProps<{
  currentPage: number
  totalPages: number
}>()

const emit = defineEmits<{
  change: [page: number]
}>()
</script>
