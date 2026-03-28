'use client'

import NewsFeed from '@/components/NewsFeed'

export default function BusinessPage() {
  return (
    <section className="mx-auto max-w-7xl px-4 sm:px-6 py-8 sm:py-12">
      <NewsFeed
        audience="business"
        title="Business"
        description="Product launches, strategy, adoption, partnerships, and market moves"
        accentColor="accent-violet"
        icon="%%"
      />
    </section>
  )
}
