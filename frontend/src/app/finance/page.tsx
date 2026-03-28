'use client'

import NewsFeed from '@/components/NewsFeed'

export default function FinancePage() {
  return (
    <section className="mx-auto max-w-7xl px-4 sm:px-6 py-8 sm:py-12">
      <NewsFeed
        audience="finance"
        title="Finance"
        description="Funding rounds, IPOs, valuations, M&A, and the money behind AI"
        accentColor="accent-amber"
        icon="$$"
      />
    </section>
  )
}
