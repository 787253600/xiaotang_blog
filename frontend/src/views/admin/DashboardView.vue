<template>
  <div class="dashboard">
    <!-- grain texture overlay -->
    <div class="grain" aria-hidden="true"></div>

    <header class="dash-header">
      <div class="dash-greeting">
        <span class="dash-label">CONSOLE</span>
        <h1 class="dash-title">{{ authStore.user?.username ?? 'Admin' }}</h1>
      </div>
      <div class="dash-date">
        <span class="date-day">{{ todayDay }}</span>
        <span class="date-rest">{{ todayRest }}</span>
      </div>
    </header>

    <!-- ── stat cards ── -->
    <section class="stat-grid">
      <div
        v-for="(card, i) in statCards"
        :key="card.label"
        class="stat-card"
        :class="{ 'stat-card--accent': i === 0, 'stat-card--loading': !overview && !statsError }"
      >
        <span class="stat-card__label">{{ card.label }}</span>
        <span class="stat-card__value">
          <template v-if="overview">{{ card.value }}</template>
          <span v-else class="stat-placeholder">—</span>
        </span>
        <span class="stat-card__sub">{{ card.sub }}</span>
      </div>
    </section>

    <!-- ── bar chart ── -->
    <section class="chart-section">
      <div class="chart-header">
        <span class="chart-title">DAILY VISITS</span>
        <span class="chart-range">14-DAY WINDOW</span>
      </div>
      <div class="chart-body" v-if="overview">
        <div class="bars">
          <div
            v-for="item in overview.daily_visits"
            :key="item.date"
            class="bar-wrap"
          >
            <div class="bar-track">
              <div
                class="bar-fill"
                :style="{ '--h': barPercent(item.count) }"
                :data-count="item.count"
              ></div>
            </div>
            <span class="bar-date">{{ fmtDate(item.date) }}</span>
          </div>
        </div>
        <div class="chart-axis">
          <span>{{ maxCount }}</span>
          <span>0</span>
        </div>
      </div>
      <div class="chart-body chart-body--skeleton" v-else>
        <div class="bars">
          <div v-for="i in 14" :key="i" class="bar-wrap">
            <div class="bar-track">
              <div class="bar-fill bar-fill--ghost" :style="{ '--h': (Math.sin(i) * 0.4 + 0.5) }"></div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ── actions ── -->
    <section class="action-strip">
      <RouterLink to="/admin/articles/new" class="action-btn action-btn--primary">
        <span class="action-btn__icon">✦</span>
        <span>撰写新文章</span>
      </RouterLink>
      <RouterLink to="/admin/articles" class="action-btn">
        <span class="action-btn__icon">◈</span>
        <span>管理文章</span>
      </RouterLink>
      <RouterLink to="/admin/links" class="action-btn">
        <span class="action-btn__icon">⬡</span>
        <span>友情链接</span>
      </RouterLink>
    </section>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { RouterLink } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { statsApi } from '@/api/stats'
import type { Overview } from '@/types/stats'

const authStore = useAuthStore()
const overview = ref<Overview | null>(null)
const statsError = ref(false)

onMounted(async () => {
  try {
    const res = await statsApi.overview()
    overview.value = res.data.data
  } catch {
    statsError.value = true
  }
})

const maxCount = computed(() =>
  overview.value ? Math.max(...overview.value.daily_visits.map((d) => d.count), 1) : 1,
)

function barPercent(count: number): number {
  return count / maxCount.value
}

function fmtDate(d: string): string {
  const [, m, day] = d.split('-')
  return `${parseInt(m)}/${parseInt(day)}`
}

const statCards = computed(() => [
  {
    label: 'TOTAL ARTICLES',
    value: overview.value?.total_articles.toLocaleString() ?? '—',
    sub: '篇文章',
    link: null,
  },
  {
    label: 'DRAFTS',
    value: overview.value?.draft_articles.toLocaleString() ?? '—',
    sub: '待发布',
    link: null,
  },
  {
    label: 'TOTAL VIEWS',
    value: overview.value?.total_views.toLocaleString() ?? '—',
    sub: '真实文章阅读量',
    link: null,
  },
  {
    label: 'COMMENTS',
    value: overview.value?.pending_comments.toLocaleString() ?? '—',
    sub: '条评论',
    link: null,
  },
])

const now = new Date()
const todayDay = now.toLocaleDateString('en-US', { weekday: 'long' })
const todayRest = now.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Crimson+Pro:ital,wght@0,300;0,400;0,600;1,300&family=IBM+Plex+Mono:wght@400;500&display=swap');

/* ── root ── */
.dashboard {
  --ink: #0d0d0d;
  --paper: #f2ede4;
  --amber: #c8863a;
  --rust: #b84c2b;
  --smoke: #1a1a1a;
  --line: rgba(242, 237, 228, 0.1);
  --muted: rgba(242, 237, 228, 0.4);

  position: relative;
  min-height: 100vh;
  background: var(--ink);
  color: var(--paper);
  font-family: 'IBM Plex Mono', monospace;
  padding: 3rem 2.5rem 4rem;
  overflow: hidden;
}

/* grain overlay */
.grain {
  pointer-events: none;
  position: fixed;
  inset: -50%;
  width: 200%;
  height: 200%;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 512 512' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.75' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='1'/%3E%3C/svg%3E");
  opacity: 0.04;
  z-index: 0;
  animation: grain-drift 8s steps(1) infinite;
}

@keyframes grain-drift {
  0%   { transform: translate(0, 0); }
  10%  { transform: translate(-2%, -3%); }
  20%  { transform: translate(1%, 2%); }
  30%  { transform: translate(-3%, 1%); }
  40%  { transform: translate(2%, -2%); }
  50%  { transform: translate(-1%, 3%); }
  60%  { transform: translate(3%, -1%); }
  70%  { transform: translate(-2%, 2%); }
  80%  { transform: translate(1%, -3%); }
  90%  { transform: translate(-3%, -1%); }
  100% { transform: translate(0, 0); }
}

/* ── header ── */
.dash-header {
  position: relative;
  z-index: 1;
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  margin-bottom: 3.5rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid var(--line);
}

.dash-label {
  display: block;
  font-size: 0.65rem;
  letter-spacing: 0.25em;
  color: var(--amber);
  margin-bottom: 0.4rem;
}

.dash-title {
  font-family: 'Crimson Pro', serif;
  font-size: clamp(2.4rem, 5vw, 4rem);
  font-weight: 300;
  font-style: italic;
  line-height: 1;
  letter-spacing: -0.02em;
  margin: 0;
}

.dash-date {
  text-align: right;
}

.date-day {
  display: block;
  font-size: 0.65rem;
  letter-spacing: 0.2em;
  color: var(--amber);
}

.date-rest {
  font-size: 0.7rem;
  color: var(--muted);
  letter-spacing: 0.05em;
}

/* ── stat grid ── */
.stat-grid {
  position: relative;
  z-index: 1;
  display: grid;
  grid-template-columns: 2fr 1fr 1fr 1fr;
  gap: 1px;
  background: var(--line);
  margin-bottom: 3rem;
  border: 1px solid var(--line);
}

.stat-card {
  background: var(--ink);
  padding: 2rem 1.75rem 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
  transition: background 0.2s;
}

.stat-card:hover {
  background: var(--smoke);
}

.stat-card--accent {
  background: var(--smoke);
}

.stat-card--loading .stat-card__value {
  opacity: 0.3;
  animation: pulse 1.4s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 0.3; }
  50%       { opacity: 0.6; }
}

.stat-card__label {
  font-size: 0.6rem;
  letter-spacing: 0.2em;
  color: var(--amber);
}

.stat-card__value {
  font-family: 'Crimson Pro', serif;
  font-size: clamp(2.8rem, 4vw, 4.5rem);
  font-weight: 600;
  line-height: 1;
  letter-spacing: -0.03em;
}

.stat-placeholder {
  color: var(--muted);
}

.stat-card__sub {
  font-size: 0.65rem;
  color: var(--muted);
  letter-spacing: 0.08em;
}

/* ── chart ── */
.chart-section {
  position: relative;
  z-index: 1;
  margin-bottom: 3rem;
}

.chart-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 1.25rem;
}

.chart-title {
  font-size: 0.65rem;
  letter-spacing: 0.25em;
  color: var(--amber);
}

.chart-range {
  font-size: 0.6rem;
  letter-spacing: 0.15em;
  color: var(--muted);
}

.chart-body {
  display: flex;
  gap: 1rem;
  align-items: flex-end;
}

.bars {
  flex: 1;
  display: flex;
  gap: 3px;
  align-items: flex-end;
  height: 130px;
  border-bottom: 1px solid var(--line);
}

.bar-wrap {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  height: 100%;
  justify-content: flex-end;
  gap: 5px;
}

.bar-track {
  width: 100%;
  height: 120px;
  display: flex;
  align-items: flex-end;
}

.bar-fill {
  width: 100%;
  height: calc(var(--h) * 120px);
  min-height: 2px;
  background: var(--paper);
  opacity: 0.7;
  transform-origin: bottom;
  animation: bar-grow 0.6s cubic-bezier(0.22, 1, 0.36, 1) both;
  transition: opacity 0.2s;
  cursor: default;
  position: relative;
}

.bar-fill:hover {
  opacity: 1;
  background: var(--amber);
}

.bar-fill:hover::after {
  content: attr(data-count);
  position: absolute;
  bottom: calc(100% + 4px);
  left: 50%;
  transform: translateX(-50%);
  font-size: 0.55rem;
  background: var(--paper);
  color: var(--ink);
  padding: 2px 5px;
  white-space: nowrap;
  pointer-events: none;
}

.bar-fill--ghost {
  background: var(--paper);
  opacity: 0.08;
  animation: pulse 1.6s ease-in-out infinite;
}

@keyframes bar-grow {
  from { height: 0; opacity: 0; }
  to   { height: calc(var(--h) * 120px); opacity: 0.7; }
}

/* stagger each bar's animation */
.bar-wrap:nth-child(1)  .bar-fill { animation-delay: 0.00s; }
.bar-wrap:nth-child(2)  .bar-fill { animation-delay: 0.04s; }
.bar-wrap:nth-child(3)  .bar-fill { animation-delay: 0.08s; }
.bar-wrap:nth-child(4)  .bar-fill { animation-delay: 0.12s; }
.bar-wrap:nth-child(5)  .bar-fill { animation-delay: 0.16s; }
.bar-wrap:nth-child(6)  .bar-fill { animation-delay: 0.20s; }
.bar-wrap:nth-child(7)  .bar-fill { animation-delay: 0.24s; }
.bar-wrap:nth-child(8)  .bar-fill { animation-delay: 0.28s; }
.bar-wrap:nth-child(9)  .bar-fill { animation-delay: 0.32s; }
.bar-wrap:nth-child(10) .bar-fill { animation-delay: 0.36s; }
.bar-wrap:nth-child(11) .bar-fill { animation-delay: 0.40s; }
.bar-wrap:nth-child(12) .bar-fill { animation-delay: 0.44s; }
.bar-wrap:nth-child(13) .bar-fill { animation-delay: 0.48s; }
.bar-wrap:nth-child(14) .bar-fill { animation-delay: 0.52s; }

.bar-date {
  font-size: 0.5rem;
  color: var(--muted);
  writing-mode: vertical-rl;
  transform: rotate(180deg);
  height: 32px;
  overflow: hidden;
}

.chart-axis {
  width: 36px;
  height: 130px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: flex-end;
  font-size: 0.55rem;
  color: var(--muted);
  padding-bottom: 10px;
}

/* ── actions ── */
.action-strip {
  position: relative;
  z-index: 1;
  display: flex;
  gap: 1px;
  background: var(--line);
  border: 1px solid var(--line);
}

.action-btn {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.6rem;
  padding: 1.25rem 1rem;
  background: var(--ink);
  color: var(--paper);
  text-decoration: none;
  font-size: 0.7rem;
  letter-spacing: 0.12em;
  transition: background 0.18s, color 0.18s;
}

.action-btn:hover {
  background: var(--smoke);
  color: var(--amber);
}

.action-btn--primary {
  background: var(--smoke);
}

.action-btn--primary:hover {
  background: var(--amber);
  color: var(--ink);
}

.action-btn__icon {
  font-size: 0.85rem;
  opacity: 0.7;
}

/* ── responsive ── */
@media (max-width: 600px) {
  .dashboard {
    padding: 2rem 1.25rem 3rem;
  }

  .stat-grid {
    grid-template-columns: 1fr 1fr;
  }

  .stat-card:first-child,
  .stat-card:nth-child(3) {
    grid-column: 1 / -1;
  }

  .dash-title {
    font-size: 2.2rem;
  }

  .action-strip {
    flex-direction: column;
  }

  .bar-date {
    display: none;
  }
}
</style>
