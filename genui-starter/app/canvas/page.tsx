'use client'

import { CopilotKit } from '@copilotkit/react-core'
import GenerativeCanvas from './GenerativeCanvas'

export default function CanvasPage() {
  return (
    <CopilotKit runtimeUrl="/api/chat">
      <GenerativeCanvas />
    </CopilotKit>
  )
}
