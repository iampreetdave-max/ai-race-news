export default function AIRacePage() {
  return (
    <section className="mx-auto max-w-7xl px-4 sm:px-6 py-16 sm:py-24">
      <div className="text-center max-w-lg mx-auto">
        {/* Icon */}
        <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-surface-2 border border-border mb-6">
          <svg
            className="w-8 h-8 text-accent-cyan"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            strokeWidth={1.5}
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M3 13.125C3 12.504 3.504 12 4.125 12h2.25c.621 0 1.125.504 1.125 1.125v6.75C7.5 20.496 6.996 21 6.375 21h-2.25A1.125 1.125 0 013 19.875v-6.75zM9.75 8.625c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125v11.25c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 01-1.125-1.125V8.625zM16.5 4.125c0-.621.504-1.125 1.125-1.125h2.25C20.496 3 21 3.504 21 4.125v15.75c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 01-1.125-1.125V4.125z"
            />
          </svg>
        </div>

        <h1 className="font-display text-2xl sm:text-3xl font-bold tracking-tight mb-3">
          AI Race
        </h1>

        <p className="text-sm text-text-secondary leading-relaxed mb-6">
          Side-by-side comparison of AI models across cost, performance,
          benchmarks, and real-world value. Track who&apos;s winning.
        </p>

        <div className="inline-flex items-center gap-2 px-4 py-2 rounded-lg border border-border bg-surface-1">
          <span className="relative flex h-2 w-2">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-accent-amber opacity-75" />
            <span className="relative inline-flex rounded-full h-2 w-2 bg-accent-amber" />
          </span>
          <span className="text-sm font-mono text-text-muted">
            Coming soon
          </span>
        </div>

        {/* Preview grid */}
        <div className="mt-12 grid grid-cols-3 gap-3">
          {[
            { label: 'Performance', value: 'MMLU, HumanEval, MATH' },
            { label: 'Cost', value: '$/1M tokens comparison' },
            { label: 'Best Value', value: 'Performance per dollar' },
          ].map((item) => (
            <div
              key={item.label}
              className="rounded-lg border border-border border-dashed bg-surface-1/50 p-4 text-left"
            >
              <p className="font-mono text-[11px] text-accent-cyan uppercase tracking-wider mb-1">
                {item.label}
              </p>
              <p className="text-[12px] text-text-muted">{item.value}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
