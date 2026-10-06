import { useEffect, useRef, useState } from 'react'
import { GlobalWorkerOptions, getDocument } from 'pdfjs-dist'
import workerSrc from 'pdfjs-dist/build/pdf.worker.min.mjs?url'
import type { PageGeometry, Point2D, WallAnalysisResponse } from '../types/api'
import { GeometryOverlay } from './GeometryOverlay'

GlobalWorkerOptions.workerSrc = workerSrc

interface Props {
  file: File
  geometry: PageGeometry
  calibrationPoints: Point2D[]
  onPickPoint: (point: Point2D) => void
  walls: WallAnalysisResponse | null
}

export function PdfGeometryViewer({ file, geometry, calibrationPoints, onPickPoint, walls }: Props) {
  const canvasRef = useRef<HTMLCanvasElement | null>(null)
  const [renderError, setRenderError] = useState<string | null>(null)

  useEffect(() => {
    let cancelled = false
    let loadingTask: ReturnType<typeof getDocument> | null = null

    async function renderPdf() {
      const canvas = canvasRef.current
      if (!canvas) return
      setRenderError(null)

      try {
        const data = new Uint8Array(await file.arrayBuffer())
        loadingTask = getDocument({ data })
        const pdf = await loadingTask.promise
        const page = await pdf.getPage(1)
        if (cancelled) return

        const baseViewport = page.getViewport({ scale: 1 })
        const targetCssWidth = Math.min(1400, Math.max(700, geometry.width))
        const renderScale = (targetCssWidth / baseViewport.width) * Math.min(window.devicePixelRatio || 1, 2)
        const viewport = page.getViewport({ scale: renderScale })
        canvas.width = Math.ceil(viewport.width)
        canvas.height = Math.ceil(viewport.height)
        canvas.style.width = '100%'
        canvas.style.height = '100%'

        await page.render({ canvas, viewport }).promise
      } catch (error) {
        if (!cancelled) {
          setRenderError(error instanceof Error ? error.message : 'No fue posible renderizar el PDF.')
        }
      }
    }

    void renderPdf()
    return () => {
      cancelled = true
      void loadingTask?.destroy()
    }
  }, [file, geometry.width])

  return (
    <div className="pdf-overlay-shell" style={{ aspectRatio: `${geometry.width} / ${geometry.height}` }}>
      <canvas ref={canvasRef} className="pdf-canvas" />
      <div className="geometry-overlay-layer">
        <GeometryOverlay
          geometry={geometry}
          calibrationPoints={calibrationPoints}
          onPickPoint={onPickPoint}
          walls={walls}
          showPageBackground={false}
        />
      </div>
      {renderError && <div className="pdf-render-error">PDF.js: {renderError}</div>}
    </div>
  )
}
