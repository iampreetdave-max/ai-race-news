export default function Footer() {
  return (
    <footer className="border-t border-border">
      {/* CTA Banner */}
      <div className="bg-gradient-to-r from-surface-1 via-surface-2 to-surface-1">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 py-10 sm:py-14">
          <div className="flex flex-col md:flex-row items-center justify-between gap-8">
            {/* LinkedIn CTA */}
            <div className="flex-1 max-w-lg text-center md:text-left">
              <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-accent-amber/20 bg-accent-amber/5 mb-4">
                <span className="font-mono text-[11px] text-accent-amber tracking-wide">
                  AUTOMATE YOUR PRESENCE
                </span>
              </div>
              <h2 className="font-display text-lg sm:text-xl font-bold text-text-primary mb-2">
                Want to stay more relevant?
              </h2>
              <p className="text-sm text-text-secondary leading-relaxed mb-5">
                For <span className="font-semibold text-accent-amber">$20/month</span>,
                get automated LinkedIn content posting powered by the latest AI news.
                Custom posts crafted from real-time industry updates — so your profile
                stays active while you focus on what matters.
              </p>
              <div className="flex flex-col sm:flex-row items-center gap-3">
                <a
                  href="https://forms.gle/wUjcRChCbuqygZ52A"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-2 px-5 py-2.5 rounded-lg bg-accent-amber text-surface-0 font-display text-sm font-semibold hover:bg-accent-amber/90 transition-all hover:shadow-lg hover:shadow-accent-amber/20"
                >
                  Get Started — $20/mo
                  <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                    <path strokeLinecap="round" strokeLinejoin="round" d="M13.5 4.5L21 12m0 0l-7.5 7.5M21 12H3" />
                  </svg>
                </a>
                <a
                  href="https://forms.gle/wUjcRChCbuqygZ52A"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-2 px-5 py-2.5 rounded-lg border border-border hover:border-border-hover text-text-secondary hover:text-text-primary font-display text-sm font-medium transition-all hover:bg-surface-2"
                >
                  <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                    <path strokeLinecap="round" strokeLinejoin="round" d="M21.75 6.75v10.5a2.25 2.25 0 01-2.25 2.25h-15a2.25 2.25 0 01-2.25-2.25V6.75m19.5 0A2.25 2.25 0 0019.5 4.5h-15a2.25 2.25 0 00-2.25 2.25m19.5 0v.243a2.25 2.25 0 01-1.07 1.916l-7.5 4.615a2.25 2.25 0 01-2.36 0L3.32 8.91a2.25 2.25 0 01-1.07-1.916V6.75" />
                  </svg>
                  Subscribe to Newsletter — Free
                </a>
              </div>
            </div>

            {/* Feature list */}
            <div className="flex-shrink-0">
              <div className="rounded-lg border border-border bg-surface-1 p-5 w-[280px]">
                <p className="font-mono text-[11px] text-accent-cyan uppercase tracking-wider mb-3">
                  What you get
                </p>
                <ul className="space-y-2.5 text-[13px] text-text-secondary">
                  {[
                    'Daily AI news posts on your LinkedIn',
                    'Custom tone & style matching',
                    'Trending topics from 110+ sources',
                    'Schedule posts at optimal times',
                    'Edit before publishing',
                    'Cancel anytime',
                  ].map((item) => (
                    <li key={item} className="flex items-start gap-2">
                      <span className="text-accent-cyan mt-0.5 text-xs">✓</span>
                      {item}
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Bottom bar */}
      <div className="bg-surface-0 border-t border-border">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 py-5">
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
                href="https://forms.gle/wUjcRChCbuqygZ52A"
                target="_blank"
                rel="noopener noreferrer"
                className="hover:text-accent-amber transition-colors"
              >
                LinkedIn Automation
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
      </div>
    </footer>
  )
}
