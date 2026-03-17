/**
 * UI 全局状态：主题切换、全局加载
 */
import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useUiStore = defineStore('ui', () => {
  const isDark = ref(localStorage.getItem('theme') !== 'light')
  const globalLoading = ref(false)

  function toggleTheme(): void {
    isDark.value = !isDark.value
    localStorage.setItem('theme', isDark.value ? 'dark' : 'light')
  }

  function setLoading(val: boolean): void {
    globalLoading.value = val
  }

  return { isDark, globalLoading, toggleTheme, setLoading }
})
