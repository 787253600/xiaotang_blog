export interface DailyVisit {
  date: string
  count: number
}

export interface Overview {
  total_articles: number
  draft_articles: number
  total_views: number
  pending_comments: number
  daily_visits: DailyVisit[]
}
