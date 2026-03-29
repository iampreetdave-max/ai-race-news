'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { useSearch } from '@/lib/SearchContext'

const NAV_ITEMS = [
  { href: '/', label: 'Feed' },
  { href: '/developers', label: 'Developers' },
  { href: '/business', label: 'Business' },
  { href: '/finance', label: 'Finance' },
  { href: '/research', label: 'Research' },
  { href: '/ai-race', label: 'AI Race' },
]

export default function Header() {
  const pathname = usePathname()
  const { open } = useSearch()

  return (
    <header className="sticky top-0 z-50 border-b border-border bg-surface-0/80 backdrop-blur-xl">
      <div className="mx-auto max-w-7xl px-4 sm:px-6">
        <div className="flex h-14 items-center justify-between">
          {/* Logo */}
          <Link href="/" className="flex items-center gap-2.5 group">
            <div className="relative flex h-7 w-7 items-center justify-center rounded-md bg-accent-cyan/10 border border-accent-cyan/20 group-hover:border-accent-cyan/40 transition-colors">
              <span className="font-mono text-xs font-bold text-accent-cyan">AI</span>
            </div>
            <span className="font-display text-sm font-semibold tracking-tight text-text-primary">
              race<span className="text-accent-cyan">.</span>news
            </span>
          </Link>

          {/* Navigation */}
          <nav className="hidden md:flex items-center gap-1">
            {NAV_ITEMS.map((item) => {
              const isActive =
                item.href === '/'
                  ? pathname === '/'
                  : pathname.startsWith(item.href)

              return (
                <Link
                  key={item.href}
                  href={item.href}
                  className={`
                    relative px-3 py-1.5 text-[13px] font-medium rounded-md transition-all duration-200
                    ${isActive
                      ? 'text-accent-cyan bg-accent-cyan/8'
                      : 'text-text-muted hover:text-text-primary hover:bg-surface-2'
                    }
                  `}
                >
                  {item.label}
                  {isActive && (
                    <span className="absolute bottom-0 left-1/2 -translate-x-1/2 w-4 h-px bg-accent-cyan" />
                  )}
                </Link>
              )
            })}
          </nav>

          {/* Right side */}
          <div className="flex items-center gap-2">
            <button
              onClick={open}
              title="Search (Ctrl+K)"
              className="hidden sm:inline-flex items-center gap-1.5 px-3 py-1.5 text-[12px] font-mono font-medium text-text-muted hover:text-text-primary border border-border hover:border-border-hover rounded-md transition-all"
            >
              <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z" />
              </svg>
              Search
              <kbd className="ml-0.5 text-[10px] px-1 border border-border rounded opacity-60">&#8984;K</kbd>
            </button>
            <a
              href={`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/docs`}
              target="_blank"
              rel="noopener noreferrer"
              className="hidden sm:inline-flex items-center gap-1.5 px-3 py-1.5 text-[12px] font-mono font-medium text-text-muted hover:text-text-primary border border-border hover:border-border-hover rounded-md transition-all"
            >
              <span className="text-accent-cyan">&gt;_</span> API
            </a>
          </div>
        </div>

        {/* Mobile nav */}
        <nav className="flex md:hidden items-center gap-1 pb-2 overflow-x-auto scrollbar-none -mx-4 px-4">
          {NAV_ITEMS.map((item) => {
            const isActive =
              item.href === '/'
                ? pathname === '/'
                : pathname.startsWith(item.href)

            return (
              <Link
                key={item.href}
                href={item.href}
                className={`
                  shrink-0 px-3 py-1.5 text-[13px] font-medium rounded-md transition-colors
                  ${isActive
                    ? 'text-accent-cyan bg-accent-cyan/8'
                    : 'text-text-muted hover:text-text-primary'
                  }
                `}
              >
                {item.label}
              </Link>
            )
          })}
          <button
            onClick={open}
            className="shrink-0 ml-auto px-3 py-1.5 text-text-muted hover:text-text-primary"
            aria-label="Search"
          >
            <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z" />
            </svg>
          </button>
        </nav>
      </div>
    </header>
  )
}
