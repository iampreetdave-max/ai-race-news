'use client'

import NewsFeed from '@/components/NewsFeed'

export default function ResearchPage() {
  return (
    <section className="mx-auto max-w-7xl px-4 sm:px-6 py-8 sm:py-12">
      <NewsFeed
        audience="research"
        title="Research"
        description="Papers, benchmarks, SOTA results, and academic breakthroughs"
        accentColor="accent-blue"
        icon="??"
      />
    </section>
  )
}
