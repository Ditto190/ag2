interface DataTableProps {
  title?: string;
  data?: {
    headers?: string[];
    rows?: any[][];
  };
}

export function DataTable({ title, data }: DataTableProps) {
  if (!data || !data.headers || !data.rows) {
    return (
      <div className="p-4 border border-gray-200 dark:border-gray-700 rounded-lg">
        <p className="text-sm text-gray-500">No table data provided</p>
      </div>
    );
  }

  return (
    <div className="border border-gray-200 dark:border-gray-700 rounded-lg overflow-hidden">
      {title && (
        <div className="px-4 py-3 bg-gray-50 dark:bg-gray-900 border-b border-gray-200 dark:border-gray-700">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
            {title}
          </h3>
        </div>
      )}
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead className="bg-gray-50 dark:bg-gray-800">
            <tr>
              {data.headers.map((header, idx) => (
                <th
                  key={idx}
                  className="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider"
                >
                  {header}
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="bg-white dark:bg-gray-900 divide-y divide-gray-200 dark:divide-gray-700">
            {data.rows.map((row, rowIdx) => (
              <tr key={rowIdx} className="hover:bg-gray-50 dark:hover:bg-gray-800">
                {row.map((cell, cellIdx) => (
                  <td
                    key={cellIdx}
                    className="px-4 py-3 text-sm text-gray-900 dark:text-gray-100"
                  >
                    {String(cell)}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
