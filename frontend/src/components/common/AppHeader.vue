<template>
  <header class="app-header">
    <div class="header-inner">
      <RouterLink to="/" class="logo">小汤博客</RouterLink>

      <nav class="nav">
        <RouterLink to="/">首页</RouterLink>
        <RouterLink to="/search">搜索</RouterLink>
        <RouterLink v-if="authStore.isLoggedIn" to="/admin">后台</RouterLink>
      </nav>

      <div class="header-actions">
        <button class="theme-btn" @click="uiStore.toggleTheme" title="切换主题">
          {{ uiStore.isDark ? '☀️' : '🌙' }}
        </button>
        <button v-if="authStore.isLoggedIn" class="logout-btn" @click="handleLogout">
          退出
        </button>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { RouterLink, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useUiStore } from '@/stores/ui'

const authStore = useAuthStore()
const uiStore = useUiStore()
const router = useRouter()

async function handleLogout(): Promise<void> {
  await authStore.logout()
  router.push('/')
}
</script>
