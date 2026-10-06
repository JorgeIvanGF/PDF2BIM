import { useState } from 'react'
import { analyzeWalls, getGeometry, uploadPdf } from './api/client'
import { PdfGeometryViewer } from './components/PdfGeometryViewer'
import { Wall3DViewer } from './components/Wall3DViewer'
import type { DocumentCreated, PageGeometry, Point2D, WallAnalysisResponse, WallTypeRule } from './types/api'
import './styles.css'

const DEFAULT_WALL_TYPES: WallTypeRule[] = [
  { id: 'wall-100', name: 'Muro 100 mm', nominal_thickness_mm: 100, tolerance_mm: 15 },
  { id: 'wall-200', name: 'Muro 200 mm', nominal_thickness_mm: 200, tolerance_mm: 15 },
]

export default function App() {
  const [file, setFile] = useState<File | null>(null)
  const [result, setResult] = useState<DocumentCreated | null>(null)
  const [geometry, setGeometry] = useState<PageGeometry | null>(null)
  const [points, setPoints] = useState<Point2D[]>([])
  const [realDistanceMm, setRealDistanceMm] = useState(5000)
  const [walls, setWalls] = useState<WallAnalysisResponse | null>(null)
  const [viewMode, setViewMode] = useState<'2D' | '3D'>('2D')
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)

  async function analyzePdf() {
    if (!file) return
    setLoading(true)
    setError(null)
    setResult(null)
    setGeometry(null)
    setPoints([])
    setWalls(null)
    setViewMode('2D')
    try {
      const created = await uploadPdf(file)
      setResult(created)
      if (created.preflight.vector_compatible) setGeometry(await getGeometry(created.document_id, 1))
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : 'Error inesperado.')
    } finally {
      setLoading(false)
    }
  }

  function pickCalibrationPoint(point: Point2D) {
    setWalls(null)
    setPoints((current) => current.length >= 2 ? [point] : [...current, point])
  }

  function exportAnalysis() {
    if (!walls) return
    const blob = new Blob([JSON.stringify(walls, null, 2)], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const anchor = document.createElement('a')
    anchor.href = url
    anchor.download = `${file?.name.replace(/\.pdf$/i, '') || 'pdf2bim'}-analysis.json`
    anchor.click()
    URL.revokeObjectURL(url)
  }

  async function runWallDetection() {
    if (!result || points.length !== 2 || realDistanceMm <= 0) return
    setLoading(true)
    setError(null)
    try {
      setWalls(await analyzeWalls(
        result.document_id,
        { pointA: points[0], pointB: points[1], realDistanceMm },
        DEFAULT_WALL_TYPES,
      ))
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : 'Error inesperado.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="shell">
      <header className="hero">
        <span className="eyebrow">PDF → GEOMETRÍA → MUROS</span>
        <h1>PDF2BIM Lab</h1>
        <p>Prototipo determinista para leer geometría vectorial, calibrarla y proponer ejes de muro antes de entrar a BIM/Revit.</p>
      </header>

      <section className="card upload-card">
        <label className="file-picker">
          <span>{file ? file.name : 'Seleccionar PDF'}</span>
          <input type="file" accept="application/pdf,.pdf" onChange={(event) => setFile(event.target.files?.[0] ?? null)} />
        </label>
        <button disabled={!file || loading} onClick={analyzePdf}>{loading ? 'Procesando…' : 'Analizar PDF'}</button>
      </section>

      {error && <section className="card error">{error}</section>}

      {result && (
        <section className="card">
          <div className="status-row">
            <div><span className="label">Compatibilidad vectorial</span><strong>{result.preflight.vector_compatible ? 'Compatible' : 'No compatible'}</strong></div>
            <span className={result.preflight.vector_compatible ? 'pill ok' : 'pill warn'}>{result.preflight.vector_compatible ? 'VECTOR' : 'REVISAR'}</span>
          </div>
          <div className="metrics">
            <article><strong>{result.preflight.total_segments}</strong><span>segmentos raw</span></article>
            <article><strong>{result.preflight.total_drawing_paths}</strong><span>paths</span></article>
            <article><strong>{result.preflight.total_images}</strong><span>imágenes</span></article>
            <article><strong>{result.preflight.page_count}</strong><span>páginas</span></article>
          </div>
        </section>
      )}

      {geometry && (
        <>
          <section className="card calibration-card">
            <div>
              <span className="label">Calibración</span>
              <strong>Toca dos puntos con una distancia conocida</strong>
              <p>{points.length}/2 puntos seleccionados. Al tocar un tercero se reinicia la selección.</p>
            </div>
            <label className="distance-field">
              <span>Distancia real (mm)</span>
              <input type="number" min="1" value={realDistanceMm} onChange={(e) => setRealDistanceMm(Number(e.target.value))} />
            </label>
            <button disabled={points.length !== 2 || loading} onClick={runWallDetection}>Detectar muros 100 / 200 mm</button>
          </section>

          <section className="card viewer-card">
            <div className="viewer-heading">
              <div><span className="label">Página {geometry.page_number}</span><strong>{viewMode === '2D' ? 'Geometría reconstruida' : 'Modelo 3D preliminar'}</strong></div>
              <div className="view-switch" role="group" aria-label="Cambiar vista">
                <button className={viewMode === '2D' ? 'active' : ''} onClick={() => setViewMode('2D')}>2D</button>
                <button disabled={!walls?.wall_candidates.length} className={viewMode === '3D' ? 'active' : ''} onClick={() => setViewMode('3D')}>3D</button>
              </div>
            </div>
            {viewMode === '2D' ? (
              <>
                <div className="viewer-frame">
                  {file && (
                    <PdfGeometryViewer
                      file={file}
                      geometry={geometry}
                      calibrationPoints={points}
                      onPickPoint={pickCalibrationPoint}
                      walls={walls}
                    />
                  )}
                </div>
                <div className="legend"><span><i className="line raw" /> Segmentos</span><span><i className="line axis" /> Ejes de muro</span></div>
              </>
            ) : (
              <Wall3DViewer walls={walls?.wall_candidates ?? []} />
            )}
          </section>
        </>
      )}

      {walls && (
        <section className="card">
          <span className="label">Resultado geométrico preliminar</span>
          <h2>{walls.wall_candidates.length} candidatos de muro</h2>
          <p className="muted">Normalización: {walls.raw_segment_count} segmentos raw → {walls.normalized_segment_count} únicos. Escala: {walls.calibration.mm_per_pdf_unit.toFixed(3)} mm/u PDF.</p>
          <button className="secondary-action" onClick={exportAnalysis}>Exportar análisis JSON</button>
          <div className="wall-list">
            {walls.wall_candidates.slice(0, 20).map((wall) => (
              <article key={wall.id}>
                <strong>{wall.wall_type_name}</strong>
                <span>{wall.measured_thickness_mm.toFixed(1)} mm · {(wall.length_mm / 1000).toFixed(2)} m · {(wall.confidence_score * 100).toFixed(0)}%</span>
              </article>
            ))}
          </div>
        </section>
      )}
    </main>
  )
}
