# F01-H00 — Plan

Pipeline:

```text
Segment2D(raw)
  ↓
canonicalize endpoints
  ↓
remove degenerate
  ↓
exact dedupe
  ↓
length + angle
  ↓
NormalizedSegment2D
```

La deduplicación utiliza una cuantización numérica extremadamente fina solo para absorber ruido flotante; no representa una tolerancia constructiva.
