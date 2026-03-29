'use client'
import { useEffect, useState } from 'react'
import { Article } from '@/lib/types'

function timeAgo(dateStr: string | null): string {
  if (!dateStr) return ''
  const d = /[Z+]/.test(dateStr) ? dateStr : dateStr + 'Z'
  const diff = Date.now() - new Date(d).getTime()
  const h = Math.floor(diff / 3600000)
  if (h < 1) return `${Math.floor(diff / 60000)}m ago`
  if (h < 24) return `${h}h ago`
  return `${Math.floor(h / 24)}d ago`
}

export default function TopStoriesHero() {
  const [articles, setArticles] = useState<Article[]>([])

  useEffect(() => {
    fetch('/data/articles.json')
      .then(r => r.json())
      .then(d => setArticles((d.articles || []).slice(0, 3)))
      .catch(() => {})
  }, [])

  if (articles.length < 3) return null

  const [main, ...rest] = articles

  return (
    <section className="mx-auto max-w-7xl px-4 sm:px-6 py-8 sm:py-10 border-b border-border">
      <div className="flex items-center gap-3 mb-5">
        <span className="font-mono text-lg text-accent-amber">&#9733;</span>
        <h2 className="font-display text-xl sm:text-2xl font-bold tracking-tight">Top Stories</h2>
      </div>
      <div className="grid md:grid-cols-3 gap-4">
        {/* Main large card */}
        <a
          href={main.url}
          target="_blank"
          rel="noopener noreferrer"
          className="md:col-span-2 group relative overflow-hidden rounded-xl border border-border bg-surface-1 hover:border-border-hover transition-all duration-300 min-h-[240px] flex flex-col justify-end"
        >
          {main.image_url && (
            <div className="absolute inset-0">
              <img
                src={main.image_url}
                alt=""
                className="w-full h-full object-cover opacity-20 group-hover:opacity-30 transition-opacity duration-500"
              />
              <div className="absolute inset-0 bg-gradient-to-t from-surface-0 via-surface-0/80 to-transparent" />
            </div>
          )}
          <div className="relative p-5 sm:p-6">
            {(main.trending_sources ?? 0) >= 2 && (
              <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-mono font-semibold bg-accent-amber/10 text-accent-amber border border-accent-amber/20 mb-3">
                &#128293; Trending &middot; {main.trending_sources} sources
              </span>
            )}
            <div className="flex flex-wrap gap-1 mb-3">
              {main.tags.slice(0, 3).map(t => (
                <span key={t} className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-surface-0/80 border border-border text-text-muted">
                  {t}
                </span>
              ))}
            </div>
            <h3 className="font-display text-lg sm:text-xl font-bold text-text-primary leading-snug group-hover:text-accent-cyan transition-colors mb-2 line-clamp-3">
              {main.title}
            </h3>
            <div className="flex items-center gap-2 text-[11px] font-mono text-text-muted">
              <span className="text-accent-cyan/70">{main.source_name}</span>
              <span className="text-border">&middot;</span>
              <span>{timeAgo(main.published_at)}</span>
            </div>
          </div>
        </a>

        {/* 2 smaller stacked cards */}
        <div className="flex flex-col gap-4">
          {rest.map(a => (
            <a
              key={String(a.id)}
              href={a.url}
              target="_blank"
              rel="noopener noreferrer"
              className="group relative overflow-hidden rounded-xl border border-border bg-surface-1 hover:border-border-hover transition-all duration-300 flex-1 flex flex-col justify-end min-h-[110px]"
            >
              {a.image_url && (
                <div className="absolute inset-0">
                  <img
                    src={a.image_url}
                    alt=""
                    className="w-full h-full object-cover opacity-15 group-hover:opacity-25 transition-opacity duration-500"
                  />
                  <div className="absolute inset-0 bg-gradient-to-t from-surface-0 via-surface-0/70 to-transparent" />
                </div>
              )}
              <div className="relative p-4">
                {(a.trending_sources ?? 0) >= 2 && (
                  <span className="inline-flex items-center gap-1 text-[10px] font-mono text-accent-amber mb-1.5">
                    &#128293; {a.trending_sources} sources
                  </span>
                )}
                <h3 className="font-semibold text-sm text-text-primary leading-snug group-hover:text-accent-cyan transition-colors line-clamp-2 mb-1.5">
                  {a.title}
                </h3>
                <div className="flex items-center gap-2 text-[10px] font-mono text-text-muted">
                  <span className="text-accent-cyan/70">{a.source_name}</span>
                  <span className="text-border">&middot;</span>
                  <span>{timeAgo(a.published_at)}</span>
                </div>
              </div>
            </a>
          ))}
        </div>
      </div>
    </section>
  )
}
