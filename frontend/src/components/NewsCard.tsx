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
  const hasImage = article.image_url && !article.image_url.includes('pixel')

  return (
    <div
      className="group block animate-slide-up"
      style={{ animationDelay: `${index * 40}ms`, animationFillMode: 'backwards' }}
    >
      <article
        onClick={() => setExpanded(!expanded)}
        className={`
          relative overflow-hidden rounded-lg border cursor-pointer
          transition-all duration-300
          ${expanded
            ? 'border-accent-cyan/30 bg-surface-2'
            : 'border-border bg-surface-1 hover:bg-surface-2 hover:border-border-hover'
          }
          ${hasImage && !expanded ? 'grid grid-cols-1 sm:grid-cols-[1fr_180px]' : ''}
        `}
      >
        {/* Content */}
        <div className="p-4 sm:p-5 flex flex-col gap-3">
          {/* Meta row */}
          <div className="flex items-center gap-2 text-[11px] font-mono text-text-muted">
            <span className="text-accent-cyan/70">{article.source_name}</span>
            <span className="text-border">\u00b7</span>
            {article.published_at && (
              <span>{timeAgo(article.published_at)}</span>
            )}
            {article.author && (
              <>
                <span className="text-border">\u00b7</span>
                <span>{article.author}</span>
              </>
            )}
          </div>

          {/* Title */}
          <h3 className={`
            font-body text-[15px] sm:text-base font-semibold leading-snug text-text-primary
            transition-colors
            ${expanded ? 'text-accent-cyan' : 'group-hover:text-accent-cyan'}
            ${expanded ? '' : 'line-clamp-2'}
          `}>
            {article.title}
          </h3>

          {/* Summary - always show when expanded, 2 lines when collapsed */}
          {article.summary && (
            <p className={`
              text-[13px] leading-relaxed text-text-secondary
              ${expanded ? '' : 'line-clamp-2'}
            `}>
              {article.summary}
            </p>
          )}

          {/* Expanded image */}
          {expanded && hasImage && (
            <div className="rounded-md overflow-hidden mt-1">
              <img
                src={article.image_url!}
                alt=""
                className="w-full max-h-[300px] object-cover rounded-md"
                loading="lazy"
              />
            </div>
          )}

          {/* Tags */}
          {article.tags.length > 0 && (
            <div className="flex flex-wrap gap-1.5 mt-auto pt-1">
              {article.tags.slice(0, expanded ? 10 : 3).map((tag) => (
                <span
                  key={tag}
                  className={`tag-pill ${TAG_CLASSES[tag] || 'tag-default'}`}
                >
                  {tag}
                </span>
              ))}
            </div>
          )}

          {/* Source link - only when expanded */}
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

        {/* Thumbnail - only when collapsed and has image */}
        {hasImage && !expanded && (
          <div className="hidden sm:block relative overflow-hidden">
            <div className="absolute inset-0 bg-gradient-to-r from-surface-1 to-transparent z-10 w-8" />
            <img
              src={article.image_url!}
              alt=""
              className="h-full w-full object-cover opacity-60 group-hover:opacity-80 group-hover:scale-105 transition-all duration-500"
              loading="lazy"
            />
          </div>
        )}

        {/* Hover accent line */}
        <div className={`
          absolute left-0 top-0 bottom-0 w-[2px] bg-accent-cyan transition-transform duration-300 origin-top
          ${expanded ? 'scale-y-100' : 'scale-y-0 group-hover:scale-y-100'}
        `} />
      </article>
    </div>
  )
}
