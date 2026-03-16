import type { Category } from './category'
import type { Tag } from './tag'

export interface ArticleSummary {
  id: number
  title: string
  slug: string
  excerpt: string | null
  category: Category | null
  tags: Tag[]
  view_count: number
  like_count: number
  is_published: boolean
  created_at: string
  published_at: string | null
}

export interface Article extends ArticleSummary {
  content: string
  updated_at: string
}

export interface ArticleCreate {
  title: string
  slug: string
  content: string
  excerpt?: string
  category_id?: number | null
  tag_ids?: number[]
  is_published?: boolean
}

export interface ArticleUpdate {
  title?: string
  slug?: string
  content?: string
  excerpt?: string
  category_id?: number | null
  tag_ids?: number[]
  is_published?: boolean
}
