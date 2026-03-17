<template>
  <div class="tag-view">
    <h1 v-if="tagName" class="tag-title"># {{ tagName }}</h1>
    <ArticleList :tag-id="tagId" :page-size="10" />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import ArticleList from '@/components/article/ArticleList.vue'

const route = useRoute()
const tagId = computed(() => Number(route.params.id))
const tagName = computed(() => route.query.name as string | undefined)
</script>
