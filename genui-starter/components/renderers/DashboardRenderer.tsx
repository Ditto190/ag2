import React from 'react'
import { StatCard } from '@/components/registry/StatCard'
import { DataTable } from '@/components/registry/DataTable'
import { ChartCard } from '@/components/registry/ChartCard'
import type { Dashboard } from '@/lib/schema/dashboard'

interface DashboardRendererProps {
  dashboard: Dashboard
}

export function DashboardRenderer({ dashboard }: DashboardRendererProps) {
  const { title, description, items, layout = 'grid' } = dashboard

  const layoutClass =
    layout === 'grid'
      ? 'grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3'
      : 'space-y-6'

  return (
    <div className="w-full space-y-6" data-testid="dashboard-renderer">
      <div>
        <h2 className="text-2xl font-bold text-gray-900">{title}</h2>
        {description && <p className="mt-1 text-sm text-gray-600">{description}</p>}
      </div>

      <div className={layoutClass}>
        {items.map((item) => {
          switch (item.type) {
            case 'stat':
              return (
                <div key={item.id}>
                  <StatCard data={item.data} />
                </div>
              )

            case 'table':
              return (
                <div key={item.id} className="col-span-full">
                  <DataTable data={item.data} />
                </div>
              )

            case 'chart':
              return (
                <div key={item.id} className="col-span-full md:col-span-2">
                  <ChartCard data={item.data} />
                </div>
              )

            default:
              return null
          }
        })}
      </div>
    </div>
  )
}
