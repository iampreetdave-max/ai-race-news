import { AIModel, PROVIDER_COLORS, getValueScore, BENCHMARK_KEYS } from '@/lib/models'

function formatContext(ctx: number): string {
  if (ctx >= 1000000) return `${(ctx / 1000000).toFixed(0)}M`
  return `${(ctx / 1000).toFixed(0)}K`
}

export default function ModelCard({ model }: { model: AIModel }) {
  const valueScore = getValueScore(model)
  const providerColor = PROVIDER_COLORS[model.provider] || '#71717a'
  const maxBenchmark = Math.max(...BENCHMARK_KEYS.map((k) => (model.benchmarks as any)[k]))

  return (
    <div className="rounded-lg border border-border bg-surface-1 hover:bg-surface-2 hover:border-border-hover transition-all p-4 sm:p-5">
      {/* Header */}
      <div className="flex items-start justify-between mb-3">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span
              className="w-2 h-2 rounded-full"
              style={{ backgroundColor: providerColor }}
            />
            <span className="text-[11px] font-mono text-text-muted">
              {model.provider}
            </span>
            {model.open_source && (
              <span className="tag-pill tag-open-source">OSS</span>
            )}
          </div>
          <h3 className="font-display text-base font-bold text-text-primary">
            {model.name}
          </h3>
        </div>
        <div className="text-right">
          <p className="text-[11px] font-mono text-text-muted">value</p>
          <p className="font-display text-lg font-bold" style={{ color: providerColor }}>
            {valueScore}
          </p>
        </div>
      </div>

      {/* Quick stats */}
      <div className="grid grid-cols-3 gap-2 mb-4">
        <div className="bg-surface-0 rounded px-2.5 py-1.5">
          <p className="text-[10px] font-mono text-text-muted uppercase">Context</p>
          <p className="text-sm font-display font-semibold text-text-primary">
            {formatContext(model.context_window)}
          </p>
        </div>
        <div className="bg-surface-0 rounded px-2.5 py-1.5">
          <p className="text-[10px] font-mono text-text-muted uppercase">Input</p>
          <p className="text-sm font-display font-semibold text-text-primary">
            ${model.pricing.input}
          </p>
        </div>
        <div className="bg-surface-0 rounded px-2.5 py-1.5">
          <p className="text-[10px] font-mono text-text-muted uppercase">Output</p>
          <p className="text-sm font-display font-semibold text-text-primary">
            ${model.pricing.output}
          </p>
        </div>
      </div>

      {/* Benchmark bars */}
      <div className="space-y-1.5 mb-4">
        {BENCHMARK_KEYS.map((key) => {
          const val = (model.benchmarks as any)[key]
          const max = key === 'mt_bench' ? 10 : 100
          const pct = (val / max) * 100
          return (
            <div key={key} className="flex items-center gap-2">
              <span className="text-[10px] font-mono text-text-muted w-14 text-right uppercase">
                {key === 'arc_challenge' ? 'ARC-C' : key === 'mt_bench' ? 'MT-B' : key}
              </span>
              <div className="flex-1 h-1.5 bg-surface-0 rounded-full overflow-hidden">
                <div
                  className="h-full rounded-full transition-all"
                  style={{ width: `${pct}%`, backgroundColor: providerColor, opacity: 0.7 }}
                />
              </div>
              <span className="text-[10px] font-mono text-text-muted w-8">
                {val}
              </span>
            </div>
          )
        })}
      </div>

      {/* Strengths */}
      <div className="flex flex-wrap gap-1">
        {model.strengths.map((s) => (
          <span key={s} className="tag-pill tag-default text-[10px]">
            {s}
          </span>
        ))}
      </div>
    </div>
  )
}
