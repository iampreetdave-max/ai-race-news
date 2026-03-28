'use client'

import {
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell,
} from 'recharts'
import { AIModel, PROVIDER_COLORS } from '@/lib/models'

export default function CostChart({ models }: { models: AIModel[] }) {
  const data = models
    .map((m) => ({
      name: m.name.length > 16 ? m.name.slice(0, 14) + '..' : m.name,
      fullName: m.name,
      input: m.pricing.input,
      output: m.pricing.output,
      provider: m.provider,
    }))
    .sort((a, b) => (a.input + a.output) - (b.input + b.output))

  return (
    <div className="rounded-lg border border-border bg-surface-1 p-4 sm:p-5">
      <h3 className="font-display text-sm font-semibold mb-1 text-text-primary">
        Cost per 1M Tokens
      </h3>
      <p className="text-[11px] text-text-muted mb-4 font-mono">USD / 1M tokens (input + output)</p>
      <div className="h-[360px]">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={data} layout="vertical" margin={{ left: 10, right: 20, top: 0, bottom: 0 }}>
            <XAxis
              type="number"
              tick={{ fill: '#71717a', fontSize: 11, fontFamily: 'JetBrains Mono' }}
              axisLine={{ stroke: '#27272a' }}
              tickLine={false}
              tickFormatter={(v) => `$${v}`}
            />
            <YAxis
              type="category"
              dataKey="name"
              width={120}
              tick={{ fill: '#a1a1aa', fontSize: 11, fontFamily: 'JetBrains Mono' }}
              axisLine={false}
              tickLine={false}
            />
            <Tooltip
              contentStyle={{
                backgroundColor: '#16161a',
                border: '1px solid #27272a',
                borderRadius: '8px',
                fontSize: 12,
                fontFamily: 'JetBrains Mono',
              }}
              labelStyle={{ color: '#e4e4e7' }}
              formatter={(value: number, name: string) => [
                `$${value.toFixed(2)}`,
                name === 'input' ? 'Input' : 'Output',
              ]}
              labelFormatter={(label) => {
                const item = data.find((d) => d.name === label)
                return item?.fullName || label
              }}
            />
            <Bar dataKey="input" stackId="cost" fill="#3b82f6" barSize={20} radius={[0, 0, 0, 0]} name="input" />
            <Bar dataKey="output" stackId="cost" fill="#ef4444" barSize={20} radius={[0, 4, 4, 0]} name="output" />
          </BarChart>
        </ResponsiveContainer>
      </div>
      <div className="flex gap-4 mt-3 justify-center text-[11px] font-mono text-text-muted">
        <span className="flex items-center gap-1.5">
          <span className="w-2.5 h-2.5 rounded-sm bg-blue-500" /> Input
        </span>
        <span className="flex items-center gap-1.5">
          <span className="w-2.5 h-2.5 rounded-sm bg-red-500" /> Output
        </span>
      </div>
    </div>
  )
}
