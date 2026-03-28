'use client'

import NewsFeed from '@/components/NewsFeed'

export default function DevelopersPage() {
  return (
    <section className="mx-auto max-w-7xl px-4 sm:px-6 py-8 sm:py-12">
      <NewsFeed
        audience="developers"
        title="Developers"
        description="Code, APIs, tools, open-source releases, and technical deep-dives"
        accentColor="accent-cyan"
        icon="/>"
      />
    </section>
  )
}
