# Evidencia y límites — AgroVive M5

**Revisión: 2026-10-22 · Clasificación: prototipo de investigación agrícola.**

## Estado observado

La interfaz de demostración y los modelos serializados aparecen en el repositorio. El README anterior recogía afirmaciones muy elevadas de accuracy, comparaciones SOTA, consumo y latencia **sin acompañarlas de una reproducción suficientemente trazable en esta rama**. Se conservan como material histórico, no como métricas validadas.

## Requisitos para validar

1. Fuente, licencia, hash y contenido del dataset (incluidos duplicados, mismo cultivo y correlación entre imágenes).
2. División train/validation/test antes de extraer cualquier dato dependiente de la clase, ajustar PCA o aplicar aumentación.
3. Transformaciones RAW→modelo serializadas, originales auditables, código y versiones exactas.
4. Predicciones por muestra con identificadores, matrices de confusión, métricas por clase e intervalos.
5. Comparación con baselines en el mismo split, hardware y límites de inferencia.
6. Latencia p50/p95, RAM y consumo medido por imagen, no estimado; evidencia fotográfica de la planta no equivale a diagnóstico validado.

## Gestión de derechos

El código está declarado AGPL-3.0 en la raíz. Los pesos, datasets e imágenes de ejemplo podrían tener derechos independientes; se debe inventariar y verificar su redistribución antes de lanzar paquetes. No subir datos de fincas ni imágenes de terceros sin autorización.

**Alcance:** no adoptar decisiones automatizadas de pesticidas, seguridad alimentaria o daños en cultivos basándose únicamente en esta demo.
