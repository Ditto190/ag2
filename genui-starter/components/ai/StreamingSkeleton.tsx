import React from 'react'

export type StreamingSkeletonVariant = 'card' | 'table' | 'chart' | 'text'

interface StreamingSkeletonProps {
  variant?: StreamingSkeletonVariant
  count?: number
}

export function StreamingSkeleton({ variant = 'card', count = 1 }: StreamingSkeletonProps) {
  const renderSkeleton = () => {
    switch (variant) {
      case 'card':
        return (
          <div className="animate-pulse rounded-lg border border-gray-200 bg-white p-6 shadow-sm" data-testid="skeleton-card">
            <div className="space-y-3">
              <div className="h-4 w-1/3 rounded bg-gray-200"></div>
              <div className="h-8 w-1/2 rounded bg-gray-300"></div>
              <div className="h-3 w-1/4 rounded bg-gray-200"></div>
            </div>
          </div>
        )

      case 'table':
        return (
          <div className="animate-pulse space-y-4" data-testid="skeleton-table">
            <div className="h-6 w-1/4 rounded bg-gray-200"></div>
            <div className="space-y-2">
              <div className="h-10 w-full rounded bg-gray-200"></div>
              {Array.from({ length: 5 }).map((_, i) => (
                <div key={i} className="h-12 w-full rounded bg-gray-100"></div>
              ))}
            </div>
          </div>
        )

      case 'chart':
        return (
          <div className="animate-pulse rounded-lg border border-gray-200 bg-white p-6 shadow-sm" data-testid="skeleton-chart">
            <div className="space-y-4">
              <div className="h-6 w-1/3 rounded bg-gray-200"></div>
              <div className="h-64 w-full rounded bg-gray-100"></div>
            </div>
          </div>
        )

      case 'text':
        return (
          <div className="animate-pulse space-y-2" data-testid="skeleton-text">
            <div className="h-4 w-full rounded bg-gray-200"></div>
            <div className="h-4 w-5/6 rounded bg-gray-200"></div>
            <div className="h-4 w-4/6 rounded bg-gray-200"></div>
          </div>
        )

      default:
        return null
    }
  }

  return (
    <div className="space-y-4" data-testid="streaming-skeleton">
      {Array.from({ length: count }).map((_, i) => (
        <div key={i}>{renderSkeleton()}</div>
      ))}
    </div>
  )
}
