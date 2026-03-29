import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'AI Race News — Research',
  description: 'AI research papers, benchmarks, breakthroughs, and academic findings from arXiv and top labs.',
  openGraph: {
    title: 'AI Race News — Research Feed',
    description: 'AI research papers, benchmarks, and breakthroughs from arXiv and top labs.',
    url: 'https://ai-race-news.pages.dev/research',
    siteName: 'AI Race News',
    type: 'website',
  },
  twitter: {
    card: 'summary',
    title: 'AI Race News — Research',
    description: 'AI research papers, benchmarks, and breakthroughs from arXiv and top labs.',
  },
}

export default function ResearchLayout({ children }: { children: React.ReactNode }) {
  return <>{children}</>
}
