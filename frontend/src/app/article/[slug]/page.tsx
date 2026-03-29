import { readFileSync } from 'fs'
import { join } from 'path'
import { notFound } from 'next/navigation'
import { Metadata } from 'next'
import { Article } from '@/lib/types'

function getArticles(): Article[] {
  try {
    const raw = readFileSync(join(process.cwd(), 'public/data/articles.json'), 'utf-8')
    return JSON.parse(raw).articles || []
  } catch {
    return []
  }
}

function articleSlug(a: Article): string {
  return a.slug ?? String(a.id)
}

function formatDate(dateStr: string | null): string {
  if (!dateStr) return ''
  const d = /[Z+]/.test(dateStr) ? dateStr : dateStr + 'Z'
  return new Date(d).toLocaleDateString('en-US', {
    year: 'numeric', month: 'long', day: 'numeric',
  })
}

export async function generateStaticParams() {
  const articles = getArticles()
  return articles
    .filter(a => a.slug)
    .map(a => ({ slug: a.slug as string }))
}

export async function generateMetadata(
  { params }: { params: { slug: string } }
): Promise<Metadata> {
  const article = getArticles().find(a => articleSlug(a) === params.slug)
  if (!article) return {}
  return {
    title: `${article.title} | AI Race News`,
    description: article.summary?.slice(0, 160) ?? undefined,
    openGraph: {
      title: article.title,
      description: article.summary?.slice(0, 160) ?? undefined,
      url: `/article/${params.slug}`,
      type: 'article',
      images: article.image_url ? [{ url: article.image_url }] : [],
    },
    twitter: {
      card: 'summary_large_image',
      title: article.title,
      description: article.summary?.slice(0, 160) ?? undefined,
    },
  }
}

export default function ArticlePage({ params }: { params: { slug: string } }) {
  const articles = getArticles()
  const article = articles.find(a => articleSlug(a) === params.slug)
  if (!article) notFound()

  const related = articles
    .filter(a => a.id !== article.id && a.tags.some(t => article.tags.includes(t)))
    .slice(0, 3)

  return (
    <div className="mx-auto max-w-3xl px-4 sm:px-6 py-8 sm:py-12">
      {/* Breadcrumb */}
      <nav className="flex items-center gap-2 text-[12px] font-mono text-text-muted mb-8">
        <a href="/" className="hover:text-accent-cyan transition-colors">Home</a>
        <span className="text-border">/</span>
        <span className="text-text-secondary truncate">{article.source_name}</span>
      </nav>

      {/* Tags */}
      {article.tags.length > 0 && (
        <div className="flex flex-wrap gap-1.5 mb-4">
          {article.tags.map(t => (
            <span key={t} className="text-[11px] font-mono px-2 py-0.5 rounded-full bg-surface-1 border border-border text-text-muted">
              {t}
            </span>
          ))}
        </div>
      )}

      {/* Title */}
      <h1 className="font-display text-2xl sm:text-3xl font-bold leading-tight text-text-primary mb-4">
        {article.title}
      </h1>

      {/* Meta */}
      <div className="flex flex-wrap items-center gap-2 text-[12px] font-mono text-text-muted mb-6">
        <span className="text-accent-cyan/70">{article.source_name}</span>
        {article.published_at && (
          <>
            <span className="text-border">&middot;</span>
            <span>{formatDate(article.published_at)}</span>
          </>
        )}
        {article.author && (
          <>
            <span className="text-border">&middot;</span>
            <span>{article.author}</span>
          </>
        )}
        {(article.trending_sources ?? 0) >= 2 && (
          <>
            <span className="text-border">&middot;</span>
            <span className="text-accent-amber">&#128293; Trending &middot; {article.trending_sources} sources</span>
          </>
        )}
      </div>

      {/* Image */}
      {article.image_url && (
        <div className="mb-6 rounded-xl overflow-hidden border border-border">
          <img src={article.image_url} alt="" className="w-full object-cover max-h-80" />
        </div>
      )}

      {/* Summary */}
      {article.summary && (
        <div className="mb-8">
          <p className="text-base leading-relaxed text-text-secondary">{article.summary}</p>
        </div>
      )}

      {/* CTA */}
      <a
        href={article.url}
        target="_blank"
        rel="noopener noreferrer"
        className="inline-flex items-center gap-2 px-5 py-2.5 rounded-lg bg-accent-cyan/10 border border-accent-cyan/30 text-accent-cyan font-mono text-sm hover:bg-accent-cyan/20 transition-colors mb-10"
      >
        Read full article on {article.source_name}
        <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
          <path strokeLinecap="round" strokeLinejoin="round" d="M13.5 6H5.25A2.25 2.25 0 003 8.25v10.5A2.25 2.25 0 005.25 21h10.5A2.25 2.25 0 0018 18.75V10.5m-10.5 6L21 3m0 0h-5.25M21 3v5.25" />
        </svg>
      </a>

      {/* Related */}
      {related.length > 0 && (
        <div>
          <h2 className="font-display text-lg font-bold text-text-primary mb-4">Related Stories</h2>
          <div className="flex flex-col gap-3">
            {related.map(a => (
              <a
                key={String(a.id)}
                href={`/article/${articleSlug(a)}`}
                className="group flex gap-4 p-3 rounded-lg border border-border bg-surface-1 hover:border-border-hover hover:bg-surface-2 transition-all"
              >
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium text-text-primary group-hover:text-accent-cyan transition-colors line-clamp-2">
                    {a.title}
                  </p>
                  <p className="text-[11px] font-mono text-text-muted mt-1">
                    {a.source_name} &middot; {formatDate(a.published_at)}
                  </p>
                </div>
              </a>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
