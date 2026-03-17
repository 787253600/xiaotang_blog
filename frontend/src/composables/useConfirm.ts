import { reactive } from 'vue'

export interface ConfirmOptions {
  title: string
  message: string
  confirmText?: string
}

const state = reactive({
  visible: false,
  options: {} as ConfirmOptions,
  resolve: null as ((value: boolean) => void) | null,
})

export function useConfirm() {
  function confirm(options: ConfirmOptions): Promise<boolean> {
    if (state.visible) return Promise.resolve(false)
    state.options = options
    state.visible = true
    return new Promise(r => { state.resolve = r })
  }

  function accept(): void {
    const resolve = state.resolve
    state.resolve = null
    state.visible = false
    resolve?.(true)
  }

  function cancel(): void {
    const resolve = state.resolve
    state.resolve = null
    state.visible = false
    resolve?.(false)
  }

  return { confirm, accept, cancel, state }
}
