export interface Point2D {
  x: number
  y: number
}

export interface Segment2D {
  id: string
  page_number: number
  start: Point2D
  end: Point2D
  source_path_index: number
  source_item_index: number
  source_kind: string
  style: {
    width: number | null
    color_rgb: [number, number, number] | null
    dashes: string | null
    opacity: number | null
  }
}

export interface PageGeometry {
  page_number: number
  width: number
  height: number
  segments: Segment2D[]
  unsupported_item_count: number
}

export interface DocumentPreflight {
  filename: string
  page_count: number
  vector_compatible: boolean
  total_drawing_paths: number
  total_segments: number
  total_images: number
  total_text_blocks: number
  warnings: string[]
  pages: Array<{
    page_number: number
    width: number
    height: number
    drawing_path_count: number
    extracted_segment_count: number
    image_count: number
    text_block_count: number
    unsupported_vector_item_count: number
  }>
}

export interface DocumentCreated {
  document_id: string
  preflight: DocumentPreflight
}

export interface WallTypeRule {
  id: string
  name: string
  nominal_thickness_mm: number
  tolerance_mm: number
}

export interface WallCandidate {
  id: string
  axis_start_mm: Point2D
  axis_end_mm: Point2D
  measured_thickness_mm: number
  nominal_thickness_mm: number
  length_mm: number
  wall_type_rule_id: string
  wall_type_name: string
  confidence_score: number
  source_segment_ids: [string, string]
  status: 'DETECTED' | 'CONFIRMED' | 'MODIFIED' | 'REJECTED'
  warnings: string[]
}

export interface WallAnalysisResponse {
  page_number: number
  raw_segment_count: number
  normalized_segment_count: number
  calibration: {
    mm_per_pdf_unit: number
    measured_pdf_distance: number
    real_distance_mm: number
  }
  wall_candidates: WallCandidate[]
  warnings: string[]
}
