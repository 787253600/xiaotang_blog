<template>
  <Teleport to="body">
    <Transition name="modal">
      <div v-if="state.visible" class="modal-overlay" @click.self="cancel">
        <div class="modal-box">
          <div class="modal-icon">⚠️</div>
          <h3 class="modal-title">{{ state.options.title }}</h3>
          <p class="modal-message">{{ state.options.message }}</p>
          <div class="modal-actions">
            <button class="btn" @click="cancel">取消</button>
            <button class="btn btn-delete" @click="accept">
              {{ state.options.confirmText ?? '确认' }}
            </button>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup lang="ts">
import { useConfirm } from '@/composables/useConfirm'
const { state, accept, cancel } = useConfirm()
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-box {
  background: var(--color-bg-secondary);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: 2rem;
  max-width: 400px;
  width: 90%;
  text-align: center;
  box-shadow: var(--shadow-md);
}

.modal-icon { font-size: 2rem; margin-bottom: 0.75rem; }
.modal-title { font-size: var(--font-size-xl); margin-bottom: 0.5rem; }
.modal-message { color: var(--color-text-muted); margin-bottom: 1.5rem; }

.modal-actions { display: flex; gap: 0.75rem; justify-content: center; }

.btn-delete {
  background: var(--color-danger);
  color: white;
  border-color: var(--color-danger);
}

.modal-enter-active, .modal-leave-active { transition: opacity 0.2s; }
.modal-enter-from, .modal-leave-to { opacity: 0; }
</style>
