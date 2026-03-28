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
  const hasImage = article.image_url && !article.image_url.includes('pixel')

  return (
    <a
      href={article.url}
      target="_blank"
      rel="noopener noreferrer"
      className="group block animate-slide-up"
      style={{ animationDelay: `${index * 40}ms`, animationFillMode: 'backwards' }}
    >
      <article
        className={`
          relative overflow-hidden rounded-lg border border-border
          bg-surface-1 hover:bg-surface-2 hover:border-border-hover
          transition-all duration-300
          ${hasImage ? 'grid grid-cols-1 sm:grid-cols-[1fr_180px]' : ''}
        `}
      >
        {/* Content */}
        <div className="p-4 sm:p-5 flex flex-col gap-3">
          {/* Meta row */}
          <div className="flex items-center gap-2 text-[11px] font-mono text-text-muted">
            <span className="text-accent-cyan/70">{article.source_name}</span>
            <span className="text-border">·</span>
            {article.published_at && (
              <span>{timeAgo(article.published_at)}</span>
            )}
          </div>

          {/* Title */}
          <h3 className="font-body text-[15px] sm:text-base font-semibold leading-snug text-text-primary group-hover:text-accent-cyan transition-colors line-clamp-2">
            {article.title}
          </h3>

          {/* Summary */}
          {article.summary && (
            <p className="text-[13px] leading-relaxed text-text-secondary line-clamp-2">
              {article.summary}
            </p>
          )}

          {/* Tags */}
          {article.tags.length > 0 && (
            <div className="flex flex-wrap gap-1.5 mt-auto pt-1">
              {article.tags.slice(0, 3).map((tag) => (
                <span
                  key={tag}
                  className={`tag-pill ${TAG_CLASSES[tag] || 'tag-default'}`}
                >
                  {tag}
                </span>
              ))}
            </div>
          )}
        </div>

        {/* Image */}
        {hasImage && (
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
        <div className="absolute left-0 top-0 bottom-0 w-[2px] bg-accent-cyan scale-y-0 group-hover:scale-y-100 transition-transform duration-300 origin-top" />
      </article>
    </a>
  )
}
