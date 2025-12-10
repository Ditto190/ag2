import { Card } from './Card';
import { Alert } from './Alert';
import { DataTable } from './DataTable';

interface DynamicComponentProps {
  type: string;
  [key: string]: any;
}

const componentMap: Record<string, React.ComponentType<any>> = {
  card: Card,
  alert: Alert,
  table: DataTable,
  // Add more components as needed
};

export function DynamicComponent({ type, ...props }: DynamicComponentProps) {
  const Component = componentMap[type];

  if (!Component) {
    return (
      <div className="p-4 bg-yellow-100 dark:bg-yellow-900 border border-yellow-300 dark:border-yellow-700 rounded-lg">
        <p className="text-sm text-yellow-800 dark:text-yellow-200">
          Unknown component type: {type}
        </p>
        <pre className="mt-2 text-xs overflow-auto">
          {JSON.stringify(props, null, 2)}
        </pre>
      </div>
    );
  }

  return <Component {...props} />;
}
