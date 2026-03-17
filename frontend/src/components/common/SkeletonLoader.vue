<template>
  <div class="skeleton-wrapper">
    <div v-for="i in lines" :key="i" class="skeleton-line" :style="lineStyle(i)" />
  </div>
</template>

<script setup lang="ts">
const props = withDefaults(defineProps<{ lines?: number }>(), { lines: 3 })

function lineStyle(i: number) {
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
