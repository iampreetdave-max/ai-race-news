'use client'

import NewsFeed from '@/components/NewsFeed'
import Leaderboard from '@/components/Leaderboard'

export default function BusinessPage() {
  return (
    <section className="mx-auto max-w-7xl px-4 sm:px-6 py-8 sm:py-12">
      <div className="flex items-center justify-between mb-6">
        <div>
          <div className="flex items-center gap-3 mb-2">
            <span className="font-mono text-lg text-accent-violet">%%</span>
            <h1 className="font-display text-xl sm:text-2xl font-bold tracking-tight">Business</h1>
          </div>
          <p className="text-sm text-text-muted max-w-xl">Product launches, strategy, adoption, partnerships, and market moves</p>
        </div>
        <Leaderboard audience="business" />
      </div>
      <NewsFeed audience="business" />
    </section>
  )
}
