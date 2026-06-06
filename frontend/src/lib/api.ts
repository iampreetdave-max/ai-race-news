import { ArticleListResponse, StatsResponse } from './types'

const API_URL = process.env.NEXT_PUBLIC_API_URL || ''
const IS_STATIC = !API_URL

function assertJson(res: Response): void {
  const contentType = res.headers.get('content-type')
  if (!contentType || !contentType.includes('application/json')) {
    throw new Error(`Expected JSON, got ${contentType || 'unknown content-type'}`)
  }
}

export async function fetchArticles(params?: {
  audience?: string
  tags?: string
  limit?: number
  offset?: number
}): Promise<ArticleListResponse> {
  const limit = params?.limit || 30
  const offset = params?.offset || 0
  try {
    if (IS_STATIC) {
      const res = await fetch('/data/articles.json')
      if (!res.ok) throw new Error('Failed to load articles.json')
      assertJson(res)
      const data: ArticleListResponse = await res.json()

      let articles = data.articles

      if (params?.audience) {
        articles = articles.filter((a) => a.audiences.includes(params.audience!))
      }
      if (params?.tags) {
        const tagList = params.tags.split(',')
        articles = articles.filter((a) => a.tags.some((t) => tagList.includes(t)))
      }

      const sliced = articles.slice(offset, offset + limit)

      return { articles: sliced, total: articles.length, limit, offset }
    } else {
      const searchParams = new URLSearchParams()
      if (params?.audience) searchParams.set('audience', params.audience)
      if (params?.tags) searchParams.set('tags', params.tags)
      if (params?.limit) searchParams.set('limit', String(params.limit))
      if (params?.offset) searchParams.set('offset', String(params.offset))

      const res = await fetch(`${API_URL}/api/v1/articles?${searchParams.toString()}`)
      if (!res.ok) throw new Error(`API error: ${res.status}`)
      return res.json()
    }
  } catch (error) {
    console.error('Failed to fetch articles:', error)
    return {
      articles: [],
      total: 0,
      limit,
      offset,
      error: error instanceof Error ? error.message : 'fetch failed',
    }
  }
}

export async function fetchAudienceFeed(
  audience: string,
  limit = 30,
  offset = 0
): Promise<ArticleListResponse> {
  try {
    if (IS_STATIC) {
      const res = await fetch(`/data/feed-${audience}.json`)
      if (!res.ok) throw new Error(`Failed to load feed-${audience}.json`)
      assertJson(res)
      const data: ArticleListResponse = await res.json()
      const sliced = data.articles.slice(offset, offset + limit)
      return { articles: sliced, total: data.articles.length, limit, offset }
    } else {
      const res = await fetch(`${API_URL}/api/v1/feed/${audience}?limit=${limit}&offset=${offset}`)
      if (!res.ok) throw new Error(`API error: ${res.status}`)
      return res.json()
    }
  } catch (error) {
    console.error(`Failed to fetch ${audience} feed:`, error)
    return {
      articles: [],
      total: 0,
      limit,
      offset,
      error: error instanceof Error ? error.message : 'fetch failed',
    }
  }
}

export async function fetchStats(): Promise<StatsResponse | null> {
  try {
    const url = IS_STATIC ? '/data/stats.json' : `${API_URL}/api/v1/stats`
    const res = await fetch(url)
    if (!res.ok) return null
    return res.json()
  } catch {
    return null
  }
}
