# AgroVive-M5-Dashboard · Estado de evidencias

**Revisión:** 2026-10-22 · **Madurez:** Demostrador agrícola / investigación de visión artificial

## Inventario de calidad

- README: sí.
- Archivo LICENSE: **no**. No asumir AGPL, MIT u otra licencia hasta confirmar derechos.
- CI en main: no se ha detectado workflow verificable.
- Capturas reales de interfaz: no hay capturas reproducibles acreditadas en main.
- Las imágenes de datasets, vídeos externos y material de promoción NO equivalen a validación experimental.

## Limitaciones

Los resultados de precisión, latencia, comparativas y ahorro energético del README original son históricos y requieren reproducción con datasets y protocolo publicados.

**EVIDENCIA PENDIENTE:** el rendimiento y las cifras de consumo divulgados previamente no están acreditados como benchmarks independientes reproducibles. La galería contiene imágenes agrícolas de ejemplo, no capturas verificadas de ejecución.

## Plan de recuperación

1. Identificar procedencia y licencias del código, datasets, pesos y contenido.
2. Fijar un conjunto de datos y una partición sin leakage; archivar hashes, versiones y semillas.
3. Publicar script de inferencia end-to-end en un entorno reproducible.
4. Ejecutar métricas con intervalos e incertidumbre adecuada y pruebas independientes.
5. Solo entonces actualizar el README con afirmaciones cuantitativas validadas.
