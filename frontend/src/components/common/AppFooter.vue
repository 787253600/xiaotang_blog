<template>
  <footer class="app-footer">
    <p>© {{ year }} 小唐博客 · Powered by FastAPI + Vue 3</p>
  </footer>
</template>

<script setup lang="ts">
const year = new Date().getFullYear()
</script>
