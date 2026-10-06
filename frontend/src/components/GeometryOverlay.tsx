import type { MouseEvent } from 'react'
import type { PageGeometry, Point2D, WallAnalysisResponse } from '../types/api'

interface Props {
  geometry: PageGeometry
  calibrationPoints?: Point2D[]
  onPickPoint?: (point: Point2D) => void
  walls?: WallAnalysisResponse | null
  showPageBackground?: boolean
}

export function GeometryOverlay({ geometry, calibrationPoints = [], onPickPoint, walls, showPageBackground = true }: Props) {
  function pick(event: MouseEvent<SVGSVGElement>) {
    if (!onPickPoint) return
    const rect = event.currentTarget.getBoundingClientRect()
    const x = ((event.clientX - rect.left) / rect.width) * geometry.width
    const y = ((event.clientY - rect.top) / rect.height) * geometry.height
    onPickPoint({ x, y })
  }

  const factor = walls?.calibration.mm_per_pdf_unit ?? null

  return (
    <svg
      className="geometry-canvas"
      viewBox={`0 0 ${geometry.width} ${geometry.height}`}
      role="img"
      aria-label={`Geometría vectorial extraída: ${geometry.segments.length} segmentos`}
      onClick={pick}
    >
      {showPageBackground && <rect x="0" y="0" width={geometry.width} height={geometry.height} className="page-bg" />}
      {geometry.segments.map((segment) => (
        <line
          key={segment.id}
          x1={segment.start.x}
          y1={segment.start.y}
          x2={segment.end.x}
          y2={segment.end.y}
          className="detected-line"
          vectorEffect="non-scaling-stroke"
        />
      ))}

      {factor && walls?.wall_candidates.map((wall) => (
        <line
          key={wall.id}
          x1={wall.axis_start_mm.x / factor}
          y1={wall.axis_start_mm.y / factor}
          x2={wall.axis_end_mm.x / factor}
          y2={wall.axis_end_mm.y / factor}
          className="wall-axis"
          vectorEffect="non-scaling-stroke"
        />
      ))}

      {calibrationPoints.map((point, index) => (
        <g key={`${point.x}-${point.y}-${index}`}>
          <circle cx={point.x} cy={point.y} r="6" className="calibration-point" vectorEffect="non-scaling-stroke" />
          <text x={point.x + 8} y={point.y - 8} className="calibration-label">{index === 0 ? 'A' : 'B'}</text>
        </g>
      ))}
    </svg>
  )
}
