'use client'

import { useState, useEffect } from 'react'
import { Article, ArticleListResponse } from '@/lib/types'
import NewsCard from './NewsCard'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

interface NewsFeedProps {
  audience?: string
  initialArticles?: Article[]
  initialTotal?: number
  title?: string
  description?: string
  accentColor?: string
  icon?: string
}

export default function NewsFeed({
  audience,
  initialArticles = [],
  initialTotal = 0,
  title,
  description,
  accentColor = 'accent-cyan',
  icon,
}: NewsFeedProps) {
  const [articles, setArticles] = useState<Article[]>(initialArticles)
  const [total, setTotal] = useState(initialTotal)
  const [loading, setLoading] = useState(initialArticles.length === 0)
  const [offset, setOffset] = useState(0)
  const [selectedTag, setSelectedTag] = useState<string | null>(null)
  const limit = 30

  useEffect(() => {
    if (initialArticles.length > 0) return
    loadArticles()
  }, [audience])

  async function loadArticles(newOffset = 0) {
    setLoading(true)
    try {
      const params = new URLSearchParams()
      if (audience) params.set('audience', audience)
      if (selectedTag) params.set('tags', selectedTag)
      params.set('limit', String(limit))
      params.set('offset', String(newOffset))

      const endpoint = audience
        ? `${API_URL}/api/v1/feed/${audience}?limit=${limit}&offset=${newOffset}`
        : `${API_URL}/api/v1/articles?${params.toString()}`

      const res = await fetch(endpoint)
      if (!res.ok) throw new Error('API error')
      const data: ArticleListResponse = await res.json()

      if (newOffset === 0) {
        setArticles(data.articles)
      } else {
        setArticles((prev) => [...prev, ...data.articles])
      }
      setTotal(data.total)
      setOffset(newOffset)
    } catch (err) {
      console.error('Failed to load articles:', err)
    } finally {
      setLoading(false)
    }
  }

  function loadMore() {
    loadArticles(offset + limit)
  }

  // Collect tags for filter
  const tagCounts: Record<string, number> = {}
  articles.forEach((a) => {
    a.tags.forEach((t) => {
      tagCounts[t] = (tagCounts[t] || 0) + 1
    })
  })
  const topTags = Object.entries(tagCounts)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 8)

  const filteredArticles = selectedTag
    ? articles.filter((a) => a.tags.includes(selectedTag))
    : articles

  return (
    <div>
      {/* Section header */}
      {title && (
        <div className="mb-6">
          <div className="flex items-center gap-3 mb-2">
            {icon && (
              <span className={`font-mono text-lg text-${accentColor}`}>{icon}</span>
            )}
            <h1 className="font-display text-xl sm:text-2xl font-bold tracking-tight">
              {title}
            </h1>
          </div>
          {description && (
            <p className="text-sm text-text-muted max-w-xl">{description}</p>
          )}
        </div>
      )}

      {/* Tag filters */}
      {topTags.length > 0 && (
        <div className="flex flex-wrap gap-1.5 mb-5">
          <button
            onClick={() => setSelectedTag(null)}
            className={`tag-pill transition-all ${
              !selectedTag
                ? 'bg-text-primary/10 text-text-primary'
                : 'tag-default hover:text-text-primary'
            }`}
          >
            all
          </button>
          {topTags.map(([tag, count]) => (
            <button
              key={tag}
              onClick={() => setSelectedTag(selectedTag === tag ? null : tag)}
              className={`tag-pill transition-all ${
                selectedTag === tag
                  ? 'bg-text-primary/10 text-text-primary'
                  : 'tag-default hover:text-text-primary'
              }`}
            >
              {tag}
              <span className="ml-1 opacity-50">{count}</span>
            </button>
          ))}
        </div>
      )}

      {/* Articles */}
      {loading && articles.length === 0 ? (
        <div className="space-y-3">
          {[...Array(6)].map((_, i) => (
            <div
              key={i}
              className="rounded-lg border border-border bg-surface-1 p-5 animate-pulse"
            >
              <div className="h-3 w-24 bg-surface-3 rounded mb-3" />
              <div className="h-5 w-3/4 bg-surface-3 rounded mb-2" />
              <div className="h-4 w-full bg-surface-3 rounded" />
            </div>
          ))}
        </div>
      ) : (
        <div className="space-y-3">
          {filteredArticles.map((article, i) => (
            <NewsCard key={article.id} article={article} index={i} />
          ))}
        </div>
      )}

      {/* Load more */}
      {!loading && articles.length < total && (
        <div className="mt-6 flex justify-center">
          <button
            onClick={loadMore}
            className="px-5 py-2 text-sm font-mono font-medium text-text-muted hover:text-text-primary border border-border hover:border-border-hover rounded-lg transition-all hover:bg-surface-2"
          >
            Load more
          </button>
        </div>
      )}

      {/* Empty state */}
      {!loading && filteredArticles.length === 0 && (
        <div className="text-center py-16">
          <p className="font-mono text-sm text-text-muted">
            {selectedTag
              ? `No articles tagged "${selectedTag}" found.`
              : 'No articles yet. Run the scraper first.'}
          </p>
        </div>
      )}
    </div>
  )
}
