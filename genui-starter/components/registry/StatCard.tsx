import React from 'react'
import type { StatCardData } from '@/lib/schema/dashboard'

interface StatCardProps {
  data: StatCardData
}

export function StatCard({ data }: StatCardProps) {
  const { title, description, metric, variant = 'default' } = data

  const variantStyles = {
    default: 'bg-white border-gray-200',
    success: 'bg-green-50 border-green-200',
    warning: 'bg-yellow-50 border-yellow-200',
    danger: 'bg-red-50 border-red-200',
  }

  const changeColor = metric.change
    ? metric.change > 0
      ? 'text-green-600'
      : metric.change < 0
      ? 'text-red-600'
      : 'text-gray-600'
    : 'text-gray-600'

  return (
    <div
      className={`rounded-lg border p-6 shadow-sm ${variantStyles[variant]}`}
      data-testid="stat-card"
    >
      <div className="space-y-2">
        <h3 className="text-sm font-medium text-gray-600">{title}</h3>
        {description && (
          <p className="text-xs text-gray-500">{description}</p>
        )}
        <div className="flex items-baseline space-x-2">
          <p className="text-3xl font-bold text-gray-900" data-testid="metric-value">
            {metric.value}
            {metric.unit && (
              <span className="ml-1 text-xl text-gray-600">{metric.unit}</span>
            )}
          </p>
        </div>
        {metric.change !== undefined && (
          <div className="flex items-center space-x-1">
            <span className={`text-sm font-medium ${changeColor}`} data-testid="metric-change">
              {metric.change > 0 ? '+' : ''}
              {metric.change}%
            </span>
            {metric.changeLabel && (
              <span className="text-xs text-gray-500">{metric.changeLabel}</span>
            )}
          </div>
        )}
      </div>
    </div>
  )
}
