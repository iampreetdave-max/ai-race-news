import type { Metadata } from 'next'
import Header from '@/components/Header'
import Footer from '@/components/Footer'
import { SearchProvider } from '@/lib/SearchContext'
import SearchModal from '@/components/SearchModal'
import './globals.css'

export const metadata: Metadata = {
  title: 'AI Race News \u2014 Real-time AI, ML & Data Intelligence',
  description:
    'AI/ML news aggregated from 110+ sources, filtered for developers, business, finance, and researchers. Track the AI race in real-time.',
  metadataBase: new URL('https://ai-race-news.pages.dev'),
  openGraph: {
    title: 'AI Race News \u2014 Real-time AI Intelligence',
    description:
      'AI/ML news from 110+ sources. Filtered feeds for developers, business, finance, and researchers.',
    url: 'https://ai-race-news.pages.dev',
    siteName: 'AI Race News',
    type: 'website',
  },
  twitter: {
    card: 'summary',
    title: 'AI Race News',
    description: 'Real-time AI/ML news from 110+ sources. Feeds for devs, business, finance & research.',
  },
  alternates: {
    types: {
      'application/atom+xml': [
        { url: '/feed.xml', title: 'AI Race News' },
        { url: '/feed-developers.xml', title: 'AI Race News \u2014 Developers' },
        { url: '/feed-business.xml', title: 'AI Race News \u2014 Business' },
        { url: '/feed-finance.xml', title: 'AI Race News \u2014 Finance' },
        { url: '/feed-research.xml', title: 'AI Race News \u2014 Research' },
      ],
    },
  },
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className="dark">
      <body className="min-h-screen flex flex-col">
        <SearchProvider>
          <div className="noise-overlay" />
          <Header />
          <main className="flex-1">{children}</main>
          <Footer />
          <SearchModal />
        </SearchProvider>
      </body>
    </html>
  )
}
