'use client'

import { useState } from 'react'
import { Article } from '@/lib/types'

const TAG_CLASSES: Record<string, string> = {
  llm: 'tag-llm',
  funding: 'tag-funding',
  research: 'tag-research',
  tutorial: 'tag-tutorial',
  'open-source': 'tag-open-source',
  'product-launch': 'tag-product-launch',
  hardware: 'tag-hardware',
  regulation: 'tag-regulation',
  agents: 'tag-agents',
  rag: 'tag-rag',
  data: 'tag-data',
  'finance-ai': 'tag-finance-ai',
  robotics: 'tag-robotics',
  'computer-vision': 'tag-computer-vision',
}

function timeAgo(dateStr: string): string {
  const date = new Date(dateStr)
  const now = new Date()
  const seconds = Math.floor((now.getTime() - date.getTime()) / 1000)
  if (seconds < 60) return 'just now'
  if (seconds < 3600) return `${Math.floor(seconds / 60)}m ago`
  if (seconds < 86400) return `${Math.floor(seconds / 3600)}h ago`
  if (seconds < 604800) return `${Math.floor(seconds / 86400)}d ago`
  return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
}

export default function NewsCard({
  article,
  index = 0,
}: {
  article: Article
  index?: number
}) {
  const [expanded, setExpanded] = useState(false)
  const [imgError, setImgError] = useState(false)

  const hasImage = !imgError && !!article.image_url && !article.image_url.includes('pixel')
  const isTrending = (article.trending_sources ?? 0) >= 2

  return (
    <div
      className="group block animate-slide-up"
      style={{ animationDelay: `${index * 40}ms`, animationFillMode: 'backwards' }}
    >
      <article
        onClick={() => setExpanded(!expanded)}
        className={[
          'relative overflow-hidden rounded-lg border cursor-pointer transition-all duration-300',
          expanded
            ? 'border-accent-cyan/30 bg-surface-2'
            : 'border-border bg-surface-1 hover:bg-surface-2 hover:border-border-hover',
          hasImage && !expanded ? 'grid grid-cols-1 sm:grid-cols-[1fr_180px]' : '',
        ].join(' ')}
      >
        <div className="p-4 sm:p-5 flex flex-col gap-3">

          {isTrending && (
            <div>
              <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-mono font-semibold bg-accent-amber/10 text-accent-amber border border-accent-amber/20">
                <svg className="w-2.5 h-2.5" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M12.395 2.553a1 1 0 00-1.45-.385c-.345.23-.614.558-.822.88-.214.33-.403.713-.57 1.116-.334.804-.614 1.768-.84 2.734a31.365 31.365 0 00-.613 3.58 2.64 2.64 0 01-.945-1.067c-.328-.68-.398-1.534-.398-2.654A1 1 0 005.05 6.05 6.981 6.981 0 003 11a7 7 0 1011.95-4.95c-.592-.591-.98-.985-1.348-1.467-.363-.476-.724-1.063-1.207-2.03zM12.12 15.12A3 3 0 017 13s.879.5 2.5.5c0-1 .5-4 1.25-4.5.5 1 .786 1.293 1.371 1.879A2.99 2.99 0 0113 13a2.99 2.99 0 01-.879 2.121z" clipRule="evenodd" />
                </svg>
                Trending &middot; {article.trending_sources} sources
              </span>
            </div>
          )}

          <div className="flex items-center gap-2 text-[11px] font-mono text-text-muted">
            <span className="text-accent-cyan/70">{article.source_name}</span>
            <span className="text-border">&middot;</span>
            {article.published_at && <span>{timeAgo(article.published_at)}</span>}
            {article.author && (
              <>
                <span className="text-border">&middot;</span>
                <span>{article.author}</span>
              </>
            )}
          </div>

          <h3 className={[
            'font-body text-[15px] sm:text-base font-semibold leading-snug text-text-primary transition-colors',
            expanded ? 'text-accent-cyan' : 'group-hover:text-accent-cyan',
            expanded ? '' : 'line-clamp-2',
          ].join(' ')}>
            {article.title}
          </h3>

          {article.summary && (
            <p className={`text-[13px] leading-relaxed text-text-secondary ${expanded ? '' : 'line-clamp-2'}`}>
              {article.summary}
            </p>
          )}

          {article.tags.length > 0 && (
            <div className="flex flex-wrap gap-1.5 mt-auto pt-1">
              {article.tags.slice(0, expanded ? 10 : 3).map((tag) => (
                <span key={tag} className={`tag-pill ${TAG_CLASSES[tag] || 'tag-default'}`}>
                  {tag}
                </span>
              ))}
            </div>
          )}

          {expanded && (
            <div className="flex items-center gap-3 pt-2 border-t border-border mt-1">
              <a
                href={article.url}
                target="_blank"
                rel="noopener noreferrer"
                onClick={(e) => e.stopPropagation()}
                className="inline-flex items-center gap-1.5 text-[12px] font-mono text-accent-cyan hover:text-accent-cyan/80 transition-colors"
              >
                Read full article
                <svg className="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M13.5 6H5.25A2.25 2.25 0 003 8.25v10.5A2.25 2.25 0 005.25 21h10.5A2.25 2.25 0 0018 18.75V10.5m-10.5 6L21 3m0 0h-5.25M21 3v5.25" />
                </svg>
              </a>
              <span className="text-[11px] text-text-muted">{article.source_name}</span>
            </div>
          )}
        </div>

        {hasImage && !expanded && (
          <div className="hidden sm:block relative overflow-hidden">
            <div className="absolute inset-0 bg-gradient-to-r from-surface-1 to-transparent z-10 w-8" />
            <img
              src={article.image_url!}
              alt=""
              className="h-full w-full object-cover opacity-60 group-hover:opacity-80 group-hover:scale-105 transition-all duration-500"
              loading="lazy"
              onError={() => setImgError(true)}
            />
          </div>
        )}

        <div className={[
          'absolute left-0 top-0 bottom-0 w-[2px] bg-accent-cyan transition-transform duration-300 origin-top',
          expanded ? 'scale-y-100' : 'scale-y-0 group-hover:scale-y-100',
        ].join(' ')} />
      </article>
    </div>
  )
}
