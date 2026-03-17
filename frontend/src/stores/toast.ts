import { defineStore } from 'pinia'
import { ref } from 'vue'

export interface Toast {
  id: string
  type: 'success' | 'error' | 'info'
  message: string
}

export const useToastStore = defineStore('toast', () => {
  const toasts = ref<Toast[]>([])
  const timers = new Map<string, ReturnType<typeof setTimeout>>()

  function add(message: string, type: Toast['type'] = 'info'): void {
    if (toasts.value.length >= 3) {
      const oldest = toasts.value[0]
      remove(oldest.id)
    }
    const id = Math.random().toString(36).slice(2)
    toasts.value.push({ id, type, message })
    timers.set(id, setTimeout(() => remove(id), 3000))
  }

  function remove(id: string): void {
    const timer = timers.get(id)
    if (timer !== undefined) {
      clearTimeout(timer)
      timers.delete(id)
    }
    const idx = toasts.value.findIndex(t => t.id === id)
    if (idx !== -1) toasts.value.splice(idx, 1)
  }

  return { toasts, add, remove }
})
