'use client'

import NewsFeed from '@/components/NewsFeed'
import Leaderboard from '@/components/Leaderboard'

export default function FinancePage() {
  return (
    <section className="mx-auto max-w-7xl px-4 sm:px-6 py-8 sm:py-12">
      <div className="flex items-center justify-between mb-6">
        <div>
          <div className="flex items-center gap-3 mb-2">
            <span className="font-mono text-lg text-accent-amber">$$</span>
            <h1 className="font-display text-xl sm:text-2xl font-bold tracking-tight">Finance</h1>
          </div>
          <p className="text-sm text-text-muted max-w-xl">Funding rounds, IPOs, valuations, M&amp;A, and the money behind AI</p>
        </div>
        <Leaderboard audience="finance" />
      </div>
      <NewsFeed audience="finance" />
    </section>
  )
}
