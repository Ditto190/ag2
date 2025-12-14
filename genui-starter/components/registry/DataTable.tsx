import React, { useState, useMemo } from 'react'
import type { DataTableData, Column } from '@/lib/schema/dashboard'

interface DataTableProps {
  data: DataTableData
}

type SortDirection = 'asc' | 'desc' | null

export function DataTable({ data }: DataTableProps) {
  const { title, description, columns, rows, filterable = true, sortable = true } = data
  const [filter, setFilter] = useState('')
  const [sortConfig, setSortConfig] = useState<{
    key: string | null
    direction: SortDirection
  }>({ key: null, direction: null })

  const filteredRows = useMemo(() => {
    if (!filterable || !filter) return rows

    return rows.filter((row) =>
      Object.values(row).some((value) =>
        String(value).toLowerCase().includes(filter.toLowerCase())
      )
    )
  }, [rows, filter, filterable])

  const sortedRows = useMemo(() => {
    if (!sortable || !sortConfig.key) return filteredRows

    const sorted = [...filteredRows].sort((a, b) => {
      const aVal = a[sortConfig.key!]
      const bVal = b[sortConfig.key!]

      if (aVal === bVal) return 0

      const column = columns.find((c) => c.key === sortConfig.key)
      const type = column?.type || 'string'

      let comparison = 0
      if (type === 'number') {
        comparison = Number(aVal) - Number(bVal)
      } else if (type === 'date') {
        comparison = new Date(aVal).getTime() - new Date(bVal).getTime()
      } else {
        comparison = String(aVal).localeCompare(String(bVal))
      }

      return sortConfig.direction === 'asc' ? comparison : -comparison
    })

    return sorted
  }, [filteredRows, sortConfig, columns, sortable])

  const handleSort = (columnKey: string) => {
    const column = columns.find((c) => c.key === columnKey)
    if (!sortable || !column?.sortable) return

    setSortConfig((prev) => {
      if (prev.key === columnKey) {
        if (prev.direction === 'asc') return { key: columnKey, direction: 'desc' }
        if (prev.direction === 'desc') return { key: null, direction: null }
      }
      return { key: columnKey, direction: 'asc' }
    })
  }

  const getSortIcon = (columnKey: string) => {
    if (sortConfig.key !== columnKey) return '⇅'
    return sortConfig.direction === 'asc' ? '↑' : '↓'
  }

  return (
    <div className="w-full space-y-4" data-testid="data-table">
      <div>
        <h3 className="text-lg font-semibold text-gray-900">{title}</h3>
        {description && <p className="text-sm text-gray-600">{description}</p>}
      </div>

      {filterable && (
        <input
          type="text"
          placeholder="Filter..."
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
          className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
          data-testid="filter-input"
        />
      )}

      <div className="overflow-x-auto rounded-lg border border-gray-200">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              {columns.map((column) => (
                <th
                  key={column.key}
                  onClick={() => handleSort(column.key)}
                  className={`px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-700 ${
                    sortable && column.sortable ? 'cursor-pointer hover:bg-gray-100' : ''
                  }`}
                  data-testid={`column-header-${column.key}`}
                >
                  <div className="flex items-center space-x-1">
                    <span>{column.header}</span>
                    {sortable && column.sortable && (
                      <span className="text-gray-400">{getSortIcon(column.key)}</span>
                    )}
                  </div>
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200 bg-white">
            {sortedRows.length === 0 ? (
              <tr>
                <td
                  colSpan={columns.length}
                  className="px-6 py-4 text-center text-sm text-gray-500"
                >
                  No data found
                </td>
              </tr>
            ) : (
              sortedRows.map((row, idx) => (
                <tr key={idx} className="hover:bg-gray-50" data-testid="table-row">
                  {columns.map((column) => (
                    <td
                      key={column.key}
                      className="whitespace-nowrap px-6 py-4 text-sm text-gray-900"
                      data-testid={`cell-${column.key}`}
                    >
                      {row[column.key] ?? '—'}
                    </td>
                  ))}
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      <div className="text-xs text-gray-500">
        Showing {sortedRows.length} of {rows.length} rows
      </div>
    </div>
  )
}
