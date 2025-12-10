'use client';

import { useState } from 'react';
import { GenerativeUIChat } from '@/components/GenerativeUIChat';
import { Send } from 'lucide-react';

export default function Home() {
  const [query, setQuery] = useState('');

  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800">
      <div className="container mx-auto px-4 py-8">
        <div className="max-w-4xl mx-auto">
          {/* Header */}
          <div className="text-center mb-8">
            <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-2">
              AG2 Generative UI
            </h1>
            <p className="text-gray-600 dark:text-gray-400">
              AI-powered interfaces that adapt to your needs
            </p>
          </div>

          {/* Main Chat Interface */}
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-xl p-6">
            <GenerativeUIChat />
          </div>

          {/* Footer */}
          <div className="mt-8 text-center text-sm text-gray-500">
            <p>
              Powered by{' '}
              <a
                href="https://docs.ag2.ai"
                target="_blank"
                rel="noopener noreferrer"
                className="text-blue-600 hover:underline"
              >
                AG2
              </a>
            </p>
          </div>
        </div>
      </div>
    </main>
  );
}
