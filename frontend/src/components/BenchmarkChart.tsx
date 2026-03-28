'use client'

import {
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell,
} from 'recharts'
import { AIModel, PROVIDER_COLORS } from '@/lib/models'

interface Props {
  models: AIModel[]
  benchmarkKey: string
  title: string
  maxScore?: number
}

export default function BenchmarkChart({ models, benchmarkKey, title, maxScore = 100 }: Props) {
  const data = models
    .map((m) => ({
      name: m.name.length > 16 ? m.name.slice(0, 14) + '..' : m.name,
      fullName: m.name,
      value: (m.benchmarks as any)[benchmarkKey] ?? 0,
      provider: m.provider,
    }))
    .sort((a, b) => b.value - a.value)
    .slice(0, 12)

  return (
    <div className="rounded-lg border border-border bg-surface-1 p-4 sm:p-5">
      <h3 className="font-display text-sm font-semibold mb-4 text-text-primary">
        {title}
      </h3>
      <div className="h-[300px] sm:h-[360px]">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={data} layout="vertical" margin={{ left: 10, right: 20, top: 0, bottom: 0 }}>
            <XAxis
              type="number"
              domain={[0, maxScore]}
              tick={{ fill: '#71717a', fontSize: 11, fontFamily: 'JetBrains Mono' }}
              axisLine={{ stroke: '#27272a' }}
              tickLine={false}
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
              itemStyle={{ color: '#a1a1aa' }}
              formatter={(value: number) => [value.toFixed(1), title]}
              labelFormatter={(label) => {
                const item = data.find((d) => d.name === label)
                return item?.fullName || label
              }}
            />
            <Bar dataKey="value" radius={[0, 4, 4, 0]} barSize={20}>
              {data.map((entry) => (
                <Cell
                  key={entry.name}
                  fill={PROVIDER_COLORS[entry.provider] || '#71717a'}
                  fillOpacity={0.8}
                />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}
