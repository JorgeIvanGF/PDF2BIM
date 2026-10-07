# F02-H00 — Plan

## Algoritmo
La primera implementación correctness-first comparaba todos los pares, con complejidad O(n²). El perfilado de T-011 justificó reemplazar la enumeración exhaustiva por una búsqueda conservadora con:

- buckets angulares de ancho igual a la tolerancia angular y sus buckets vecinos;
- una grilla uniforme sobre las cajas envolventes de cada segmento, expandidas por el espesor máximo admitido y el desvío angular máximo;
- comprobaciones geométricas originales después del prefiltrado;
- orden lexicográfico de índices para conservar el orden de evaluación, los IDs y el orden estable de resultados.

El índice solo elimina pares que no pueden cumplir las reglas geométricas actuales. La prueba diferencial compara los resultados indexados con una evaluación exhaustiva sobre los mismos segmentos.

## Solapamiento relativo
`min_overlap_ratio` se calcula ahora como el solapamiento proyectado dividido por la longitud del segmento fuente más largo. Así, el umbral exige soporte longitudinal en ambas líneas; el solapamiento completo de una línea corta sobre una fracción pequeña de una línea larga ya no obtiene ratio 1. El valor configurado sigue siendo 0,45.

## Confianza
Ponderación inicial:
- 35% paralelismo
- 40% proximidad al espesor nominal
- 25% proporción de solapamiento

Estos pesos son heurísticos explícitos y deberán recalibrarse con fixtures reales.

## Perfilado real y análisis de T-012/T-013
Validación ejecutada sobre `samples/PLANO PDF LEO.pdf`, página completa, con calibración 17.6444686 mm/unidad PDF, reglas de 100 mm y 200 mm ±15 mm, tolerancia angular 1.5°, solapamiento mínimo 300 mm y ratio 0.45.

- Entrada: 11148 segmentos raw y 10360 normalizados.
- Antes: 968 candidatos; detección directa 204.796 s; 53,659,620 pares posibles.
- Después: 726 candidatos; detección directa 12.275 s; 1,830,795 pares de broadphase y 1,712,254 pares que pasan el filtro angular.
- La comparación de pares fuente entre la salida anterior filtrada por el nuevo ratio y la salida indexada encontró equivalencia exacta: 726 pares coincidentes, ninguno omitido ni añadido por el índice.
- Los grupos de primera planta pasan de 34 registros a 6. Desaparecen G1, G2, G4, G5, G7 y G8; G6 y G9 permanecen como falsos positivos confirmados. G3 desaparece por su ratio geométrico de solapamiento, pero continúa sin clasificación semántica.
- Los 6 registros restantes corresponden a G6 y G9. El filtro elimina 24 de los 30 registros pertenecientes a grupos confirmados como falsos positivos en esta zona. Esta muestra no mide precisión global y no contiene ningún grupo confirmado como muro real.
- La redundancia global agrupada por regla y ejes redondeados a 0.01 unidad PDF pasa de 246 grupos/901 registros a 197 grupos/661 registros. Esta agrupación solo sirve para analizar redundancia y no forma parte del detector.
- En la zona de primera planta no hay candidatos de eje mayores de 815.3 mm antes del filtro ni después. La superposición deja tramos largos de muros visibles sin candidato.
- Se encontró un par vertical de 6031.9 mm con separación geométrica de 256.7 mm. Las reglas activas solo admiten espesores de 85–115 mm y 185–215 mm, por lo que el par queda fuera de configuración. Esto es una causa geométrica verificable de omisión bajo las reglas usadas; no se añadió un tipo de 250 mm.

La geometría de G1, G2, G4, G5, G7 y G8 contiene pares cuyo solapamiento cubre una fracción pequeña de la línea fuente más larga. G6 y G9 son pares cortos de longitudes similares y superan el ratio, por lo que esta regla no los separa de un muro corto usando solo estos atributos. T-012 permanece pendiente; quedan falsos positivos confirmados y no hay una referencia positiva real confirmada para medir cobertura.

### Análisis adicional de T-012
Se inspeccionaron los segmentos fuente y el contexto geométrico local de G6 y G9. G6 produce cuatro registros sobre el mismo eje por combinaciones redundantes de líneas verticales próximas; sus líneas representativas miden aproximadamente 500.2 mm y 350.1 mm, con separación de 100.0 mm, solapamiento de 350.1 mm y ratio 0.700. G9 produce dos registros; ambas líneas miden aproximadamente 469.7 mm, con separación de 105.6 mm, solapamiento completo y ratio 1.000. Ambos pares son verticales y cumplen las reglas actuales de espesor, ángulo y solapamiento.

Como análisis descriptivo, la geometría vecina a 5/10/20 unidades PDF del eje cuenta 10/19/73 segmentos para G6 y 2/2/18 para G9. Hay cruces geométricos locales y redundancia en ambos casos, pero ninguna de estas señales está definida como semántica de muro en el alcance. Una regla por densidad o intersecciones también podría rechazar encuentros válidos; una regla por estilo o redundancia tampoco separa ambos grupos de forma común. No se implementa un nuevo rechazo sin positivos reales etiquetados que permitan medir el riesgo.

Se añadieron guardas sintéticas para muros aislados y en encuentro, de 100 mm y 200 mm de espesor, con longitudes de 350 mm y 470 mm. Los ocho controles son detectados. Estas pruebas protegen muros cortos válidos frente a futuros cambios, pero no constituyen evidencia de precisión sobre planos reales. G6 y G9 permanecen como falsos positivos confirmados y T-012 sigue parcial.

La respuesta API ya no emite la advertencia obsoleta que anunciaba comparación exhaustiva e indexación futura. El hito continúa EN VALIDACIÓN.
