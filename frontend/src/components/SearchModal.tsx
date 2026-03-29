'use client'
import { useState, useEffect, useRef } from 'react'
import Fuse from 'fuse.js'
import { useSearch } from '@/lib/SearchContext'
import { Article } from '@/lib/types'

function timeAgo(dateStr: string | null): string {
  if (!dateStr) return ''
  const d = /[Z+]/.test(dateStr) ? dateStr : dateStr + 'Z'
  const diff = Date.now() - new Date(d).getTime()
  const m = Math.floor(diff / 60000)
  if (m < 60) return `${m}m ago`
  const h = Math.floor(m / 60)
  if (h < 24) return `${h}h ago`
  return `${Math.floor(h / 24)}d ago`
}

export default function SearchModal() {
  const { isOpen, close, articles } = useSearch()
  const [query, setQuery] = useState('')
  const [results, setResults] = useState<Article[]>([])
  const inputRef = useRef<HTMLInputElement>(null)
  const fuseRef = useRef<Fuse<Article> | null>(null)

  useEffect(() => {
    if (articles.length > 0) {
      fuseRef.current = new Fuse(articles, {
        keys: ['title', 'summary', 'tags', 'source_name'],
        threshold: 0.4,
        includeScore: true,
      })
    }
  }, [articles])

  useEffect(() => {
    if (isOpen) {
      setTimeout(() => inputRef.current?.focus(), 50)
      setQuery('')
      setResults(articles.slice(0, 8))
    }
  }, [isOpen, articles])

  useEffect(() => {
    if (!query.trim()) {
      setResults(articles.slice(0, 8))
      return
    }
    const r = fuseRef.current?.search(query).slice(0, 8).map(r => r.item) ?? []
    setResults(r)
  }, [query, articles])

  if (!isOpen) return null

  return (
    <div
      className="fixed inset-0 z-[100] flex items-start justify-center pt-[15vh] px-4"
      onClick={close}
    >
      <div className="absolute inset-0 bg-black/60 backdrop-blur-sm" />
      <div
        className="relative w-full max-w-2xl bg-surface-1 border border-border rounded-xl shadow-2xl overflow-hidden"
        onClick={e => e.stopPropagation()}
      >
        <div className="flex items-center gap-3 px-4 py-3 border-b border-border">
          <svg className="w-4 h-4 text-text-muted shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z" />
          </svg>
          <input
            ref={inputRef}
            value={query}
            onChange={e => setQuery(e.target.value)}
            placeholder="Search AI news..."
            className="flex-1 bg-transparent text-sm text-text-primary placeholder:text-text-muted outline-none"
          />
          <kbd className="hidden sm:inline-flex items-center px-1.5 py-0.5 text-[10px] font-mono text-text-muted border border-border rounded">
            ESC
          </kbd>
        </div>

        <div className="max-h-[60vh] overflow-y-auto">
          {results.length === 0 ? (
            <p className="text-center text-text-muted text-sm py-8">No results found</p>
          ) : (
            <ul>
              {results.map(a => (
                <li key={String(a.id)}>
                  <a
                    href={a.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    onClick={close}
                    className="flex flex-col gap-1 px-4 py-3 hover:bg-surface-2 transition-colors border-b border-border/50 last:border-0"
                  >
                    <div className="flex items-center gap-2 text-[11px] font-mono text-text-muted">
                      <span className="text-accent-cyan/70">{a.source_name}</span>
                      {a.published_at && (
                        <>
                          <span className="text-border">&middot;</span>
                          <span>{timeAgo(a.published_at)}</span>
                        </>
                      )}
                      {(a.trending_sources ?? 0) >= 2 && (
                        <span className="text-accent-amber">&#128293; {a.trending_sources} sources</span>
                      )}
                    </div>
                    <p className="text-sm font-medium text-text-primary line-clamp-1">{a.title}</p>
                    {a.tags.length > 0 && (
                      <div className="flex gap-1 flex-wrap">
                        {a.tags.slice(0, 3).map(t => (
                          <span key={t} className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-surface-0 border border-border text-text-muted">
                            {t}
                          </span>
                        ))}
                      </div>
                    )}
                  </a>
                </li>
              ))}
            </ul>
          )}
        </div>

        <div className="px-4 py-2 border-t border-border text-[11px] font-mono text-text-muted">
          {query
            ? `${results.length} results`
            : `Showing ${results.length} recent \u00b7 Type to search all ${articles.length}`}
        </div>
      </div>
    </div>
  )
}
