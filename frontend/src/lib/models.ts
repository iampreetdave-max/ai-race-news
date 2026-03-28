export interface ModelBenchmarks {
  mmlu: number
  humaneval: number
  math: number
  gpqa: number
  arc_challenge: number
  mt_bench: number
}

export interface AIModel {
  id: string
  name: string
  provider: string
  released: string
  context_window: number
  open_source: boolean
  pricing: { input: number; output: number }
  benchmarks: ModelBenchmarks
  strengths: string[]
  category: string
}

export interface BenchmarkMeta {
  name: string
  full_name: string
  description: string
  max_score: number
}

export interface ModelsData {
  models: AIModel[]
  benchmarks: Record<string, BenchmarkMeta>
  last_updated: string
}

export const PROVIDER_COLORS: Record<string, string> = {
  OpenAI: '#10b981',
  Anthropic: '#f59e0b',
  Google: '#3b82f6',
  Meta: '#6366f1',
  DeepSeek: '#ef4444',
  xAI: '#a855f7',
  Mistral: '#f97316',
  Alibaba: '#14b8a6',
}

export const BENCHMARK_KEYS: (keyof ModelBenchmarks)[] = [
  'mmlu', 'humaneval', 'math', 'gpqa', 'arc_challenge', 'mt_bench'
]

export function getValueScore(model: AIModel): number {
  const avgBenchmark =
    (model.benchmarks.mmlu +
      model.benchmarks.humaneval +
      model.benchmarks.math +
      model.benchmarks.gpqa) / 4
  const avgCost = (model.pricing.input + model.pricing.output) / 2
  if (avgCost === 0) return 0
  return Math.round((avgBenchmark / avgCost) * 10) / 10
}
