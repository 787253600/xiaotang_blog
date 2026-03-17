<template>
  <div :class="['app-wrapper', { light: !uiStore.isDark }]">
    <AppHeader />
    <main class="main-content">
      <RouterView />
    </main>
    <AppFooter />
    <AppToast />
    <ConfirmModal />
  </div>
</template>

<script setup lang="ts">
import { RouterView } from 'vue-router'
import AppHeader from '@/components/common/AppHeader.vue'
import AppFooter from '@/components/common/AppFooter.vue'
import AppToast from '@/components/common/AppToast.vue'
import ConfirmModal from '@/components/common/ConfirmModal.vue'
import { useUiStore } from '@/stores/ui'

const uiStore = useUiStore()
</script>
