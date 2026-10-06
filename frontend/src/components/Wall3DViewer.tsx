import { useEffect, useRef } from 'react'
import * as THREE from 'three'
import * as OBC from '@thatopen/components'
import type { WallCandidate } from '../types/api'

interface Props {
  walls: WallCandidate[]
  heightMm?: number
}

interface Bounds2D {
  minX: number
  minY: number
  maxX: number
  maxY: number
}

function getBounds(walls: WallCandidate[]): Bounds2D | null {
  if (!walls.length) return null
  const xs = walls.flatMap((w) => [w.axis_start_mm.x, w.axis_end_mm.x])
  const ys = walls.flatMap((w) => [w.axis_start_mm.y, w.axis_end_mm.y])
  return {
    minX: Math.min(...xs),
    minY: Math.min(...ys),
    maxX: Math.max(...xs),
    maxY: Math.max(...ys),
  }
}

export function Wall3DViewer({ walls, heightMm = 2700 }: Props) {
  const containerRef = useRef<HTMLDivElement | null>(null)

  useEffect(() => {
    const container = containerRef.current
    if (!container || !walls.length) return

    const components = new OBC.Components()
    const worlds = components.get(OBC.Worlds)
    const world = worlds.create<OBC.SimpleScene, OBC.SimpleCamera, OBC.SimpleRenderer>()

    world.scene = new OBC.SimpleScene(components)
    world.renderer = new OBC.SimpleRenderer(components, container, { antialias: true })
    world.camera = new OBC.SimpleCamera(components)
    world.scene.setup()

    const bounds = getBounds(walls)
    if (!bounds) return

    const centerX = (bounds.minX + bounds.maxX) / 2
    const centerY = (bounds.minY + bounds.maxY) / 2
    const heightM = heightMm / 1000
    const material = new THREE.MeshLambertMaterial({ color: 0xb9cbc7 })
    const geometries: THREE.BoxGeometry[] = []

    for (const wall of walls) {
      const startX = (wall.axis_start_mm.x - centerX) / 1000
      const startZ = -(wall.axis_start_mm.y - centerY) / 1000
      const endX = (wall.axis_end_mm.x - centerX) / 1000
      const endZ = -(wall.axis_end_mm.y - centerY) / 1000

      const dx = endX - startX
      const dz = endZ - startZ
      const lengthM = Math.hypot(dx, dz)
      const thicknessM = wall.nominal_thickness_mm / 1000
      if (lengthM <= 0 || thicknessM <= 0) continue

      const geometry = new THREE.BoxGeometry(lengthM, heightM, thicknessM)
      geometries.push(geometry)
      const mesh = new THREE.Mesh(geometry, material)
      mesh.position.set((startX + endX) / 2, heightM / 2, (startZ + endZ) / 2)
      mesh.rotation.y = -Math.atan2(dz, dx)
      mesh.userData = { wallId: wall.id, wallType: wall.wall_type_name }
      world.scene.three.add(mesh)
    }

    components.init()

    const extentM = Math.max(
      (bounds.maxX - bounds.minX) / 1000,
      (bounds.maxY - bounds.minY) / 1000,
      4,
    )
    const cameraDistance = Math.max(6, extentM * 1.25)
    world.camera.controls.setLookAt(
      cameraDistance * 0.75,
      cameraDistance * 0.8,
      cameraDistance * 0.75,
      0,
      heightM * 0.35,
      0,
      false,
    )

    return () => {
      components.dispose()
      for (const geometry of geometries) geometry.dispose()
      material.dispose()
    }
  }, [walls, heightMm])

  if (!walls.length) return null
  return <div ref={containerRef} className="viewer-3d" aria-label="Vista 3D preliminar de muros detectados" />
}
