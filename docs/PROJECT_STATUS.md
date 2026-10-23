# AgroVive-M5-Dashboard · Estado de evidencias

**Revisión:** 2026-10-23 · **Madurez:** Demostrador agrícola / investigación de visión artificial

## Inventario de calidad

- README: sí.
- Archivo LICENSE: **sí**, AGPL-3.0 para el código según el archivo actual; verificar separadamente licencias de pesos, datasets, fotografías y demás recursos.
- CI en main: **sí**, `.github/workflows/ci.yml` realiza comprobación sintáctica y documental, **sin ejecutar modelos ni validar resultados**. También existe `.github/workflows/repository-quality.yml` para integridad documental.
- Capturas reales de interfaz: no hay capturas reproducibles acreditadas en main.
- Las imágenes de datasets, vídeos externos y material de promoción NO equivalen a validación experimental.

## Limitaciones

Los resultados de precisión, latencia, comparativas y ahorro energético del README original son históricos y requieren reproducción con datasets y protocolo publicados.

**EVIDENCIA PENDIENTE:** el rendimiento y las cifras de consumo divulgados previamente no están acreditados como benchmarks independientes reproducibles. La galería contiene imágenes agrícolas de ejemplo, no capturas verificadas de ejecución.

## Plan de recuperación

1. Mantener la licencia AGPL-3.0 del código y verificar procedencia, atribuciones y derechos de redistribución de datasets, pesos y fotografías.
2. Fijar un conjunto de datos y una partición sin leakage; archivar hashes, versiones y semillas.
3. Publicar script de inferencia end-to-end en un entorno reproducible.
4. Ejecutar métricas con intervalos e incertidumbre adecuada y pruebas independientes.
5. Solo entonces actualizar el README con afirmaciones cuantitativas validadas.
