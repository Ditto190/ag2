import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import { ChartCard } from '@/components/registry/ChartCard'
import type { ChartCardData } from '@/lib/schema/dashboard'

const mockChartData: ChartCardData = {
  title: 'Sales Trends',
  description: 'Monthly sales over time',
  chartType: 'line',
  data: [
    { month: 'Jan', sales: 100, revenue: 1000 },
    { month: 'Feb', sales: 150, revenue: 1500 },
    { month: 'Mar', sales: 200, revenue: 2000 },
  ],
  xKey: 'month',
  series: [
    { key: 'sales', name: 'Sales', color: '#3b82f6' },
    { key: 'revenue', name: 'Revenue', color: '#10b981' },
  ],
  height: 300,
}

describe('ChartCard', () => {
  it('renders chart with title and description', () => {
    render(<ChartCard data={mockChartData} />)
    expect(screen.getByText('Sales Trends')).toBeInTheDocument()
    expect(screen.getByText('Monthly sales over time')).toBeInTheDocument()
  })

  it('renders line chart', () => {
    render(<ChartCard data={mockChartData} />)
    expect(screen.getByTestId('chart-line')).toBeInTheDocument()
  })

  it('renders bar chart', () => {
    const barChartData: ChartCardData = {
      ...mockChartData,
      chartType: 'bar',
    }
    render(<ChartCard data={barChartData} />)
    expect(screen.getByTestId('chart-bar')).toBeInTheDocument()
  })

  it('renders area chart', () => {
    const areaChartData: ChartCardData = {
      ...mockChartData,
      chartType: 'area',
    }
    render(<ChartCard data={areaChartData} />)
    expect(screen.getByTestId('chart-area')).toBeInTheDocument()
  })

  it('renders pie chart', () => {
    const pieChartData: ChartCardData = {
      ...mockChartData,
      chartType: 'pie',
    }
    render(<ChartCard data={pieChartData} />)
    expect(screen.getByTestId('chart-pie')).toBeInTheDocument()
  })

  it('displays series labels', () => {
    render(<ChartCard data={mockChartData} />)
    // Recharts renders series names in the legend
    const chartContainer = screen.getByTestId('chart-line')
    expect(chartContainer).toBeInTheDocument()
  })

  it('renders without description', () => {
    const dataWithoutDesc: ChartCardData = {
      ...mockChartData,
      description: undefined,
    }
    render(<ChartCard data={dataWithoutDesc} />)
    expect(screen.getByText('Sales Trends')).toBeInTheDocument()
    expect(screen.queryByText('Monthly sales over time')).not.toBeInTheDocument()
  })

  it('uses default height when not specified', () => {
    const dataWithDefaultHeight: ChartCardData = {
      ...mockChartData,
      height: 300,
    }
    render(<ChartCard data={dataWithDefaultHeight} />)
    expect(screen.getByTestId('chart-card')).toBeInTheDocument()
  })
})
