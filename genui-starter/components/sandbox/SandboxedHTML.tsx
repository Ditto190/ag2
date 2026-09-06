import React, { useEffect, useRef, useState } from 'react'

interface SandboxedHTMLProps {
  html: string
  css?: string
  onError?: (error: Error) => void
}

export function SandboxedHTML({ html, css = '', onError }: SandboxedHTMLProps) {
  const iframeRef = useRef<HTMLIFrameElement>(null)
  const [height, setHeight] = useState(300)

  useEffect(() => {
    const handleMessage = (event: MessageEvent) => {
      // Only accept messages from the iframe
      if (event.source !== iframeRef.current?.contentWindow) return

      if (event.data.type === 'resize') {
        setHeight(event.data.height)
      }
    }

    window.addEventListener('message', handleMessage)
    return () => window.removeEventListener('message', handleMessage)
  }, [])

  useEffect(() => {
    if (!iframeRef.current) return

    const iframe = iframeRef.current
    const iframeDoc = iframe.contentDocument || iframe.contentWindow?.document

    if (!iframeDoc) return

    try {
      const content = `
        <!DOCTYPE html>
        <html>
          <head>
            <meta charset="utf-8">
            <style>
              body {
                margin: 0;
                padding: 16px;
                font-family: system-ui, -apple-system, sans-serif;
              }
              ${css}
            </style>
          </head>
          <body>
            ${html}
            <script>
              // Send height updates to parent
              function sendHeight() {
                const height = document.body.scrollHeight;
                window.parent.postMessage({ type: 'resize', height }, '*');
              }
              
              // Send initial height
              sendHeight();
              
              // Watch for changes
              const observer = new ResizeObserver(sendHeight);
              observer.observe(document.body);
            </script>
          </body>
        </html>
      `

      iframeDoc.open()
      iframeDoc.write(content)
      iframeDoc.close()
    } catch (error) {
      console.error('Error rendering sandboxed HTML:', error)
      onError?.(error as Error)
    }
  }, [html, css, onError])

  return (
    <div className="w-full overflow-hidden rounded-lg border border-gray-200 bg-white" data-testid="sandboxed-html">
      <iframe
        ref={iframeRef}
        sandbox="allow-scripts"
        className="w-full border-0"
        style={{ height: `${height}px` }}
        title="Sandboxed HTML Content"
        data-testid="sandbox-iframe"
      />
    </div>
  )
}
