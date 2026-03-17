<template>
  <header class="app-header">
    <div class="header-inner">
      <RouterLink to="/" class="logo">
        <span class="logo-bracket">&lt;/&gt;</span> 小汤博客
      </RouterLink>

      <!-- 桌面端导航 -->
      <nav class="nav desktop-nav">
        <RouterLink to="/">首页</RouterLink>
        <RouterLink to="/search">搜索</RouterLink>
        <RouterLink to="/links">友情链接</RouterLink>
        <RouterLink v-if="authStore.isLoggedIn" to="/admin">后台</RouterLink>
      </nav>

      <!-- 顶部搜索框（桌面端常驻） -->
      <form class="header-search" @submit.prevent="handleHeaderSearch">
        <input
          v-model="headerQuery"
          type="search"
          placeholder="搜索文章..."
          class="header-search-input"
        />
        <button type="submit" class="header-search-btn" aria-label="搜索">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>
          </svg>
        </button>
      </form>

      <div class="header-actions">
        <button class="icon-btn" @click="uiStore.toggleTheme" :title="uiStore.isDark ? '切换浅色' : '切换深色'">
          <!-- 太阳图标（深色模式时显示，点击切换到浅色） -->
          <svg v-if="uiStore.isDark" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/>
            <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/>
            <line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/>
            <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/>
          </svg>
          <!-- 月亮图标（浅色模式时显示） -->
          <svg v-else xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>
          </svg>
        </button>
        <button v-if="authStore.isLoggedIn" class="icon-btn logout-btn" @click="handleLogout" title="退出">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/>
          </svg>
        </button>
        <!-- 移动端汉堡按钮 -->
        <button class="icon-btn hamburger" @click="mobileMenuOpen = !mobileMenuOpen" title="菜单">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="18" x2="21" y2="18"/>
          </svg>
        </button>
      </div>
    </div>

    <!-- 移动端导航抽屉 -->
    <Transition name="drawer">
      <nav v-if="mobileMenuOpen" class="mobile-nav" @click="mobileMenuOpen = false">
        <RouterLink to="/">首页</RouterLink>
        <RouterLink to="/search">搜索</RouterLink>
        <RouterLink to="/links">友情链接</RouterLink>
        <RouterLink v-if="authStore.isLoggedIn" to="/admin">后台</RouterLink>
      </nav>
    </Transition>
  </header>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useUiStore } from '@/stores/ui'

const authStore = useAuthStore()
const uiStore = useUiStore()
const router = useRouter()
const mobileMenuOpen = ref(false)
const headerQuery = ref('')

function handleHeaderSearch(): void {
  if (!headerQuery.value.trim()) return
  router.push({ path: '/search', query: { q: headerQuery.value.trim() } })
  headerQuery.value = ''
}

async function handleLogout(): Promise<void> {
  await authStore.logout()
  router.push('/')
}
</script>

<style scoped>
.app-header {
  position: sticky;
  top: 0;
  z-index: 100;
  background: rgba(13,17,23,0.85);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid var(--color-border);
}

:global(.app-wrapper.light) .app-header {
  background: rgba(255,255,255,0.85);
}

.header-inner {
  max-width: var(--max-width);
  margin: 0 auto;
  padding: 0.75rem var(--spacing-md);
  display: flex;
  align-items: center;
  gap: var(--spacing-lg);
}

.logo {
  font-family: var(--font-mono);
  font-size: var(--font-size-xl);
  font-weight: 700;
  color: var(--color-text);
  text-decoration: none;
  display: flex;
  align-items: center;
  gap: 0.4rem;
}

.logo-bracket { color: var(--color-primary); }

.desktop-nav {
  display: flex;
  gap: var(--spacing-md);
  flex: 1;
}

.desktop-nav a {
  color: var(--color-text-muted);
  text-decoration: none;
  font-size: var(--font-size-sm);
  padding-bottom: 2px;
  border-bottom: 2px solid transparent;
  transition: color 0.15s, border-color 0.15s;
}

.desktop-nav a:hover,
.desktop-nav a.router-link-active {
  color: var(--color-text);
  border-bottom-color: var(--color-primary);
}

.header-actions {
  display: flex;
  gap: 0.25rem;
  align-items: center;
}

.icon-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border-radius: var(--radius-md);
  background: none;
  border: none;
  color: var(--color-text-muted);
  cursor: pointer;
  transition: background 0.15s, color 0.15s;
  min-height: unset;
  padding: 0;
}

.icon-btn:hover { background: var(--color-bg-hover); color: var(--color-text); }

.hamburger { display: none; }

.mobile-nav {
  display: flex;
  flex-direction: column;
  padding: 0.5rem var(--spacing-md) 1rem;
  border-top: 1px solid var(--color-border);
}

.mobile-nav a {
  padding: 0.75rem 0;
  color: var(--color-text);
  text-decoration: none;
  border-bottom: 1px solid var(--color-border);
  min-height: 44px;
  display: flex;
  align-items: center;
}

.drawer-enter-active, .drawer-leave-active { transition: opacity 0.2s, transform 0.2s; }
.drawer-enter-from, .drawer-leave-to { opacity: 0; transform: translateY(-8px); }

@media (max-width: 639px) {
  .desktop-nav { display: none; }
  .hamburger { display: flex; }
}

.header-search {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  flex: 1;
  max-width: 280px;
}

.header-search-input {
  flex: 1;
  padding: 0.35rem 0.65rem;
  font-size: var(--font-size-sm);
  color: var(--color-text);
  background: var(--color-bg-hover);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  outline: none;
  transition: border-color 0.15s, box-shadow 0.15s;
  min-height: unset;
}

.header-search-input:focus {
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(88, 166, 255, 0.15);
}

.header-search-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border-radius: var(--radius-md);
  background: none;
  border: none;
  color: var(--color-text-muted);
  cursor: pointer;
  transition: background 0.15s, color 0.15s;
  min-height: unset;
  padding: 0;
}

.header-search-btn:hover {
  background: var(--color-bg-hover);
  color: var(--color-text);
}

@media (max-width: 639px) {
  .header-search { display: none; }
}
</style>
