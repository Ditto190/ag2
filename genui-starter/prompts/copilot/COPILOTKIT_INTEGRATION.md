# CopilotKit Integration Guide

## Overview

This document describes the CopilotKit integration for the GenUI Starter application, including tool registration, usage patterns, and testing considerations.

## Architecture

### Tool Registration Hooks

The application provides two main hooks for registering GenUI tools with CopilotKit:

1. **`useGenUIRegistryTools`** - Registers individual component tools (StatCard, DataTable, ChartCard)
2. **`useDashboardTools`** - Registers the high-level dashboard composition tool

### Component Registry

The following components are exposed as CopilotKit tools:

#### StatCard (`render_stat_card`)
Renders metric/stat summary cards with:
- Title and optional description
- Metric value with optional unit
- Change indicator (percentage with label)
- Visual variant (default, success, warning, danger)

#### DataTable (`render_data_table`)
Renders sortable and filterable data tables with:
- Configurable columns (with type hints for sorting)
- Row data
- Optional filtering and sorting capabilities

#### ChartCard (`render_chart_card`)
Renders charts using Recharts with:
- Multiple chart types (line, bar, area, pie)
- Configurable data and series
- X-axis key specification
- Custom colors per series

#### Dashboard (`render_dashboard`)
Composes multiple components into a dashboard with:
- Title and description
- Array of dashboard items (stats, tables, charts)
- Layout configuration (grid or stack)

## Usage

### In React Components

```tsx
import { useGenUIRegistryTools } from '@/lib/copilotkit/hooks'

function MyCanvas() {
  const [components, setComponents] = useState([])

  useGenUIRegistryTools({
    onRenderStat: (data) => {
      setComponents(prev => [...prev, { type: 'stat', data }])
    },
    onRenderTable: (data) => {
      setComponents(prev => [...prev, { type: 'table', data }])
    },
    onRenderChart: (data) => {
      setComponents(prev => [...prev, { type: 'chart', data }])
    },
  })

  return (
    <div>
      {components.map((comp, idx) => {
        switch (comp.type) {
          case 'stat': return <StatCard key={idx} data={comp.data} />
          case 'table': return <DataTable key={idx} data={comp.data} />
          case 'chart': return <ChartCard key={idx} data={comp.data} />
        }
      })}
    </div>
  )
}
```

### With CopilotKit Provider

The hooks must be used within a CopilotKit provider context:

```tsx
import { CopilotKit } from '@copilotkit/react-core'
import { CopilotSidebar } from '@copilotkit/react-ui'

function App() {
  return (
    <CopilotKit runtimeUrl="/api/chat">
      <CopilotSidebar>
        <MyCanvas />
      </CopilotSidebar>
    </CopilotKit>
  )
}
```

## Storybook Integration

For Storybook or other non-CopilotKit contexts, you have two options:

### Option 1: Mock Provider

Create a mock CopilotKit provider for Storybook:

```tsx
// .storybook/decorators/CopilotKitDecorator.tsx
import { vi } from 'vitest'

vi.mock('@copilotkit/react-core', () => ({
  useCopilotAction: () => {},
  CopilotKit: ({ children }) => <>{children}</>,
}))
```

### Option 2: Conditional Hook Usage

Only call the hooks when in a CopilotKit context:

```tsx
function MyComponent({ enableCopilotKit = true }) {
  if (enableCopilotKit && typeof window !== 'undefined') {
    useGenUIRegistryTools({ /* ... */ })
  }
  
  return <div>...</div>
}
```

## Testing

The hooks are tested with mocked CopilotKit functions. See `tests/copilotkit-hooks.test.tsx` for examples.

### Test Strategy

1. **Import Validation** - Ensure hooks can be imported without errors
2. **Callback Acceptance** - Verify hooks accept and store callbacks
3. **Tool Registration** - Confirm tools are registered with correct names
4. **Schema Validation** - Test that Zod schemas validate data correctly

### Running Tests

```bash
npm test                    # Run all tests
npm test -- --watch        # Watch mode
npm run test:coverage      # Generate coverage report
```

## Schema Validation

All tools use Zod schemas for runtime validation. This ensures:

1. **Type Safety** - TypeScript types derived from schemas
2. **Runtime Validation** - Invalid data rejected before rendering
3. **LLM Guidance** - Clear parameter documentation for the AI

Example schema:

```typescript
const StatCardSchema = z.object({
  title: z.string(),
  description: z.string().optional(),
  metric: MetricSchema,
  variant: z.enum(['default', 'success', 'warning', 'danger']).default('default'),
})
```

## Error Handling

### Tool Handler Errors

Each tool handler includes try-catch for validation:

```typescript
handler: async (params) => {
  try {
    const data = Schema.parse(params)
    callback?.(data)
    return { success: true, data }
  } catch (error) {
    console.error('Validation error:', error)
    throw new Error('Invalid data provided')
  }
}
```

### Component Rendering Errors

All components are wrapped in ErrorBoundary:

```tsx
<ErrorBoundary>
  <GeneratedComponents />
</ErrorBoundary>
```

## Best Practices

1. **Always Use Schemas** - Validate all AI-generated data with Zod
2. **Provide Clear Descriptions** - Help the LLM understand tool parameters
3. **Set Safe Defaults** - Use sensible defaults for optional parameters
4. **Handle Missing Data** - Gracefully handle incomplete data
5. **Test Extensively** - Cover edge cases and validation errors

## Future Enhancements

Potential improvements to consider:

1. **Streaming Support** - Show loading states while LLM generates data
2. **Component Versioning** - Track and update component schemas
3. **Custom Validators** - Add business logic validation beyond schema
4. **Tool Composition** - Allow tools to call other tools
5. **Undo/Redo** - Track component history for user corrections

## References

- [CopilotKit Documentation](https://docs.copilotkit.ai)
- [Zod Documentation](https://zod.dev)
- [Recharts Documentation](https://recharts.org)
- [Next.js Documentation](https://nextjs.org/docs)
