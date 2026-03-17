# 前端全面优化设计文档

**日期：** 2026-03-17
**项目：** Xiaotangblog 前端
**技术栈：** Vue 3 + TypeScript + Vite + Pinia

---

## 目标

对博客前台（访客页面）和管理后台进行全面升级，包含：
- 建立技术感深色主题设计 token
- 组件视觉重构
- UX 功能补全（骨架屏、Toast、空状态、确认弹窗）
- Bug 修复（SearchView props 不匹配、CommentItem 缺失）
- 移动端优先响应式优化

**风格定位：** 技术博客，深色主题为主，参考 GitHub 配色风格。
**受众：** 技术读者，桌面端和移动端同等重要。

---

## 一、设计 Token

### 主题切换机制

**CSS 层面：** `:root` 定义深色主题（全局默认，`body` 等全局选择器可直接继承），`.app-wrapper.light` 覆盖为浅色。这样全局元素样式（`body`、`a`、`button` 等）能正常继承深色 token，光照模式时通过 `.light` 类覆盖。

**JS 层面：** `ui.ts` 初始化时默认 `isDark = true`（深色为默认）：
```typescript
// stores/ui.ts — 修改默认值
isDark: localStorage.getItem('theme') !== 'light',  // 原来是 === 'dark'
```

`toggleTheme()` 保持不变（仍操作 `isDark` 布尔值）。

`App.vue` 主题类绑定改为：
```html
<div :class="['app-wrapper', { light: !uiStore.isDark }]">
```

### 颜色系统

```css
/* variables.css */

/* 深色主题（全局默认，body 等全局选择器可继承） */
:root {
  --color-bg:           #0d1117;
  --color-bg-secondary: #161b22;
  --color-bg-hover:     #21262d;   /* 新增 */
  --color-primary:      #58a6ff;
  --color-primary-hover:#79b8ff;   /* 保留，值更新 */
  --color-danger:       #f78166;
  --color-error:        var(--color-danger);  /* 向后兼容别名，防止漏改引用 */
  --color-success:      #3fb950;
  --color-text:         #e6edf3;
  --color-text-muted:   #8b949e;
  --color-border:       #30363d;
  --shadow-sm: 0 1px 3px rgba(0,0,0,0.4);
  --shadow-md: 0 4px 12px rgba(0,0,0,0.5);
  /* --spacing-*, --radius-*, --font-size-*, --max-width, --content-width: 完全保留不变 */
}

/* 浅色主题覆盖（应用到 .app-wrapper.light 及其所有子元素） */
.app-wrapper.light {
  --color-bg:           #ffffff;
  --color-bg-secondary: #f6f8fa;
  --color-bg-hover:     #eaeef2;
  --color-primary:      #0969da;
  --color-primary-hover:#0550ae;
  --color-danger:       #cf222e;
  --color-success:      #1a7f37;
  --color-text:         #1f2328;
  --color-text-muted:   #656d76;
  --color-border:       #d0d7de;
  --shadow-sm: 0 1px 3px rgba(0,0,0,0.1);
  --shadow-md: 0 4px 12px rgba(0,0,0,0.15);
}
```

**注意：** `body` 级样式（`background-color`、`color`、`font-family`）在 `main.css` 中保持引用 `var(--color-bg)` 等，因 `:root` 已定义，全局继承不受影响。`.app-wrapper.light` 的覆盖通过 CSS 层叠优先级生效，子元素自动继承。

**必须删除：** 现有 `variables.css` 中存在旧的 `.dark { ... }` 覆盖块（约第 44–51 行），新方案改用 `:root` 为深色默认，旧 `.dark` 块必须完全删除，否则其中的 token 值（如 `--color-bg: #111827`）会因 class 优先级问题覆盖新的 `:root` 默认值，导致颜色不一致。

**Token 迁移映射：**

| 旧 Token | 处理 | 说明 |
|----------|------|------|
| `--color-bg` | 保留同名，值更新 | 无需改动引用 |
| `--color-bg-secondary` | 保留同名，值更新 | 无需改动引用 |
| `--color-error` | 保留为 `var(--color-danger)` 别名 | 零破坏，旧引用自动转发 |
| `--color-primary-hover` | 保留同名，值更新 | 无需改动引用 |
| `--color-bg-hover` | 新增 | 新组件使用 |
| `--spacing-*`, `--radius-*`, `--font-size-*` | 完全保留 | 无需处理 |
| `--content-width` | 保留（860px），不修改 | ArticleView 正文用局部 720px 限宽 |

### 字体

```css
:root {
  --font-sans: 'Inter', 'PingFang SC', system-ui, sans-serif;  /* 保留原名，值更新 */
  --font-mono: 'JetBrains Mono', 'Fira Code', monospace;
  --line-height-body: 1.7;  /* 新增 */
}
```

**字体加载：** `npm install @fontsource/inter`，在 `main.ts` 中 `import '@fontsource/inter'`。

### 间距

现有 `--spacing-*` token 保留不变。卡片内边距统一为 `1.25rem`，直接写具体值。

---

## 二、组件视觉升级

### AppHeader

- 背景：`rgba(13,17,23,0.85)` + `backdrop-filter: blur(12px)`
  - `.light` 主题：`rgba(255,255,255,0.85)`
  - 如遇 blur 被裁切，检查祖先是否有 `overflow: hidden` 或 `transform`，移除即可
- 底部 `1px solid var(--color-border)` 分隔线
- Logo：`font-family: var(--font-mono)` + `</>` 前缀
- 主题切换：内联 SVG（Heroicons 太阳/月亮，MIT 许可）
- 导航链接 hover 下划线动画
- 移动端：hamburger 图标，点击展开垂直导航抽屉（见第六节）

### ArticleCard

**彩色左边框 — category 颜色映射（`category` 为 null 时默认索引 0）：**

```typescript
const CATEGORY_COLORS = ['#58a6ff', '#3fb950', '#f78166', '#d2a8ff', '#ffa657']
const borderColor = CATEGORY_COLORS[(props.article.category?.id ?? 0) % 5]
```

- 左侧 `3px` 竖向彩色边框（CSS `border-left`）
- 卡片背景 `var(--color-bg-secondary)`，悬浮时蓝色 border + `translateY(-2px)`
- 标题 `font-weight: 600`，摘要 `var(--color-text-muted)`
- 底部 meta：flex 行，标签小胶囊（`border-radius: 9999px`，`padding: 2px 8px`）

### ArticleView（文章详情）

- 顶部 Hero 区：大标题 + meta + 分隔线
- 正文 `.article-body { max-width: 720px; margin: 0 auto; }`（局部限宽，不影响 `--content-width`）
- 桌面端右侧 TOC 占位框架：`<aside class="toc-placeholder">` 空元素，内容生成逻辑留待后续（见第八节）
- **代码复制按钮注入：**
  ```typescript
  // 使用 MutationObserver 监听 vditor 渲染完成，然后注入按钮
  // 每次 Vditor.preview() 调用前，先 disconnect() 旧 observer
  // 渲染完成后重新 observe，防止重复注入
  let observer: MutationObserver | null = null

  function injectCopyButtons(container: HTMLElement) {
    container.querySelectorAll('pre').forEach(pre => {
      if (pre.querySelector('.copy-btn')) return  // 防重复
      const btn = document.createElement('button')
      btn.className = 'copy-btn'
      btn.textContent = '复制'
      btn.onclick = () => navigator.clipboard.writeText(pre.innerText)
      pre.style.position = 'relative'
      pre.appendChild(btn)
    })
  }
  ```
- **Vditor 主题同步：**
  ```typescript
  // 封装为函数，每次主题变化时调用
  async function renderContent(content: string) {
    observer?.disconnect()
    await Vditor.preview(el, content, { mode: uiStore.isDark ? 'dark' : 'light' })
    injectCopyButtons(el)
  }

  // watch 主题变化，传入当前内容重新渲染
  watch(() => uiStore.isDark, () => {
    if (article.value) renderContent(article.value.content)
  })
  ```
- 点赞按钮：心形 SVG + `@keyframes pulse` 动画

### 侧边栏

- SearchBar：`border-radius: 8px`，聚焦时 `var(--color-primary)` outline
- CategoryFilter：列表样式，active 态左侧蓝色竖线 + `var(--color-bg-hover)` 背景
- 分类数量徽章右对齐

### AppFooter

- 单行居中，`color: var(--color-text-muted)`

---

## 三、UX 功能补全

### 骨架屏（SkeletonLoader 组件）

新建 `components/common/SkeletonLoader.vue`，通用占位条样式（灰色矩形 + shimmer 动画），不精确模拟卡片布局，接受 `lines` prop（默认 3）。

覆盖场景：文章列表、文章详情、分类过滤器（替换所有"加载中..."文字）。

### Toast 通知系统

新建 `components/common/AppToast.vue` + `stores/toast.ts`。

**队列行为：** 最多 3 条，超出移除最旧；每条独立计时 3 秒，互不影响。

**Store（`stores/toast.ts`，Pinia defineStore）：**
```typescript
interface Toast { id: string; type: 'success' | 'error' | 'info'; message: string }
// actions: add(message, type), remove(id)
```

- 位置：`position: fixed; bottom: 1.5rem; right: 1.5rem`
- 动画：从右侧滑入，3 秒后淡出

### 删除确认弹窗（ConfirmModal 组件）

新建 `components/common/ConfirmModal.vue`（使用 `<Teleport to="body">` 避免 z-index 问题）。

**`useConfirm` composable（模块级 reactive，不放 Pinia）：**

```typescript
// composables/useConfirm.ts
interface ConfirmOptions { title: string; message: string; confirmText?: string }

const state = reactive({
  visible: false,
  options: {} as ConfirmOptions,
  resolve: null as ((v: boolean) => void) | null,
})

export function useConfirm() {
  function confirm(options: ConfirmOptions): Promise<boolean> {
    state.options = options
    state.visible = true
    return new Promise(r => { state.resolve = r })
  }
  // ConfirmModal 内部调用 accept()/cancel() 触发 state.resolve
  function accept() { state.resolve?.(true); state.visible = false }
  function cancel() { state.resolve?.(false); state.visible = false }
  return { confirm, accept, cancel, state }
}
```

`App.vue` 挂载单例 `<ConfirmModal />`；调用方 `await confirm({ ... })` 获得布尔值。

### 空状态（EmptyState 组件）

新建 `components/common/EmptyState.vue`。
props：`icon`（SVG string）、`title`、`description`（可选）、`actionText`（可选）、`actionTo`（可选路由路径）

---

## 四、Bug 修复

### 1. SearchView props 不匹配

**问题：** SearchView 错误地向 ArticleList 传递 `articles`、`total` 等 ArticleList 不接受的 props。

**为何不用 ArticleList 的 `searchQuery` prop：** ArticleList 内部管理分页状态，SearchView 无法从外部控制当前页码，因此不适合复用。

**修复方案：** SearchView 直接调用 `articlesApi.search()` 渲染 ArticleCard 列表 + AppPagination，**不使用 `useSearch` composable**（其内置 300ms 防抖对分页点击多余）。

SearchView 自行管理：`query ref`、`results ref`、`total ref`、`currentPage ref`、`loading ref`，在搜索框 submit 时防抖，在翻页时直接调用 API（无防抖）。

### 2. CommentItem.vue 缺失

**修复方案：**
1. 新建 `components/article/CommentItem.vue`
2. `CommentList.vue` `<script setup>` 中添加 `import CommentItem from './CommentItem.vue'`

**CommentItem 交互模型：**
- 展示：头像占位圆形 + 作者名 + 相对时间 + 内容
- 最大嵌套深度：2 层，通过 `depth` prop 控制（`depth >= 2` 时不渲染回复按钮）
- 回复触发：点击"回复"按钮，内部显示内联表单
- 回复提交：调用评论 API，成功后 emit `reply-submitted` 事件（**无 payload**）给 CommentList
- CommentList 收到事件后**重新调用 API 获取最新评论列表**

**CommentList.vue 需同步修改：**

1. 将 `onMounted` 中的 `client.get(...)` 提取为具名函数 `fetchComments()`：
   ```typescript
   async function fetchComments() {
     // 原 onMounted 内的逻辑移至此处
   }
   onMounted(fetchComments)
   ```

2. 在模板中为 `<CommentItem>` 绑定事件监听：
   ```html
   <CommentItem
     v-for="comment in comments"
     :key="comment.id"
     :comment="comment"
     :article-id="articleId"
     :depth="0"
     @reply-submitted="fetchComments"
   />
   ```

### 3. 主题切换按钮 emoji

改为 Heroicons `sun` / `moon` 内联 SVG（MIT 许可，直接复制 path，无需安装包）。

---

## 五、管理后台优化

### ArticleListView

- 偶数行 `var(--color-bg-hover)` 斑马纹
- 行悬浮高亮
- 编辑/删除改为 SVG 图标按钮（`title` tooltip）
- 删除接入 `useConfirm()`

### ArticleEditView

- 顶部标题栏
- 底部 sticky 操作栏（`position: sticky; bottom: 0; background: var(--color-bg)`）
  - Vditor 工具栏吸顶，操作栏吸底，不重叠
- 标题为空时实时红色提示
- 发布成功触发 toast

### LoginView

- 居中卡片（`var(--color-bg-secondary)`，圆角，`var(--shadow-md)`）
- 顶部 Logo + 博客名
- 登录失败触发 toast error

### DashboardView

不修改，验证新 token 下视觉正常即可。

---

## 六、移动端响应式

**断点（移动优先）：**
```css
/* 默认 < 640px */
/* @media (min-width: 640px) 平板 */
/* @media (min-width: 1024px) 桌面 */
```

**关键改动：**
- 首页：移动端单列，侧边栏可展开折叠；桌面端双栏
- AppHeader：移动端 hamburger，点击展开导航抽屉（绝对定位 + 遮罩关闭）
- ArticleView TOC：移动端改为 `<details>` 折叠
- ArticleListView：移动端表格变卡片列表（展示标题、分类、状态、日期、操作按钮）
- 所有可点击元素 `min-height: 44px; min-width: 44px`

---

## 七、文件变更清单

### 新增文件
- `src/components/common/SkeletonLoader.vue`
- `src/components/common/AppToast.vue`
- `src/components/common/ConfirmModal.vue`
- `src/components/common/EmptyState.vue`
- `src/components/article/CommentItem.vue`
- `src/stores/toast.ts`
- `src/composables/useConfirm.ts`

### 修改文件
- `src/styles/variables.css` — token 更新（见第一节）
- `src/styles/main.css` — 保留 `body` 级 token 引用（`:root` 已定义，继承正常）
- `src/main.ts` — `import '@fontsource/inter'`
- `src/App.vue` — 主题类 `{ light: !uiStore.isDark }`；挂载 `<AppToast />`、`<ConfirmModal />`
- `src/stores/ui.ts` — 默认值改为 `isDark: localStorage.getItem('theme') !== 'light'`
- `src/components/common/AppHeader.vue` — 毛玻璃 + SVG 图标 + hamburger
- `src/components/common/AppFooter.vue` — 简化样式
- `src/components/article/ArticleCard.vue` — 彩色边框 + 悬浮动效
- `src/components/article/ArticleList.vue` — 接入 SkeletonLoader + EmptyState
- `src/components/article/CommentList.vue` — import CommentItem；监听 `reply-submitted` 重新拉取
- `src/components/article/CategoryFilter.vue` — 列表样式
- `src/components/search/SearchBar.vue` — 圆角 + 聚焦样式
- `src/views/public/HomeView.vue` — 移动端响应式
- `src/views/public/ArticleView.vue` — Hero + TOC 占位 + 代码复制 + Vditor 主题同步
- `src/views/public/SearchView.vue` — 重构，直接用 `articlesApi.search()`
- `src/views/public/TagView.vue` — 验证 ArticleList 改动兼容（无其他修改）
- `src/views/admin/LoginView.vue` — 卡片布局 + toast
- `src/views/admin/ArticleListView.vue` — 斑马纹 + ConfirmModal + 移动端卡片视图
- `src/views/admin/ArticleEditView.vue` — sticky 底部栏 + toast + 验证

---

## 八、不在本次范围内

- TOC 自动从 Markdown 标题生成条目（本次仅 UI 占位框架）
- 图片上传
- 文章调度/定时发布
- 标签管理后台
- 用户个人资料页
- PWA 支持
- DashboardView 深度优化
