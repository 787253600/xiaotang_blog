import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(),
  scrollBehavior: () => ({ top: 0 }),
  routes: [
    // 公开页面
    {
      path: '/',
      component: () => import('@/views/public/HomeView.vue'),
      meta: { title: '首页' },
    },
    {
      path: '/articles/:id',
      component: () => import('@/views/public/ArticleView.vue'),
      meta: { title: '文章详情' },
    },
    {
      path: '/search',
      component: () => import('@/views/public/SearchView.vue'),
      meta: { title: '搜索' },
    },
    {
      path: '/tags/:slug',
      component: () => import('@/views/public/TagView.vue'),
      meta: { title: '标签' },
    },
    {
      path: '/links',
      component: () => import('@/views/public/LinksView.vue'),
      meta: { title: '友情链接' },
    },

    // 后台管理（需认证）
    {
      path: '/admin/login',
      component: () => import('@/views/admin/LoginView.vue'),
      meta: { title: '登录' },
    },
    {
      path: '/admin',
      meta: { requiresAuth: true },
      children: [
        {
          path: '',
          component: () => import('@/views/admin/DashboardView.vue'),
          meta: { title: '控制台' },
        },
        {
          path: 'articles',
          component: () => import('@/views/admin/ArticleListView.vue'),
          meta: { title: '文章管理' },
        },
        {
          path: 'articles/new',
          component: () => import('@/views/admin/ArticleEditView.vue'),
          meta: { title: '新建文章' },
        },
        {
          path: 'articles/:id/edit',
          component: () => import('@/views/admin/ArticleEditView.vue'),
          meta: { title: '编辑文章' },
        },
      ],
    },

    // 404
    {
      path: '/:pathMatch(.*)*',
      component: () => import('@/views/public/HomeView.vue'),
    },
  ],
})

// 路由守卫：未登录跳转登录页
router.beforeEach(async (to) => {
  const authStore = useAuthStore()

  if (to.meta.requiresAuth && !authStore.isLoggedIn) {
    return { path: '/admin/login', query: { redirect: to.fullPath } }
  }
})

// 更新页面标题
router.afterEach((to) => {
  const title = to.meta.title as string | undefined
  document.title = title ? `${title} - 小汤博客` : '小汤博客'
})

export default router
