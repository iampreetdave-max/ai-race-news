export default function Footer() {
  return (
    <footer className="border-t border-border">
      {/* CTA Section */}
      <div className="mx-auto max-w-7xl px-4 sm:px-6 py-8">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {/* Paid - LinkedIn Automation */}
          <div className="rounded-lg border border-accent-amber/20 bg-accent-amber/[0.03] p-5">
            <div className="flex items-center gap-2 mb-2">
              <span className="font-mono text-[10px] text-accent-amber uppercase tracking-wider px-1.5 py-0.5 rounded bg-accent-amber/10">
                Pro
              </span>
              <span className="font-mono text-[10px] text-accent-amber">$20/mo</span>
            </div>
            <h3 className="font-display text-sm font-bold text-text-primary mb-1">
              Automate your LinkedIn with AI news
            </h3>
            <p className="text-[12px] text-text-muted leading-relaxed mb-3">
              Daily posts crafted from 110+ sources. Custom tone. Edit before publishing.
            </p>
            <a
              href="https://forms.gle/wUjcRChCbuqygZ52A"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-1.5 px-4 py-2 rounded-md bg-accent-amber text-surface-0 font-display text-[13px] font-semibold hover:bg-accent-amber/90 transition-all"
            >
              Get Started
              <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M13.5 4.5L21 12m0 0l-7.5 7.5M21 12H3" />
              </svg>
            </a>
          </div>

          {/* Free - Newsletter */}
          <div className="rounded-lg border border-border bg-surface-1 p-5">
            <div className="flex items-center gap-2 mb-2">
              <span className="font-mono text-[10px] text-accent-cyan uppercase tracking-wider px-1.5 py-0.5 rounded bg-accent-cyan/10">
                Free
              </span>
            </div>
            <h3 className="font-display text-sm font-bold text-text-primary mb-1">
              Subscribe to our newsletter
            </h3>
            <p className="text-[12px] text-text-muted leading-relaxed mb-3">
              Get the top AI stories delivered to your inbox. No spam, unsubscribe anytime.
            </p>
            <a
              href="https://forms.gle/wUjcRChCbuqygZ52A"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-1.5 px-4 py-2 rounded-md border border-border hover:border-accent-cyan/40 text-text-secondary hover:text-accent-cyan font-display text-[13px] font-medium transition-all hover:bg-accent-cyan/5"
            >
              <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M21.75 6.75v10.5a2.25 2.25 0 01-2.25 2.25h-15a2.25 2.25 0 01-2.25-2.25V6.75m19.5 0A2.25 2.25 0 0019.5 4.5h-15a2.25 2.25 0 00-2.25 2.25m19.5 0v.243a2.25 2.25 0 01-1.07 1.916l-7.5 4.615a2.25 2.25 0 01-2.36 0L3.32 8.91a2.25 2.25 0 01-1.07-1.916V6.75" />
              </svg>
              Subscribe
            </a>
          </div>
        </div>
      </div>

      {/* Bottom bar */}
      <div className="border-t border-border">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 py-4">
          <div className="flex flex-col sm:flex-row items-center justify-between gap-3">
            <div className="flex items-center gap-2">
              <div className="flex h-5 w-5 items-center justify-center rounded bg-accent-cyan/10">
                <span className="font-mono text-[9px] font-bold text-accent-cyan">AI</span>
              </div>
              <span className="font-display text-xs text-text-muted">
                race.news
              </span>
              <span className="text-text-muted/30 text-xs">·</span>
              <span className="text-text-muted text-[11px]">
                110+ sources. Updated daily.
              </span>
            </div>
            <div className="flex items-center gap-4 text-[11px] text-text-muted">
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
      </div>
    </footer>
  )
}
