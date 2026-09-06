'use client'

import React, { useState } from 'react'
import { CopilotKit } from '@copilotkit/react-core'
import { CopilotSidebar } from '@copilotkit/react-ui'
import '@copilotkit/react-ui/styles.css'

import { useGenUIRegistryTools, useDashboardTools } from '@/lib/copilotkit/hooks'
import { StatCard } from '@/components/registry/StatCard'
import { DataTable } from '@/components/registry/DataTable'
import { ChartCard } from '@/components/registry/ChartCard'
import { DashboardRenderer } from '@/components/renderers/DashboardRenderer'
import { ErrorBoundary } from '@/components/common/ErrorBoundary'
import { StreamingSkeleton } from '@/components/ai/StreamingSkeleton'

import type {
  StatCardData,
  DataTableData,
  ChartCardData,
  Dashboard,
} from '@/lib/schema/dashboard'

type RenderedComponent =
  | { type: 'stat'; data: StatCardData; id: string }
  | { type: 'table'; data: DataTableData; id: string }
  | { type: 'chart'; data: ChartCardData; id: string }
  | { type: 'dashboard'; data: Dashboard; id: string }

export default function GenerativeCanvas() {
  const [components, setComponents] = useState<RenderedComponent[]>([])
  const [isStreaming, setIsStreaming] = useState(false)

  // Register GenUI tools
  useGenUIRegistryTools({
    onRenderStat: (data) => {
      setComponents((prev) => [
        ...prev,
        { type: 'stat', data, id: `stat-${Date.now()}` },
      ])
      setIsStreaming(false)
    },
    onRenderTable: (data) => {
      setComponents((prev) => [
        ...prev,
        { type: 'table', data, id: `table-${Date.now()}` },
      ])
      setIsStreaming(false)
    },
    onRenderChart: (data) => {
      setComponents((prev) => [
        ...prev,
        { type: 'chart', data, id: `chart-${Date.now()}` },
      ])
      setIsStreaming(false)
    },
  })

  // Register dashboard tool
  useDashboardTools({
    onRenderDashboard: (data) => {
      setComponents((prev) => [
        ...prev,
        { type: 'dashboard', data, id: `dashboard-${Date.now()}` },
      ])
      setIsStreaming(false)
    },
  })

  return (
    <div className="flex h-screen w-full">
      <CopilotSidebar
        defaultOpen={true}
        instructions="You are a helpful assistant that can create beautiful data visualizations and dashboards. You can render stat cards, data tables, and charts based on user requests."
        labels={{
          title: 'GenUI Assistant',
          initial: 'Hello! I can help you create dashboards, charts, tables, and stat cards. What would you like to visualize?',
        }}
      >
        <div className="flex-1 overflow-auto bg-gray-50 p-8">
          <div className="mx-auto max-w-7xl space-y-8">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Generative Canvas</h1>
              <p className="mt-2 text-gray-600">
                Use the chat sidebar to generate UI components with AI
              </p>
            </div>

            <ErrorBoundary>
              {isStreaming && <StreamingSkeleton variant="card" />}

              {components.length === 0 && !isStreaming && (
                <div className="rounded-lg border-2 border-dashed border-gray-300 p-12 text-center">
                  <p className="text-lg text-gray-500">
                    No components yet. Ask the assistant to create something!
                  </p>
                  <p className="mt-2 text-sm text-gray-400">
                    Try: &quot;Create a stat card showing revenue&quot; or &quot;Build a sales dashboard&quot;
                  </p>
                </div>
              )}

              <div className="space-y-6">
                {components.map((component) => {
                  switch (component.type) {
                    case 'stat':
                      return (
                        <div key={component.id}>
                          <StatCard data={component.data} />
                        </div>
                      )

                    case 'table':
                      return (
                        <div key={component.id}>
                          <DataTable data={component.data} />
                        </div>
                      )

                    case 'chart':
                      return (
                        <div key={component.id}>
                          <ChartCard data={component.data} />
                        </div>
                      )

                    case 'dashboard':
                      return (
                        <div key={component.id}>
                          <DashboardRenderer dashboard={component.data} />
                        </div>
                      )

                    default:
                      return null
                  }
                })}
              </div>
            </ErrorBoundary>
          </div>
        </div>
      </CopilotSidebar>
    </div>
  )
}
