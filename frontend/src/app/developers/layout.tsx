import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'AI Race News — Developers',
  description: 'AI/ML news for developers: new models, APIs, open-source releases, benchmarks, and coding tools.',
  openGraph: {
    title: 'AI Race News — Developers Feed',
    description: 'AI/ML news for developers: new models, APIs, open-source releases, benchmarks, and coding tools.',
    url: 'https://ai-race-news.pages.dev/developers',
    siteName: 'AI Race News',
    type: 'website',
  },
  twitter: {
    card: 'summary',
    title: 'AI Race News — Developers',
    description: 'AI/ML news for developers: new models, APIs, open-source releases, and benchmarks.',
  },
}

export default function DevelopersLayout({ children }: { children: React.ReactNode }) {
  return <>{children}</>
}
