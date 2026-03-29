import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'AI Race News — Business',
  description: 'AI strategy, enterprise adoption, product launches, and market moves. Curated for business leaders.',
  openGraph: {
    title: 'AI Race News — Business Feed',
    description: 'AI strategy, enterprise adoption, product launches, and market moves. Curated for business leaders.',
    url: 'https://ai-race-news.pages.dev/business',
    siteName: 'AI Race News',
    type: 'website',
  },
  twitter: {
    card: 'summary',
    title: 'AI Race News — Business',
    description: 'AI strategy, enterprise adoption, product launches, and market moves.',
  },
}

export default function BusinessLayout({ children }: { children: React.ReactNode }) {
  return <>{children}</>
}
