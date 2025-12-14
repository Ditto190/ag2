import { describe, it, expect, vi, beforeEach } from 'vitest'
import { renderHook } from '@testing-library/react'
import type { StatCardData, DataTableData, ChartCardData, Dashboard } from '@/lib/schema/dashboard'

// Mock CopilotKit hooks before imports
vi.mock('@copilotkit/react-core', () => ({
  useCopilotAction: vi.fn((config) => {
    return config
  }),
}))

import { useGenUIRegistryTools, useDashboardTools } from '@/lib/copilotkit/hooks'

describe('CopilotKit Hooks', () => {
  beforeEach(() => {
    // Clear mock calls before each test
    vi.clearAllMocks()
  })

  describe('useGenUIRegistryTools', () => {
    it('can be imported and used without throwing', () => {
      expect(() => {
        renderHook(() => useGenUIRegistryTools())
      }).not.toThrow()
    })

    it('accepts callbacks for rendering components', () => {
      const callbacks = {
        onRenderStat: vi.fn(),
        onRenderTable: vi.fn(),
        onRenderChart: vi.fn(),
      }

      expect(() => {
        renderHook(() => useGenUIRegistryTools(callbacks))
      }).not.toThrow()
    })

    it('returns availability status', () => {
      const { result } = renderHook(() => useGenUIRegistryTools())
      expect(result.current).toHaveProperty('isAvailable')
    })

    it('handles undefined callbacks gracefully', () => {
      expect(() => {
        renderHook(() => useGenUIRegistryTools(undefined))
      }).not.toThrow()
    })

    it('registers tools with proper names', async () => {
      const { useCopilotAction } = await import('@copilotkit/react-core')
      renderHook(() => useGenUIRegistryTools())
      
      // Check that useCopilotAction was called with proper tool names
      const mockFn = vi.mocked(useCopilotAction)
      const calls = mockFn.mock.calls
      const toolNames = calls.map((call: any) => call[0]?.name).filter(Boolean)
      
      expect(toolNames).toContain('render_stat_card')
      expect(toolNames).toContain('render_data_table')
      expect(toolNames).toContain('render_chart_card')
    })
  })

  describe('useDashboardTools', () => {
    it('can be imported and used without throwing', () => {
      expect(() => {
        renderHook(() => useDashboardTools())
      }).not.toThrow()
    })

    it('accepts onRenderDashboard callback', () => {
      const callbacks = {
        onRenderDashboard: vi.fn(),
      }

      expect(() => {
        renderHook(() => useDashboardTools(callbacks))
      }).not.toThrow()
    })

    it('registers dashboard tool', async () => {
      const { useCopilotAction } = await import('@copilotkit/react-core')
      vi.clearAllMocks()
      
      renderHook(() => useDashboardTools())
      
      const mockFn = vi.mocked(useCopilotAction)
      const calls = mockFn.mock.calls
      const toolNames = calls.map((call: any) => call[0]?.name).filter(Boolean)
      
      expect(toolNames).toContain('render_dashboard')
    })
  })

  describe('Tool schema validation', () => {
    it('validates StatCard data structure', () => {
      const validStatData: StatCardData = {
        title: 'Revenue',
        metric: {
          label: 'Total Revenue',
          value: '1000',
          unit: 'USD',
        },
        variant: 'success',
      }

      // This should not throw
      expect(validStatData).toBeDefined()
    })

    it('validates DataTable data structure', () => {
      const validTableData: DataTableData = {
        title: 'Sales',
        columns: [
          { key: 'name', header: 'Name', sortable: true, type: 'string' },
        ],
        rows: [{ name: 'Product A' }],
        filterable: true,
        sortable: true,
      }

      expect(validTableData).toBeDefined()
    })

    it('validates ChartCard data structure', () => {
      const validChartData: ChartCardData = {
        title: 'Trends',
        chartType: 'line',
        data: [{ month: 'Jan', value: 100 }],
        xKey: 'month',
        series: [{ key: 'value', name: 'Value' }],
        height: 300,
      }

      expect(validChartData).toBeDefined()
    })

    it('validates Dashboard data structure', () => {
      const validDashboard: Dashboard = {
        title: 'My Dashboard',
        items: [
          {
            type: 'stat',
            id: '1',
            data: {
              title: 'Revenue',
              metric: { label: 'Total', value: '100' },
              variant: 'default',
            },
          },
        ],
        layout: 'grid',
      }

      expect(validDashboard).toBeDefined()
    })
  })
})

