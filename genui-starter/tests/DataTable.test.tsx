import { describe, it, expect } from 'vitest'
import { render, screen, fireEvent } from '@testing-library/react'
import { DataTable } from '@/components/registry/DataTable'
import type { DataTableData } from '@/lib/schema/dashboard'

const mockTableData: DataTableData = {
  title: 'Sales Report',
  description: 'Monthly sales data',
  columns: [
    { key: 'name', header: 'Product', sortable: true, type: 'string' },
    { key: 'sales', header: 'Sales', sortable: true, type: 'number' },
    { key: 'date', header: 'Date', sortable: true, type: 'date' },
  ],
  rows: [
    { name: 'Product A', sales: 100, date: '2024-01-01' },
    { name: 'Product B', sales: 200, date: '2024-01-02' },
    { name: 'Product C', sales: 150, date: '2024-01-03' },
  ],
  filterable: true,
  sortable: true,
}

describe('DataTable', () => {
  it('renders table with title and description', () => {
    render(<DataTable data={mockTableData} />)
    expect(screen.getByText('Sales Report')).toBeInTheDocument()
    expect(screen.getByText('Monthly sales data')).toBeInTheDocument()
  })

  it('renders all columns', () => {
    render(<DataTable data={mockTableData} />)
    expect(screen.getByText('Product')).toBeInTheDocument()
    expect(screen.getByText('Sales')).toBeInTheDocument()
    expect(screen.getByText('Date')).toBeInTheDocument()
  })

  it('renders all rows', () => {
    render(<DataTable data={mockTableData} />)
    expect(screen.getByText('Product A')).toBeInTheDocument()
    expect(screen.getByText('Product B')).toBeInTheDocument()
    expect(screen.getByText('Product C')).toBeInTheDocument()
  })

  it('displays filter input when filterable is true', () => {
    render(<DataTable data={mockTableData} />)
    expect(screen.getByTestId('filter-input')).toBeInTheDocument()
  })

  it('filters rows based on input', () => {
    render(<DataTable data={mockTableData} />)
    const filterInput = screen.getByTestId('filter-input')
    
    fireEvent.change(filterInput, { target: { value: 'Product A' } })
    
    expect(screen.getByText('Product A')).toBeInTheDocument()
    expect(screen.queryByText('Product B')).not.toBeInTheDocument()
    expect(screen.queryByText('Product C')).not.toBeInTheDocument()
  })

  it('sorts rows when column header is clicked', () => {
    render(<DataTable data={mockTableData} />)
    const salesHeader = screen.getByTestId('column-header-sales')
    
    // Click to sort ascending
    fireEvent.click(salesHeader)
    
    const rows = screen.getAllByTestId('table-row')
    const firstRowCells = rows[0].querySelectorAll('[data-testid^="cell-"]')
    expect(firstRowCells[0]).toHaveTextContent('Product A')
  })

  it('shows row count', () => {
    render(<DataTable data={mockTableData} />)
    expect(screen.getByText('Showing 3 of 3 rows')).toBeInTheDocument()
  })

  it('displays "No data found" when no rows match filter', () => {
    render(<DataTable data={mockTableData} />)
    const filterInput = screen.getByTestId('filter-input')
    
    fireEvent.change(filterInput, { target: { value: 'nonexistent' } })
    
    expect(screen.getByText('No data found')).toBeInTheDocument()
  })

  it('handles empty rows gracefully', () => {
    const emptyData: DataTableData = {
      ...mockTableData,
      rows: [],
    }
    
    render(<DataTable data={emptyData} />)
    expect(screen.getByText('No data found')).toBeInTheDocument()
  })

  it('does not render filter input when filterable is false', () => {
    const nonFilterableData: DataTableData = {
      ...mockTableData,
      filterable: false,
    }
    
    render(<DataTable data={nonFilterableData} />)
    expect(screen.queryByTestId('filter-input')).not.toBeInTheDocument()
  })
})
