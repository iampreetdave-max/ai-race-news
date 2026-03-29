'use client'

import Link from 'next/link'
import NewsFeed from '@/components/NewsFeed'
import Leaderboard from '@/components/Leaderboard'
import TopStoriesHero from '@/components/TopStoriesHero'
import { AUDIENCE_CONFIG, Audience } from '@/lib/types'

const AUDIENCES: Audience[] = ['developers', 'business', 'finance', 'research']

export default function HomePage() {
  return (
    <div>
      {/* Hero */}
      <section className="relative overflow-hidden border-b border-border">
        <div className="absolute inset-0 bg-grid-pattern bg-grid opacity-[0.03]" />
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[600px] h-[300px] bg-gradient-radial from-accent-cyan/8 via-transparent to-transparent" />

        <div className="relative mx-auto max-w-7xl px-4 sm:px-6 py-16 sm:py-24">
          <div className="max-w-2xl">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-accent-cyan/20 bg-accent-cyan/5 mb-6">
              <span className="relative flex h-1.5 w-1.5">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-accent-cyan opacity-75" />
                <span className="relative inline-flex rounded-full h-1.5 w-1.5 bg-accent-cyan" />
              </span>
              <span className="text-[11px] font-mono text-accent-cyan tracking-wide">
                LIVE \u2014 110+ SOURCES
              </span>
            </div>

            <h1 className="font-display text-3xl sm:text-5xl font-bold tracking-tight leading-[1.1] mb-4">
              The AI race,
              <br />
              <span className="text-accent-cyan">decoded for you.</span>
            </h1>

            <p className="text-base sm:text-lg text-text-secondary leading-relaxed max-w-lg mb-8">
              Real-time news from 110+ sources. Filtered for how AI
              affects <em>you</em> \u2014 whether you ship code, close deals,
              move capital, or push research.
            </p>

            <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
              {AUDIENCES.map((key) => {
                const config = AUDIENCE_CONFIG[key]
                return (
                  <Link
                    key={key}
                    href={`/${key}`}
                    className="group relative overflow-hidden rounded-lg border border-border hover:border-border-hover bg-surface-1 hover:bg-surface-2 p-3 transition-all duration-200"
                  >
                    <span className={`font-mono text-sm text-${config.color} opacity-60 group-hover:opacity-100 transition-opacity`}>
                      {config.icon}
                    </span>
                    <p className="text-[13px] font-semibold text-text-primary mt-1">
                      {config.label}
                    </p>
                    <p className="text-[11px] text-text-muted mt-0.5 line-clamp-2">
                      {config.description}
                    </p>
                  </Link>
                )
              })}
            </div>
          </div>
        </div>
      </section>

      {/* Top Stories */}
      <TopStoriesHero />

      {/* Latest news feed */}
      <section className="mx-auto max-w-7xl px-4 sm:px-6 py-8 sm:py-12">
        <div className="flex items-center justify-between mb-6">
          <div>
            <div className="flex items-center gap-3 mb-2">
              <span className="font-mono text-lg text-accent-cyan">*</span>
              <h2 className="font-display text-xl sm:text-2xl font-bold tracking-tight">Latest</h2>
            </div>
            <p className="text-sm text-text-muted max-w-xl">Everything from all sources, newest first</p>
          </div>
          <Leaderboard audience="overall" />
        </div>
        <NewsFeed />
      </section>
    </div>
  )
}
