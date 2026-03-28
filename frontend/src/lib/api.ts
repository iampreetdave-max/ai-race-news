import { ArticleListResponse, StatsResponse } from './types'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export async function fetchArticles(params?: {
  audience?: string
  tags?: string
  source?: string
  since?: string
  limit?: number
  offset?: number
}): Promise<ArticleListResponse> {
  const searchParams = new URLSearchParams()
  if (params?.audience) searchParams.set('audience', params.audience)
  if (params?.tags) searchParams.set('tags', params.tags)
  if (params?.source) searchParams.set('source', params.source)
  if (params?.since) searchParams.set('since', params.since)
  if (params?.limit) searchParams.set('limit', String(params.limit))
  if (params?.offset) searchParams.set('offset', String(params.offset))

  const url = `${API_URL}/api/v1/articles?${searchParams.toString()}`

  try {
    const res = await fetch(url, { next: { revalidate: 300 } })
    if (!res.ok) throw new Error(`API error: ${res.status}`)
    return res.json()
  } catch (error) {
    console.error('Failed to fetch articles:', error)
    return { articles: [], total: 0, limit: 50, offset: 0 }
  }
}

export async function fetchAudienceFeed(
  audience: string,
  limit = 30,
  offset = 0
): Promise<ArticleListResponse> {
  const url = `${API_URL}/api/v1/feed/${audience}?limit=${limit}&offset=${offset}`

  try {
    const res = await fetch(url, { next: { revalidate: 300 } })
    if (!res.ok) throw new Error(`API error: ${res.status}`)
    return res.json()
  } catch (error) {
    console.error(`Failed to fetch ${audience} feed:`, error)
    return { articles: [], total: 0, limit, offset }
  }
}

export async function fetchStats(): Promise<StatsResponse | null> {
  try {
    const res = await fetch(`${API_URL}/api/v1/stats`, { next: { revalidate: 300 } })
    if (!res.ok) throw new Error(`API error: ${res.status}`)
    return res.json()
  } catch (error) {
    console.error('Failed to fetch stats:', error)
    return null
  }
}
