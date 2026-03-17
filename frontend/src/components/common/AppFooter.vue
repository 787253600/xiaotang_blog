<template>
  <footer class="app-footer">
    <p>© {{ year }} 小汤博客 · Powered by FastAPI + Vue 3</p>
  </footer>
</template>

<script setup lang="ts">
const year = new Date().getFullYear()
</script>

<style scoped>
.app-footer {
  text-align: center;
  border-top: 1px solid var(--color-border);
  padding: 1rem 0;
}

.app-footer p {
  margin: 0;
  color: var(--color-text-muted);
  font-size: var(--font-size-sm);
}
</style>
