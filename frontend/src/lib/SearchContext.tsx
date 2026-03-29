'use client'
import { createContext, useContext, useState, useEffect, useCallback, ReactNode } from 'react'
import { Article } from './types'

interface SearchContextType {
  isOpen: boolean
  open: () => void
  close: () => void
  articles: Article[]
}

const SearchContext = createContext<SearchContextType>({
  isOpen: false,
  open: () => {},
  close: () => {},
  articles: [],
})

export function SearchProvider({ children }: { children: ReactNode }) {
  const [isOpen, setIsOpen] = useState(false)
  const [articles, setArticles] = useState<Article[]>([])

  useEffect(() => {
    fetch('/data/articles.json')
      .then(r => r.json())
      .then(d => setArticles(d.articles || []))
      .catch(() => {})
  }, [])

  const open = useCallback(() => setIsOpen(true), [])
  const close = useCallback(() => setIsOpen(false), [])

  useEffect(() => {
    function handleKey(e: KeyboardEvent) {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault()
        setIsOpen(v => !v)
      }
      if (e.key === 'Escape') setIsOpen(false)
    }
    window.addEventListener('keydown', handleKey)
    return () => window.removeEventListener('keydown', handleKey)
  }, [])

  return (
    <SearchContext.Provider value={{ isOpen, open, close, articles }}>
      {children}
    </SearchContext.Provider>
  )
}

export const useSearch = () => useContext(SearchContext)
