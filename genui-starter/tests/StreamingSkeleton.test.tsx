import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import { StreamingSkeleton } from '@/components/ai/StreamingSkeleton'

describe('StreamingSkeleton', () => {
  it('renders card skeleton by default', () => {
    render(<StreamingSkeleton />)
    expect(screen.getByTestId('streaming-skeleton')).toBeInTheDocument()
    expect(screen.getByTestId('skeleton-card')).toBeInTheDocument()
  })

  it('renders table skeleton variant', () => {
    render(<StreamingSkeleton variant="table" />)
    expect(screen.getByTestId('skeleton-table')).toBeInTheDocument()
  })

  it('renders chart skeleton variant', () => {
    render(<StreamingSkeleton variant="chart" />)
    expect(screen.getByTestId('skeleton-chart')).toBeInTheDocument()
  })

  it('renders text skeleton variant', () => {
    render(<StreamingSkeleton variant="text" />)
    expect(screen.getByTestId('skeleton-text')).toBeInTheDocument()
  })

  it('renders multiple skeletons when count is specified', () => {
    render(<StreamingSkeleton variant="card" count={3} />)
    const skeletons = screen.getAllByTestId('skeleton-card')
    expect(skeletons).toHaveLength(3)
  })

  it('applies animation class', () => {
    const { container } = render(<StreamingSkeleton variant="card" />)
    const animatedElement = container.querySelector('.animate-pulse')
    expect(animatedElement).toBeInTheDocument()
  })
})
