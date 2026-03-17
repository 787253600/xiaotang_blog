<template>
  <div class="empty-state">
    <div v-if="icon" class="empty-icon" v-html="icon" />
    <p class="empty-title">{{ title }}</p>
    <p v-if="description" class="empty-desc">{{ description }}</p>
    <RouterLink v-if="actionText && actionTo" :to="actionTo" class="btn btn-primary empty-action">
      {{ actionText }}
    </RouterLink>
  </div>
</template>

<script setup lang="ts">
import { RouterLink } from 'vue-router'
defineProps<{
  icon?: string
  title: string
  description?: string
  actionText?: string
  actionTo?: string
}>()
</script>

<style scoped>
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem 1rem;
  text-align: center;
  color: var(--color-text-muted);
}

.empty-icon { font-size: 3rem; margin-bottom: 1rem; opacity: 0.5; }
.empty-title { font-size: var(--font-size-lg); font-weight: 500; color: var(--color-text); }
.empty-desc { margin-top: 0.5rem; font-size: var(--font-size-sm); }
.empty-action { margin-top: 1.25rem; }
</style>
