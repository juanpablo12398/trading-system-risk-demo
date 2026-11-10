# Documentación pública · Trading System Risk demo

El repositorio publica una consola React ilustrativa y una extracción Python de infraestructura de agentes. Sigue el patrón de índice, especificación, SDD, decisión, recorrido y calidad de Find Me, pero **no contiene ni documenta la estrategia privada**. Los parámetros y eventos son inventados.

| Sección | Documento | Propósito |
| --- | --- | --- |
| 01 · Alcance | [Especificación](../../specs/001-public-risk-demo/spec.md) | Requisitos y exclusiones verificables. |
| 02 · Diseño | [SDD](../../specs/001-public-risk-demo/sdd.md) | Puertas ilustrativas, estados y flujo. |
| 02 · Agentes | [Extracción Python](../02-arquitectura/EXTRACCION_AGENTES.md) | Procedencia, flujo LLM, memoria y límites. |
| 02 · SDD agentes | [SDD 002](../../specs/002-public-agent-slice/sdd.md) | Contratos, flujo, riesgos y criterios del recorte Python. |
| 03 · Ejecución | [Plan y tareas](../../specs/001-public-risk-demo/tasks.md) | Trabajo implementado en la muestra. |
| 03 · Desarrollo | [Guía local](../03-desarrollo/GUIA_LOCAL.md) | Instalación y estructura del código. |
| 04 · Decisiones | [ADR 001](../08-adr/001-sin-ejecucion.md) | Por qué la consola no puede operar. |
| 05 · Uso | [Recorrido](../04-usuario/RECORRIDO.md) | Escenarios para evaluar. |
| 06 · Calidad | [Estrategia de pruebas](../06-calidad/ESTRATEGIA_TESTING.md) | Casos, comandos y límites. |
| 07 · Publicación | [Guía de publicación](../05-despliegue/GUIA_PUBLICACION.md) | Bundle estático y validación previa. |

**Evidencia:** `src/App.jsx`, `src/App.test.jsx`, `agent_sample/` con 21 tests Python, `docs/preview.png` y el workflow de CI.
