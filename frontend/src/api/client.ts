import type { DocumentCreated, PageGeometry, Point2D, WallAnalysisResponse, WallTypeRule } from '../types/api'

const API_BASE = import.meta.env.VITE_API_BASE ?? 'http://localhost:8000/api'

export async function uploadPdf(file: File): Promise<DocumentCreated> {
  const formData = new FormData()
  formData.append('file', file)

  const response = await fetch(`${API_BASE}/documents`, {
    method: 'POST',
    body: formData,
  })

  if (!response.ok) {
    const payload = await response.json().catch(() => null)
    throw new Error(payload?.detail ?? 'No fue posible analizar el PDF.')
  }

  return response.json()
}

export async function getGeometry(documentId: string, page = 1): Promise<PageGeometry> {
  const response = await fetch(`${API_BASE}/documents/${documentId}/geometry?page=${page}`)
  if (!response.ok) throw new Error('No fue posible recuperar la geometría.')
  return response.json()
}


export async function analyzeWalls(
  documentId: string,
  calibration: { pointA: Point2D; pointB: Point2D; realDistanceMm: number },
  wallTypes: WallTypeRule[],
): Promise<WallAnalysisResponse> {
  const response = await fetch(`${API_BASE}/documents/${documentId}/analyze-walls`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      page: 1,
      calibration: {
        point_a: calibration.pointA,
        point_b: calibration.pointB,
        real_distance_mm: calibration.realDistanceMm,
      },
      wall_types: wallTypes,
    }),
  })
  if (!response.ok) {
    const payload = await response.json().catch(() => null)
    throw new Error(payload?.detail ?? 'No fue posible detectar muros.')
  }
  return response.json()
}
