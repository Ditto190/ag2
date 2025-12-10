import { AlertCircle, CheckCircle, Info, XCircle } from 'lucide-react';

interface AlertProps {
  title?: string;
  content?: string;
  type?: 'info' | 'success' | 'warning' | 'error';
}

const alertStyles = {
  info: {
    bg: 'bg-blue-50 dark:bg-blue-900/20',
    border: 'border-blue-200 dark:border-blue-800',
    text: 'text-blue-800 dark:text-blue-200',
    icon: Info,
  },
  success: {
    bg: 'bg-green-50 dark:bg-green-900/20',
    border: 'border-green-200 dark:border-green-800',
    text: 'text-green-800 dark:text-green-200',
    icon: CheckCircle,
  },
  warning: {
    bg: 'bg-yellow-50 dark:bg-yellow-900/20',
    border: 'border-yellow-200 dark:border-yellow-800',
    text: 'text-yellow-800 dark:text-yellow-200',
    icon: AlertCircle,
  },
  error: {
    bg: 'bg-red-50 dark:bg-red-900/20',
    border: 'border-red-200 dark:border-red-800',
    text: 'text-red-800 dark:text-red-200',
    icon: XCircle,
  },
};

export function Alert({ title, content, type = 'info' }: AlertProps) {
  const style = alertStyles[type];
  const Icon = style.icon;

  return (
    <div className={`${style.bg} ${style.border} border rounded-lg p-4`}>
      <div className="flex items-start gap-3">
        <Icon className={`h-5 w-5 ${style.text} mt-0.5`} />
        <div className="flex-1">
          {title && (
            <h4 className={`font-semibold ${style.text} mb-1`}>{title}</h4>
          )}
          {content && <p className={`text-sm ${style.text}`}>{content}</p>}
        </div>
      </div>
    </div>
  );
}
