'use client'

import { useState, useEffect } from 'react'
import { AIModel, ModelsData, PROVIDER_COLORS, getValueScore } from '@/lib/models'

type AudienceType = 'developers' | 'business' | 'finance' | 'research' | 'overall'

const AUDIENCE_CRITERIA: Record<AudienceType, {
  label: string
  sortFn: (a: AIModel, b: AIModel) => number
  description: string
}> = {
  overall: {
    label: 'Top 3 AI Models Overall',
    description: 'Best all-around performance across all benchmarks',
    sortFn: (a, b) => {
      const avgA = (a.benchmarks.mmlu + a.benchmarks.humaneval + a.benchmarks.math + a.benchmarks.gpqa) / 4
      const avgB = (b.benchmarks.mmlu + b.benchmarks.humaneval + b.benchmarks.math + b.benchmarks.gpqa) / 4
      return avgB - avgA
    },
  },
  developers: {
    label: 'Top 3 AI for Developers',
    description: 'Ranked by code generation, value, and open-source availability',
    sortFn: (a, b) => {
      const scoreA = a.benchmarks.humaneval * 2 + a.benchmarks.math + getValueScore(a) * 0.5 + (a.open_source ? 10 : 0)
      const scoreB = b.benchmarks.humaneval * 2 + b.benchmarks.math + getValueScore(b) * 0.5 + (b.open_source ? 10 : 0)
      return scoreB - scoreA
    },
  },
  business: {
    label: 'Top 3 AI for Business',
    description: 'Ranked by reasoning, conversation quality, and cost efficiency',
    sortFn: (a, b) => {
      const scoreA = a.benchmarks.mmlu + a.benchmarks.mt_bench * 10 + getValueScore(a) * 0.3
      const scoreB = b.benchmarks.mmlu + b.benchmarks.mt_bench * 10 + getValueScore(b) * 0.3
      return scoreB - scoreA
    },
  },
  finance: {
    label: 'Top 3 AI for Finance',
    description: 'Ranked by math, reasoning, and knowledge accuracy',
    sortFn: (a, b) => {
      const scoreA = a.benchmarks.math * 2 + a.benchmarks.gpqa + a.benchmarks.mmlu
      const scoreB = b.benchmarks.math * 2 + b.benchmarks.gpqa + b.benchmarks.mmlu
      return scoreB - scoreA
    },
  },
  research: {
    label: 'Top 3 AI for Research',
    description: 'Ranked by PhD-level reasoning, math, and context window',
    sortFn: (a, b) => {
      const scoreA = a.benchmarks.gpqa * 2 + a.benchmarks.math + Math.log10(a.context_window) * 5
      const scoreB = b.benchmarks.gpqa * 2 + b.benchmarks.math + Math.log10(b.context_window) * 5
      return scoreB - scoreA
    },
  },
}

const MEDAL = ['\u{1F947}', '\u{1F948}', '\u{1F949}']

export default function Leaderboard({ audience = 'overall' }: { audience?: AudienceType }) {
  const [open, setOpen] = useState(false)
  const [models, setModels] = useState<AIModel[]>([])

  useEffect(() => {
    fetch('/data/models.json')
      .then((r) => r.json())
      .then((d: ModelsData) => setModels(d.models))
      .catch(() => {})
  }, [])

  const criteria = AUDIENCE_CRITERIA[audience]
  const top3 = [...models].sort(criteria.sortFn).slice(0, 3)

  if (models.length === 0) return null

  return (
    <>
      <button
        onClick={() => setOpen(!open)}
        className={`
          inline-flex items-center gap-1.5 px-3 py-1.5 rounded-md text-[12px] font-mono font-medium
          transition-all
          ${open
            ? 'bg-accent-amber/10 text-accent-amber border border-accent-amber/20'
            : 'text-text-muted hover:text-text-primary border border-border hover:border-border-hover'
          }
        `}
      >
        <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
          <path strokeLinecap="round" strokeLinejoin="round" d="M16.5 18.75h-9m9 0a3 3 0 013 3h-15a3 3 0 013-3m9 0v-4.5A3.375 3.375 0 0012.75 6H11.25A3.375 3.375 0 007.5 9.375v5.25m9 4.125l-2.25-2.25M7.5 18.75l2.25-2.25" />
        </svg>
        Leaderboard
      </button>

      {open && (
        <div className="mt-4 rounded-lg border border-accent-amber/20 bg-surface-1 overflow-hidden animate-slide-up">
          <div className="p-4 border-b border-border">
            <h3 className="font-display text-sm font-bold text-text-primary">{criteria.label}</h3>
            <p className="text-[11px] text-text-muted mt-0.5">{criteria.description}</p>
          </div>

          <div className="divide-y divide-border/50">
            {top3.map((model, i) => {
              const color = PROVIDER_COLORS[model.provider] || '#71717a'
              return (
                <div key={model.id} className="flex items-center gap-4 p-4 hover:bg-surface-2 transition-colors">
                  {/* Rank */}
                  <span className="text-lg w-8 text-center">{MEDAL[i]}</span>

                  {/* Model info */}
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2">
                      <span className="w-2 h-2 rounded-full flex-shrink-0" style={{ backgroundColor: color }} />
                      <span className="font-display text-sm font-bold text-text-primary truncate">
                        {model.name}
                      </span>
                      {model.open_source && (
                        <span className="tag-pill tag-open-source text-[9px]">OSS</span>
                      )}
                    </div>
                    <div className="flex items-center gap-3 mt-1 text-[11px] font-mono text-text-muted">
                      <span>{model.provider}</span>
                      <span className="text-border">\u00b7</span>
                      <span>${(model.pricing.input + model.pricing.output).toFixed(2)}/1M tokens</span>
                      <span className="text-border">\u00b7</span>
                      <span>
                        {model.context_window >= 1000000
                          ? `${(model.context_window / 1000000).toFixed(0)}M ctx`
                          : `${(model.context_window / 1000).toFixed(0)}K ctx`}
                      </span>
                    </div>
                  </div>

                  {/* Key scores */}
                  <div className="hidden sm:flex items-center gap-3">
                    {audience === 'developers' && (
                      <>
                        <div className="text-center">
                          <p className="text-[9px] font-mono text-text-muted uppercase">Code</p>
                          <p className="text-sm font-display font-bold" style={{ color }}>{model.benchmarks.humaneval}</p>
                        </div>
                        <div className="text-center">
                          <p className="text-[9px] font-mono text-text-muted uppercase">Math</p>
                          <p className="text-sm font-display font-bold text-text-secondary">{model.benchmarks.math}</p>
                        </div>
                      </>
                    )}
                    {audience === 'business' && (
                      <>
                        <div className="text-center">
                          <p className="text-[9px] font-mono text-text-muted uppercase">MMLU</p>
                          <p className="text-sm font-display font-bold" style={{ color }}>{model.benchmarks.mmlu}</p>
                        </div>
                        <div className="text-center">
                          <p className="text-[9px] font-mono text-text-muted uppercase">Chat</p>
                          <p className="text-sm font-display font-bold text-text-secondary">{model.benchmarks.mt_bench}</p>
                        </div>
                      </>
                    )}
                    {audience === 'finance' && (
                      <>
                        <div className="text-center">
                          <p className="text-[9px] font-mono text-text-muted uppercase">Math</p>
                          <p className="text-sm font-display font-bold" style={{ color }}>{model.benchmarks.math}</p>
                        </div>
                        <div className="text-center">
                          <p className="text-[9px] font-mono text-text-muted uppercase">GPQA</p>
                          <p className="text-sm font-display font-bold text-text-secondary">{model.benchmarks.gpqa}</p>
                        </div>
                      </>
                    )}
                    {audience === 'research' && (
                      <>
                        <div className="text-center">
                          <p className="text-[9px] font-mono text-text-muted uppercase">GPQA</p>
                          <p className="text-sm font-display font-bold" style={{ color }}>{model.benchmarks.gpqa}</p>
                        </div>
                        <div className="text-center">
                          <p className="text-[9px] font-mono text-text-muted uppercase">Math</p>
                          <p className="text-sm font-display font-bold text-text-secondary">{model.benchmarks.math}</p>
                        </div>
                      </>
                    )}
                    {audience === 'overall' && (
                      <>
                        <div className="text-center">
                          <p className="text-[9px] font-mono text-text-muted uppercase">MMLU</p>
                          <p className="text-sm font-display font-bold" style={{ color }}>{model.benchmarks.mmlu}</p>
                        </div>
                        <div className="text-center">
                          <p className="text-[9px] font-mono text-text-muted uppercase">Code</p>
                          <p className="text-sm font-display font-bold text-text-secondary">{model.benchmarks.humaneval}</p>
                        </div>
                      </>
                    )}
                    <div className="text-center">
                      <p className="text-[9px] font-mono text-text-muted uppercase">Value</p>
                      <p className="text-sm font-display font-bold text-accent-cyan">{getValueScore(model)}</p>
                    </div>
                  </div>
                </div>
              )
            })}
          </div>
        </div>
      )}
    </>
  )
}
