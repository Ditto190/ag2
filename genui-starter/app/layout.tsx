import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'GenUI Starter',
  description: 'Generative UI starter with CopilotKit',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
