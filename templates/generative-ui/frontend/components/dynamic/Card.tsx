interface CardProps {
  title?: string;
  content?: string;
  data?: any;
  actions?: Array<{ label: string; action: string }>;
}

export function Card({ title, content, data, actions }: CardProps) {
  return (
    <div className="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg shadow-sm overflow-hidden">
      {title && (
        <div className="px-4 py-3 border-b border-gray-200 dark:border-gray-700">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
            {title}
          </h3>
        </div>
      )}
      
      <div className="px-4 py-3">
        {content && (
          <p className="text-gray-700 dark:text-gray-300 mb-3">{content}</p>
        )}
        
        {data && (
          <div className="space-y-2">
            {Object.entries(data).map(([key, value]) => (
              <div key={key} className="flex justify-between items-center">
                <span className="text-sm font-medium text-gray-600 dark:text-gray-400">
                  {key}:
                </span>
                <span className="text-sm text-gray-900 dark:text-white">
                  {String(value)}
                </span>
              </div>
            ))}
          </div>
        )}
      </div>
      
      {actions && actions.length > 0 && (
        <div className="px-4 py-3 bg-gray-50 dark:bg-gray-900 border-t border-gray-200 dark:border-gray-700 flex gap-2">
          {actions.map((action, idx) => (
            <button
              key={idx}
              className="px-4 py-2 text-sm bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors"
              onClick={() => {
                // TODO: Implement proper action handling
                // This is a placeholder - in production, dispatch actions to your backend
                console.log('Action triggered:', action.action);
                alert(`Action: ${action.label}\nThis is a placeholder. Implement your action handler.`);
              }}
            >
              {action.label}
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
