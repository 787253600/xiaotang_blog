/**
 * 分页状态管理
 */
import { ref, computed } from 'vue'

export function usePagination(totalPages: () => number) {
  const currentPage = ref(1)
  const total = computed(totalPages)

  function goTo(page: number): void {
    if (page >= 1 && page <= total.value) {
      currentPage.value = page
    }
  }

  function prev(): void {
    goTo(currentPage.value - 1)
  }

  function next(): void {
    goTo(currentPage.value + 1)
  }

  const hasPrev = computed(() => currentPage.value > 1)
  const hasNext = computed(() => currentPage.value < total.value)

  return { currentPage, hasPrev, hasNext, goTo, prev, next }
}
