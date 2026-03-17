<template>
  <div :class="['app-wrapper', { light: !uiStore.isDark }]">
    <AppHeader />
    <main class="main-content">
      <RouterView />
    </main>
    <AppFooter />
    <!-- 全局单例组件（Task 2 新建后取消注释）
    <AppToast />
    <ConfirmModal />
    -->
  </div>
</template>

<script setup lang="ts">
import { RouterView } from 'vue-router'
import AppHeader from '@/components/common/AppHeader.vue'
import AppFooter from '@/components/common/AppFooter.vue'
import { useUiStore } from '@/stores/ui'
// import AppToast from '@/components/common/AppToast.vue'
// import ConfirmModal from '@/components/common/ConfirmModal.vue'

const uiStore = useUiStore()
</script>
