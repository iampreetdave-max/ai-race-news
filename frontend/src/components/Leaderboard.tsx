'use client'

import { useState, useEffect } from 'react'
import { AIModel, ModelsData, PROVIDER_COLORS, getValueScore } from '@/lib/models'

type AudienceType = 'developers' | 'business' | 'finance' | 'research' | 'overall'

const AUDIENCE_CRITERIA: Record<AudienceType, {
  label: string
  sortFn: (a: AIModel, b: AIModel) => number
  description: string
  metrics: { key: string; label: string; getValue: (m: AIModel) => number }[]
}> = {
  overall: {
    label: 'Top 3 AI Models Overall',
    description: 'Highest average across MMLU, HumanEval, MATH, and GPQA',
    sortFn: (a, b) => {
      const avgA = (a.benchmarks.mmlu + a.benchmarks.humaneval + a.benchmarks.math + a.benchmarks.gpqa) / 4
      const avgB = (b.benchmarks.mmlu + b.benchmarks.humaneval + b.benchmarks.math + b.benchmarks.gpqa) / 4
      return avgB - avgA
    },
    metrics: [
      { key: 'mmlu', label: 'MMLU', getValue: (m) => m.benchmarks.mmlu },
      { key: 'code', label: 'Code', getValue: (m) => m.benchmarks.humaneval },
    ],
  },
  developers: {
    label: 'Top 3 AI for Developers',
    description: 'Best for coding — ranked by HumanEval + MATH + reasoning',
    sortFn: (a, b) => {
      const scoreA = a.benchmarks.humaneval * 3 + a.benchmarks.math * 2 + a.benchmarks.gpqa
      const scoreB = b.benchmarks.humaneval * 3 + b.benchmarks.math * 2 + b.benchmarks.gpqa
      return scoreB - scoreA
    },
    metrics: [
      { key: 'code', label: 'Code', getValue: (m) => m.benchmarks.humaneval },
      { key: 'math', label: 'Math', getValue: (m) => m.benchmarks.math },
    ],
  },
  business: {
    label: 'Top 3 AI for Business',
    description: 'Best for business — ranked by knowledge, conversation, and reasoning',
    sortFn: (a, b) => {
      const scoreA = a.benchmarks.mmlu * 2 + a.benchmarks.mt_bench * 15 + a.benchmarks.humaneval
      const scoreB = b.benchmarks.mmlu * 2 + b.benchmarks.mt_bench * 15 + b.benchmarks.humaneval
      return scoreB - scoreA
    },
    metrics: [
      { key: 'mmlu', label: 'MMLU', getValue: (m) => m.benchmarks.mmlu },
      { key: 'chat', label: 'Chat', getValue: (m) => m.benchmarks.mt_bench },
    ],
  },
  finance: {
    label: 'Top 3 AI for Finance',
    description: 'Best for finance — ranked by math, PhD-level reasoning, and accuracy',
    sortFn: (a, b) => {
      const scoreA = a.benchmarks.math * 3 + a.benchmarks.gpqa * 2 + a.benchmarks.mmlu
      const scoreB = b.benchmarks.math * 3 + b.benchmarks.gpqa * 2 + b.benchmarks.mmlu
      return scoreB - scoreA
    },
    metrics: [
      { key: 'math', label: 'Math', getValue: (m) => m.benchmarks.math },
      { key: 'gpqa', label: 'GPQA', getValue: (m) => m.benchmarks.gpqa },
    ],
  },
  research: {
    label: 'Top 3 AI for Research',
    description: 'Best for research — ranked by PhD-level science, math, and depth',
    sortFn: (a, b) => {
      const scoreA = a.benchmarks.gpqa * 3 + a.benchmarks.math * 2 + a.benchmarks.mmlu
      const scoreB = b.benchmarks.gpqa * 3 + b.benchmarks.math * 2 + b.benchmarks.mmlu
      return scoreB - scoreA
    },
    metrics: [
      { key: 'gpqa', label: 'GPQA', getValue: (m) => m.benchmarks.gpqa },
      { key: 'math', label: 'Math', getValue: (m) => m.benchmarks.math },
    ],
  },
}

const MEDAL = ['\ud83e\udd47', '\ud83e\udd48', '\ud83e\udd49']

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
    <div className="relative">
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
        <div className="absolute right-0 top-full mt-2 z-50 w-[420px] sm:w-[520px] rounded-lg border border-accent-amber/20 bg-surface-1 shadow-2xl shadow-black/40 animate-slide-up">
          {/* Header with close button */}
          <div className="flex items-start justify-between p-4 border-b border-border">
            <div>
              <h3 className="font-display text-sm font-bold text-text-primary">{criteria.label}</h3>
              <p className="text-[11px] text-text-muted mt-0.5">{criteria.description}</p>
            </div>
            <button
              onClick={() => setOpen(false)}
              className="p-1 rounded hover:bg-surface-3 text-text-muted hover:text-text-primary transition-colors -mt-1 -mr-1"
            >
              <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          {/* Models */}
          <div className="divide-y divide-border/50">
            {top3.map((model, i) => {
              const color = PROVIDER_COLORS[model.provider] || '#71717a'
              return (
                <div key={model.id} className="flex items-center gap-3 p-4 hover:bg-surface-2 transition-colors">
                  <span className="text-lg w-7 text-center flex-shrink-0">{MEDAL[i]}</span>

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
                    <div className="flex items-center gap-2 mt-1 text-[11px] font-mono text-text-muted">
                      <span>{model.provider}</span>
                      <span className="text-border">&middot;</span>
                      <span>${(model.pricing.input + model.pricing.output).toFixed(2)}/1M</span>
                      <span className="text-border">&middot;</span>
                      <span>
                        {model.context_window >= 1000000
                          ? `${(model.context_window / 1000000).toFixed(0)}M ctx`
                          : `${(model.context_window / 1000).toFixed(0)}K ctx`}
                      </span>
                    </div>
                  </div>

                  <div className="flex items-center gap-3 flex-shrink-0">
                    {criteria.metrics.map((metric) => (
                      <div key={metric.key} className="text-center">
                        <p className="text-[9px] font-mono text-text-muted uppercase">{metric.label}</p>
                        <p className="text-sm font-display font-bold" style={{ color }}>
                          {metric.getValue(model)}
                        </p>
                      </div>
                    ))}
                  </div>
                </div>
              )
            })}
          </div>
        </div>
      )}
    </div>
  )
}
