<template>
  <div class="dashboard-view">
    <h1>控制台</h1>
    <div class="dashboard-actions">
      <RouterLink to="/admin/articles/new" class="btn btn-primary">
        撰写新文章
      </RouterLink>
      <RouterLink to="/admin/articles" class="btn">
        管理文章
      </RouterLink>
    </div>
    <p class="welcome">欢迎回来，{{ authStore.user?.username }}</p>
  </div>
</template>

<script setup lang="ts">
import { RouterLink } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
</script>
