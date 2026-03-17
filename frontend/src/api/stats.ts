import client from './client'
import type { Overview } from '@/types/stats'

interface StatsOverviewResponse {
  code: number
  message: string
  data: Overview
}

export const statsApi = {
  overview() {
    return client.get<StatsOverviewResponse>('/stats/overview')
  },
}
