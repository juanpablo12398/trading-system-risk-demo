# ADR 001 · Consola sin ruta de ejecución

**Estado:** aceptada para la muestra pública.

## Contexto

Un portfolio puede mostrar cómo se presenta una decisión de riesgo, pero publicar conexiones de mercado, adaptadores de exchange o reglas propietarias crearía una copia engañosa y potencialmente sensible del sistema experimental.

## Decisión

Crear una interfaz React con entradas y traza inventadas, sin backend ni botón de orden. Mantener siempre `DRY RUN` y `Live orders Disabled`. La función de evaluación usa un umbral ficticio rotulado como tal.

## Consecuencias

El evaluador puede comprobar cambios de estado, bordes y explicación de bloqueos. La muestra no permite operar ni respalda afirmaciones sobre seguridad o rentabilidad del sistema privado. Cualquier discusión de parámetros reales queda fuera de este repositorio.
