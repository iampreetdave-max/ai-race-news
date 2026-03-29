import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'AI Race News — Finance',
  description: 'AI funding rounds, IPOs, acquisitions, valuations, and fintech AI deals. Updated daily.',
  openGraph: {
    title: 'AI Race News — Finance Feed',
    description: 'AI funding rounds, IPOs, acquisitions, valuations, and fintech AI deals.',
    url: 'https://ai-race-news.pages.dev/finance',
    siteName: 'AI Race News',
    type: 'website',
  },
  twitter: {
    card: 'summary',
    title: 'AI Race News — Finance',
    description: 'AI funding rounds, IPOs, acquisitions, and fintech deals.',
  },
}

export default function FinanceLayout({ children }: { children: React.ReactNode }) {
  return <>{children}</>
}
