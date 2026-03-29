'use client'

import { useState, useEffect } from 'react'
import { AIModel, ModelsData, PROVIDER_COLORS, getValueScore, BENCHMARK_KEYS } from '@/lib/models'
import BenchmarkChart from '@/components/BenchmarkChart'
import CostChart from '@/components/CostChart'
import ModelCard from '@/components/ModelCard'

type FilterCategory = 'all' | 'flagship' | 'mid-tier' | 'budget' | 'reasoning' | 'open-source'
type SortBy = 'performance' | 'cost' | 'value' | 'context'

const BENCHMARK_OPTIONS: { key: string; label: string; maxScore: number }[] = [
  { key: 'mmlu', label: 'MMLU \u2014 Knowledge', maxScore: 100 },
  { key: 'humaneval', label: 'HumanEval \u2014 Code', maxScore: 100 },
  { key: 'math', label: 'MATH \u2014 Mathematics', maxScore: 100 },
  { key: 'gpqa', label: 'GPQA \u2014 PhD Science', maxScore: 100 },
  { key: 'arc_challenge', label: 'ARC-C \u2014 Reasoning', maxScore: 100 },
  { key: 'mt_bench', label: 'MT-Bench \u2014 Conversation', maxScore: 10 },
]

export default function AIRacePage() {
  const [data, setData] = useState<ModelsData | null>(null)
  const [loading, setLoading] = useState(true)
  const [selectedBenchmark, setSelectedBenchmark] = useState('mmlu')
  const [filter, setFilter] = useState<FilterCategory>('all')
  const [sortBy, setSortBy] = useState<SortBy>('performance')

  useEffect(() => {
    fetch('/data/models.json')
      .then((r) => r.json())
      .then((d) => { setData(d); setLoading(false) })
      .catch(() => setLoading(false))
  }, [])

  if (loading) {
    return (
      <div className="mx-auto max-w-7xl px-4 sm:px-6 py-16">
        <div className="animate-pulse space-y-6">
          <div className="h-8 w-48 bg-surface-3 rounded" />
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
            <div className="h-[400px] bg-surface-2 rounded-lg" />
            <div className="h-[400px] bg-surface-2 rounded-lg" />
          </div>
        </div>
      </div>
    )
  }

  if (!data) return null

  const models = data.models

  const filtered = filter === 'all'
    ? models
    : models.filter((m) => m.category === filter)

  const sorted = [...filtered].sort((a, b) => {
    switch (sortBy) {
      case 'performance': {
        const avgA = (a.benchmarks.mmlu + a.benchmarks.humaneval + a.benchmarks.math + a.benchmarks.gpqa) / 4
        const avgB = (b.benchmarks.mmlu + b.benchmarks.humaneval + b.benchmarks.math + b.benchmarks.gpqa) / 4
        return avgB - avgA
      }
      case 'cost':
        return (a.pricing.input + a.pricing.output) - (b.pricing.input + b.pricing.output)
      case 'value':
        return getValueScore(b) - getValueScore(a)
      case 'context':
        return b.context_window - a.context_window
      default:
        return 0
    }
  })

  const bestOverall = [...models].sort((a, b) => {
    const avgA = (a.benchmarks.mmlu + a.benchmarks.humaneval + a.benchmarks.math + a.benchmarks.gpqa) / 4
    const avgB = (b.benchmarks.mmlu + b.benchmarks.humaneval + b.benchmarks.math + b.benchmarks.gpqa) / 4
    return avgB - avgA
  })[0]

  const bestValue = [...models].sort((a, b) => getValueScore(b) - getValueScore(a))[0]

  const cheapest = [...models].sort(
    (a, b) => (a.pricing.input + a.pricing.output) - (b.pricing.input + b.pricing.output)
  )[0]

  const bestOSS = [...models]
    .filter((m) => m.open_source)
    .sort((a, b) => {
      const avgA = (a.benchmarks.mmlu + a.benchmarks.humaneval + a.benchmarks.math) / 3
      const avgB = (b.benchmarks.mmlu + b.benchmarks.humaneval + b.benchmarks.math) / 3
      return avgB - avgA
    })[0]

  const selectedBM = BENCHMARK_OPTIONS.find((b) => b.key === selectedBenchmark)!

  function renderTableRow(m: AIModel) {
    const color = PROVIDER_COLORS[m.provider] || '#71717a'
    return (
      <tr key={m.id} className="border-b border-border/50 hover:bg-surface-2 transition-colors">
        <td className="p-3 text-text-primary font-medium min-w-[160px]">
          <div className="flex items-center gap-2">
            <span className="w-1.5 h-1.5 rounded-full flex-shrink-0" style={{ backgroundColor: color }} />
            <span className="truncate">{m.name}</span>
            {m.open_source && <span className="text-emerald-400 text-[9px] flex-shrink-0">OSS</span>}
          </div>
        </td>
        <td className="p-3 text-right text-text-muted whitespace-nowrap">{m.provider}</td>
        <td className="p-3 text-right text-text-secondary">${m.pricing.input}</td>
        <td className="p-3 text-right text-text-secondary">${m.pricing.output}</td>
        <td className="p-3 text-right text-text-secondary">
          {m.context_window >= 1000000
            ? `${(m.context_window / 1000000).toFixed(0)}M`
            : `${(m.context_window / 1000).toFixed(0)}K`}
        </td>
        <td className="p-3 text-right text-text-secondary">{m.benchmarks.mmlu}</td>
        <td className="p-3 text-right text-text-secondary">{m.benchmarks.humaneval}</td>
        <td className="p-3 text-right text-text-secondary">{m.benchmarks.math}</td>
        <td className="p-3 text-right text-text-secondary">{m.benchmarks.gpqa}</td>
        <td className="p-3 text-right font-medium" style={{ color }}>{getValueScore(m)}</td>
      </tr>
    )
  }

  return (
    <div className="mx-auto max-w-7xl px-4 sm:px-6 py-8 sm:py-12">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-2">
          <span className="font-mono text-lg text-accent-cyan">{'<>'}</span>
          <h1 className="font-display text-xl sm:text-2xl font-bold tracking-tight">
            AI Race
          </h1>
        </div>
        <p className="text-sm text-text-muted max-w-xl">
          Side-by-side comparison of {models.length} AI models across cost, performance, and value.
          Updated {data.last_updated}.
        </p>
      </div>

      {/* Top Picks */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 sm:gap-3 mb-8">
        {[
          { label: 'Best Overall', model: bestOverall, color: '#f59e0b' },
          { label: 'Best Value', model: bestValue, color: '#06d6a0' },
          { label: 'Cheapest', model: cheapest, color: '#3b82f6' },
          { label: 'Best Open Source', model: bestOSS, color: '#ef4444' },
        ].map((pick) => (
          <div
            key={pick.label}
            className="rounded-lg border border-border bg-surface-1 p-3 sm:p-4"
          >
            <p className="text-[10px] font-mono uppercase tracking-wider mb-1"
               style={{ color: pick.color }}>
              {pick.label}
            </p>
            <p className="font-display text-sm font-bold text-text-primary truncate">
              {pick.model.name}
            </p>
            <p className="text-[11px] text-text-muted mt-0.5">
              {pick.model.provider} \u00b7 ${(pick.model.pricing.input + pick.model.pricing.output).toFixed(2)}/1M
            </p>
          </div>
        ))}
      </div>

      {/* Benchmark Charts */}
      <div className="mb-8">
        <div className="flex flex-wrap gap-1.5 mb-4">
          {BENCHMARK_OPTIONS.map((bm) => (
            <button
              key={bm.key}
              onClick={() => setSelectedBenchmark(bm.key)}
              className={`tag-pill transition-all ${
                selectedBenchmark === bm.key
                  ? 'bg-accent-cyan/10 text-accent-cyan'
                  : 'tag-default hover:text-text-primary'
              }`}
            >
              {bm.key === 'arc_challenge' ? 'ARC-C' : bm.key === 'mt_bench' ? 'MT-Bench' : bm.key.toUpperCase()}
            </button>
          ))}
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
          <BenchmarkChart
            models={models}
            benchmarkKey={selectedBenchmark}
            title={selectedBM.label}
            maxScore={selectedBM.maxScore}
          />
          <CostChart models={models} />
        </div>
      </div>

      {/* Provider Legend */}
      <div className="flex flex-wrap gap-3 mb-6 px-1">
        {Object.entries(PROVIDER_COLORS).map(([provider, color]) => (
          <span key={provider} className="flex items-center gap-1.5 text-[11px] font-mono text-text-muted">
            <span className="w-2.5 h-2.5 rounded-sm" style={{ backgroundColor: color }} />
            {provider}
          </span>
        ))}
      </div>

      {/* Filters + Sort */}
      <div className="flex flex-wrap items-center gap-4 mb-5">
        <div className="flex flex-wrap gap-1.5">
          {(['all', 'flagship', 'mid-tier', 'budget', 'reasoning', 'open-source'] as FilterCategory[]).map((f) => (
            <button
              key={f}
              onClick={() => setFilter(f)}
              className={`tag-pill transition-all ${
                filter === f
                  ? 'bg-text-primary/10 text-text-primary'
                  : 'tag-default hover:text-text-primary'
              }`}
            >
              {f}
            </button>
          ))}
        </div>
        <div className="flex items-center gap-2 ml-auto">
          <span className="text-[11px] font-mono text-text-muted">Sort:</span>
          {(['performance', 'value', 'cost', 'context'] as SortBy[]).map((s) => (
            <button
              key={s}
              onClick={() => setSortBy(s)}
              className={`text-[11px] font-mono px-2 py-0.5 rounded transition-all ${
                sortBy === s
                  ? 'text-accent-cyan bg-accent-cyan/10'
                  : 'text-text-muted hover:text-text-primary'
              }`}
            >
              {s}
            </button>
          ))}
        </div>
      </div>

      {/* Model Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
        {sorted.map((model, i) => (
          <div
            key={model.id}
            className="animate-slide-up"
            style={{ animationDelay: `${i * 50}ms`, animationFillMode: 'backwards' }}
          >
            <ModelCard model={model} />
          </div>
        ))}
      </div>

      {/* Comparison Table */}
      <div className="mt-10 rounded-lg border border-border bg-surface-1 overflow-x-auto">
        <table className="w-full text-[12px] font-mono">
          <thead>
            <tr className="border-b border-border">
              <th className="text-left p-3 text-text-muted font-medium">Model</th>
              <th className="text-right p-3 text-text-muted font-medium">Provider</th>
              <th className="text-right p-3 text-text-muted font-medium">In $/1M</th>
              <th className="text-right p-3 text-text-muted font-medium">Out $/1M</th>
              <th className="text-right p-3 text-text-muted font-medium">Ctx</th>
              <th className="text-right p-3 text-text-muted font-medium">MMLU</th>
              <th className="text-right p-3 text-text-muted font-medium">HEval</th>
              <th className="text-right p-3 text-text-muted font-medium">MATH</th>
              <th className="text-right p-3 text-text-muted font-medium">GPQA</th>
              <th className="text-right p-3 text-text-muted font-medium">Value</th>
            </tr>
          </thead>
          <tbody>
            {sorted.map(renderTableRow)}
          </tbody>
        </table>
      </div>
    </div>
  )
}
