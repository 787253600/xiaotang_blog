import { ref, onUnmounted } from 'vue'

export function useDraftSave(key: string) {
  const lastSavedText = ref<string>('')
  let intervalId: ReturnType<typeof setInterval> | null = null
  let lastSavedAt: Date | null = null

  function save(data: unknown): void {
    localStorage.setItem(key, JSON.stringify(data))
    lastSavedAt = new Date()
    lastSavedText.value = '刚刚暂存'
  }

  function load<T>(): T | null {
    const raw = localStorage.getItem(key)
    if (!raw) return null
    try {
      return JSON.parse(raw) as T
    } catch {
      return null
    }
  }

  function clear(): void {
    localStorage.removeItem(key)
    lastSavedText.value = ''
    lastSavedAt = null
  }

  function startAutoSave(getter: () => unknown, intervalMs = 30_000): void {
    intervalId = setInterval(() => {
      save(getter())
      updateSavedText()
    }, intervalMs)

    // 每分钟更新「上次暂存于 X 分钟前」文字
    setInterval(updateSavedText, 60_000)
  }

  function updateSavedText(): void {
    if (!lastSavedAt) return
    const minutes = Math.floor((Date.now() - lastSavedAt.getTime()) / 60_000)
    lastSavedText.value = minutes === 0 ? '刚刚暂存' : `上次暂存于 ${minutes} 分钟前`
  }

  onUnmounted(() => {
    if (intervalId !== null) clearInterval(intervalId)
  })

  return { save, load, clear, startAutoSave, lastSavedText }
}
