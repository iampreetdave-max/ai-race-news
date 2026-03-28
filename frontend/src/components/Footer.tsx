export default function Footer() {
  return (
    <footer className="border-t border-border bg-surface-1">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 py-8">
        <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-2">
            <div className="flex h-5 w-5 items-center justify-center rounded bg-accent-cyan/10">
              <span className="font-mono text-[9px] font-bold text-accent-cyan">AI</span>
            </div>
            <span className="font-display text-xs text-text-muted">
              race.news
            </span>
            <span className="text-text-muted/40 text-xs">|</span>
            <span className="text-text-muted text-xs">
              110+ sources. Real-time AI news.
            </span>
          </div>

          <div className="flex items-center gap-4 text-xs text-text-muted">
            <a
              href={`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/docs`}
              target="_blank"
              rel="noopener noreferrer"
              className="hover:text-accent-cyan transition-colors"
            >
              API Docs
            </a>
            <a
              href="https://github.com/iampreetdave-max/ai-race-news"
              target="_blank"
              rel="noopener noreferrer"
              className="hover:text-text-primary transition-colors"
            >
              GitHub
            </a>
          </div>
        </div>
      </div>
    </footer>
  )
}
