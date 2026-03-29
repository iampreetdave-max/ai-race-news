export interface Article {
  id: string | number
  title: string
  url: string
  summary: string | null
  author: string | null
  image_url: string | null
  source_name: string
  published_at: string | null
  scraped_at?: string
  tags: string[]
  audiences: string[]
  priority?: number
  trending_sources?: number
  slug?: string
}

export interface ArticleListResponse {
  articles: Article[]
  total: number
  limit: number
  offset: number
}

export interface StatsResponse {
  total_articles: number
  total_scrapes: number
  successful_scrapes: number
  success_rate: number
  articles_by_source: Record<string, number>
}

export type Audience = 'developers' | 'business' | 'finance' | 'research' | 'general'

export const AUDIENCE_CONFIG: Record<Audience, { label: string; description: string; color: string; icon: string }> = {
  developers: {
    label: 'Developers',
    description: 'Code, APIs, tools, and technical deep-dives',
    color: 'accent-cyan',
    icon: '/>',
  },
  business: {
    label: 'Business',
    description: 'Launches, strategy, adoption, and market moves',
    color: 'accent-violet',
    icon: '%%',
  },
  finance: {
    label: 'Finance',
    description: 'Funding rounds, IPOs, valuations, and deals',
    color: 'accent-amber',
    icon: '$$',
  },
  research: {
    label: 'Research',
    description: 'Papers, benchmarks, and breakthroughs',
    color: 'accent-blue',
    icon: '??',
  },
  general: {
    label: 'General',
    description: 'Everything AI for everyone',
    color: 'text-secondary',
    icon: '**',
  },
}
