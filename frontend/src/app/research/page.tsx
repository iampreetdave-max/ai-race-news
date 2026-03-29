'use client'

import NewsFeed from '@/components/NewsFeed'
import Leaderboard from '@/components/Leaderboard'

export default function ResearchPage() {
  return (
    <section className="mx-auto max-w-7xl px-4 sm:px-6 py-8 sm:py-12">
      <div className="flex items-center justify-between mb-6">
        <div>
          <div className="flex items-center gap-3 mb-2">
            <span className="font-mono text-lg text-accent-blue">??</span>
            <h1 className="font-display text-xl sm:text-2xl font-bold tracking-tight">Research</h1>
          </div>
          <p className="text-sm text-text-muted max-w-xl">Papers, benchmarks, SOTA results, and academic breakthroughs</p>
        </div>
        <Leaderboard audience="research" />
      </div>
      <NewsFeed audience="research" />
    </section>
  )
}
