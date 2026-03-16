<template>
  <div :class="['app-wrapper', { 'dark': uiStore.isDark }]">
    <AppHeader />
    <main class="main-content">
      <RouterView />
    </main>
    <AppFooter />
  </div>
</template>

<script setup lang="ts">
import { RouterView } from 'vue-router'
import AppHeader from '@/components/common/AppHeader.vue'
import AppFooter from '@/components/common/AppFooter.vue'
import { useUiStore } from '@/stores/ui'

const uiStore = useUiStore()
</script>
