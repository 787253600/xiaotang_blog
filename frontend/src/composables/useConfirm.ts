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
    state.options = options
    state.visible = true
    return new Promise(r => { state.resolve = r })
  }

  function accept(): void {
    state.resolve?.(true)
    state.visible = false
  }

  function cancel(): void {
    state.resolve?.(false)
    state.visible = false
  }

  return { confirm, accept, cancel, state }
}
