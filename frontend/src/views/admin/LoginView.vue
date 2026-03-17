<template>
  <div class="login-view">
    <div class="login-card">
      <h1>小汤博客</h1>
      <h2>管理员登录</h2>

      <form @submit.prevent="handleLogin">
        <div class="field">
          <label for="username">用户名</label>
          <input
            id="username"
            v-model="form.username"
            type="text"
            required
            autocomplete="username"
          />
        </div>
        <div class="field">
          <label for="password">密码</label>
          <input
            id="password"
            v-model="form.password"
            type="password"
            required
            autocomplete="current-password"
          />
        </div>
        <p v-if="error" class="error">{{ error }}</p>
        <button type="submit" :disabled="loading">
          {{ loading ? '登录中...' : '登录' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const form = reactive({ username: '', password: '' })
const loading = ref(false)
const error = ref<string | null>(null)

async function handleLogin(): Promise<void> {
  loading.value = true
  error.value = null
  try {
    await authStore.login(form)
    const redirect = (route.query.redirect as string) || '/admin'
    router.push(redirect)
  } catch {
    error.value = '用户名或密码错误'
  } finally {
    loading.value = false
  }
}
</script>
