# GenUI Starter

A Next.js starter application for building Generative UI experiences with CopilotKit.

## Features

- 🎨 **Component Registry**: Pre-built UI components for data visualization
  - StatCard: Metric/stat summary cards
  - DataTable: Sortable and filterable tables
  - ChartCard: Charts powered by Recharts (line, bar, area, pie)
  
- 🤖 **CopilotKit Integration**: AI-powered component generation
  - LLM-friendly tool definitions with Zod schema validation
  - Declarative API for registering UI tools
  - Dashboard composition support

- 🧪 **Testing Setup**: Comprehensive test coverage
  - Vitest + React Testing Library
  - Unit tests for all components
  - Mock-friendly CopilotKit integration

- 🔒 **Sandboxed Execution**: Safe HTML rendering with iframe sandboxing
  
- 🎯 **Type Safety**: Full TypeScript support with Zod runtime validation

## Getting Started

### Prerequisites

- Node.js 20+
- npm or pnpm

### Installation

```bash
cd genui-starter
npm install
```

### Development

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) to see the application.

### Testing

```bash
# Run tests
npm test

# Run tests in watch mode
npm test -- --watch

# Generate coverage report
npm run test:coverage
```

### Building

```bash
npm run build
npm start
```

## Project Structure

```
genui-starter/
├── app/
│   ├── api/
│   │   └── chat/
│   │       └── route.ts          # CopilotKit chat API endpoint
│   ├── canvas/
│   │   ├── GenerativeCanvas.tsx  # Main GenUI canvas component
│   │   └── page.tsx              # Canvas page with CopilotKit provider
│   ├── layout.tsx                # Root layout
│   ├── page.tsx                  # Home page (redirects to canvas)
│   └── globals.css               # Global styles
├── components/
│   ├── ai/
│   │   └── StreamingSkeleton.tsx # Loading skeletons for streaming UI
│   ├── common/
│   │   └── ErrorBoundary.tsx     # Error boundary component
│   ├── registry/
│   │   ├── StatCard.tsx          # Metric/stat card component
│   │   ├── DataTable.tsx         # Data table with sort/filter
│   │   └── ChartCard.tsx         # Chart component (Recharts)
│   ├── renderers/
│   │   └── DashboardRenderer.tsx # Dashboard layout renderer
│   └── sandbox/
│       └── SandboxedHTML.tsx     # Sandboxed HTML renderer
├── lib/
│   ├── copilotkit/
│   │   └── hooks.ts              # CopilotKit tool registration hooks
│   └── schema/
│       └── dashboard.ts          # Zod schemas for components
├── tests/
│   ├── setupTests.ts             # Test configuration
│   ├── StreamingSkeleton.test.tsx
│   ├── DataTable.test.tsx
│   ├── ChartCard.test.tsx
│   ├── SandboxedHTML.test.tsx
│   ├── ErrorBoundary.test.tsx
│   └── copilotkit-hooks.test.tsx
├── package.json
├── tsconfig.json
├── vitest.config.ts
└── tailwind.config.js
```

## Usage

### Registering GenUI Tools

In your React component (within a CopilotKit provider):

```tsx
import { useGenUIRegistryTools } from '@/lib/copilotkit/hooks'

function MyCanvas() {
  useGenUIRegistryTools({
    onRenderStat: (data) => {
      // Handle stat card rendering
    },
    onRenderTable: (data) => {
      // Handle table rendering
    },
    onRenderChart: (data) => {
      // Handle chart rendering
    },
  })

  return <div>Your UI</div>
}
```

### Available CopilotKit Tools

- `render_stat_card`: Create metric/stat summary cards
- `render_data_table`: Create sortable/filterable data tables
- `render_chart_card`: Create charts (line, bar, area, pie)
- `render_dashboard`: Create complete dashboards with multiple components

### Component Examples

#### StatCard

```tsx
<StatCard
  data={{
    title: 'Total Revenue',
    metric: {
      label: 'Revenue',
      value: '1,234',
      unit: 'USD',
      change: 12.5,
      changeLabel: 'vs last month',
    },
    variant: 'success',
  }}
/>
```

#### DataTable

```tsx
<DataTable
  data={{
    title: 'Sales Report',
    columns: [
      { key: 'product', header: 'Product', sortable: true },
      { key: 'sales', header: 'Sales', sortable: true, type: 'number' },
    ],
    rows: [
      { product: 'A', sales: 100 },
      { product: 'B', sales: 200 },
    ],
  }}
/>
```

#### ChartCard

```tsx
<ChartCard
  data={{
    title: 'Sales Trends',
    chartType: 'line',
    data: [
      { month: 'Jan', sales: 100 },
      { month: 'Feb', sales: 150 },
    ],
    xKey: 'month',
    series: [{ key: 'sales', name: 'Sales' }],
  }}
/>
```

## Architecture

This starter follows the Generative UI architecture with:

1. **Schema-First Design**: All components use Zod schemas for validation
2. **Tool-Based Generation**: CopilotKit tools map to UI components
3. **Type Safety**: Full TypeScript support with runtime validation
4. **Composability**: Components can be combined into dashboards
5. **Error Boundaries**: Graceful error handling for AI-generated UI

## Testing Strategy

- **Component Tests**: Verify rendering, interactions, and edge cases
- **Hook Tests**: Ensure CopilotKit integration works correctly
- **Schema Validation**: Test Zod schemas validate/reject data correctly
- **Accessibility**: Components follow accessibility best practices

## License

MIT
