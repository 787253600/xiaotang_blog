<template>
  <Teleport to="body">
    <div class="toast-container">
      <TransitionGroup name="toast">
        <div
          v-for="toast in toastStore.toasts"
          :key="toast.id"
          :class="['toast', `toast-${toast.type}`]"
        >
          <span class="toast-icon">
            <span v-if="toast.type === 'success'">✓</span>
            <span v-else-if="toast.type === 'error'">✕</span>
            <span v-else>ℹ</span>
          </span>
          {{ toast.message }}
          <button class="toast-close" @click="toastStore.remove(toast.id)">×</button>
        </div>
      </TransitionGroup>
    </div>
  </Teleport>
</template>

<script setup lang="ts">
import { useToastStore } from '@/stores/toast'
const toastStore = useToastStore()
</script>

<style scoped>
.toast-container {
  position: fixed;
  bottom: 1.5rem;
  right: 1.5rem;
  z-index: 9999;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.toast {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  border-radius: var(--radius-md);
  background: var(--color-bg-secondary);
  border: 1px solid var(--color-border);
  color: var(--color-text);
  font-size: var(--font-size-sm);
  min-width: 240px;
  max-width: 360px;
  box-shadow: var(--shadow-md);
}

.toast-success { border-left: 3px solid var(--color-success); }
.toast-error   { border-left: 3px solid var(--color-danger); }
.toast-info    { border-left: 3px solid var(--color-primary); }

.toast-icon { font-weight: bold; flex-shrink: 0; }
.toast-success .toast-icon { color: var(--color-success); }
.toast-error   .toast-icon { color: var(--color-danger); }
.toast-info    .toast-icon { color: var(--color-primary); }

.toast-close {
  margin-left: auto;
  background: none;
  border: none;
  color: var(--color-text-muted);
  cursor: pointer;
  padding: 0;
  font-size: 1rem;
  line-height: 1;
  min-height: unset;
}

.toast-enter-active, .toast-leave-active { transition: all 0.3s ease; }
.toast-enter-from { opacity: 0; transform: translateX(100%); }
.toast-leave-to   { opacity: 0; transform: translateX(100%); }
</style>
