# Documentación pública · Trading System

Este repositorio muestra mecanismos adaptados del sistema privado con datos y umbrales inventados. El [SDD 003](../../specs/003-connected-paper-cycle/sdd.md) describe el ciclo conectado y el [SDD 004](../../specs/004-synthetic-prediction/sdd.md) añade la muestra predictiva. Los SDD anteriores registran etapas de construcción.

| Sección | Documento | Propósito |
| --- | --- | --- |
| 01 · Alcance | [Especificación inicial](../../specs/001-public-risk-demo/spec.md) | Primer escenario ficticio y exclusiones. |
| 02 · Diseño | [SDD 001](../../specs/001-public-risk-demo/sdd.md), [SDD 002](../../specs/002-public-agent-slice/sdd.md), [SDD 003](../../specs/003-connected-paper-cycle/sdd.md), [SDD 004](../../specs/004-synthetic-prediction/sdd.md) | Evolución de consola, agentes, ciclo conectado y predicción sintética. |
| 02 · Arquitectura | [Extracción de agentes](../02-arquitectura/EXTRACCION_AGENTES.md) | Procedencia y límites de la muestra. |
| 03 · Ejecución | [Plan inicial](../../specs/001-public-risk-demo/tasks.md), [guía local](../03-desarrollo/GUIA_LOCAL.md) | Comandos y estructura. |
| 04 · Decisiones | [ADR 001](../08-adr/001-sin-ejecucion.md) | Ausencia de ruta de órdenes y evolución. |
| 05 · Uso | [Recorrido](../04-usuario/RECORRIDO.md) | Escenarios para evaluar. |
| 06 · Calidad | [Estrategia de pruebas](../06-calidad/ESTRATEGIA_TESTING.md) | Matriz y límites de cobertura. |
| 07 · Publicación | [Guía de publicación](../05-despliegue/GUIA_PUBLICACION.md) | Revisión previa a compartir. |

La [matriz de evidencia del CV](../../README.md#qué-permite-comprobar-del-cv) enlaza cada afirmación técnica con archivos verificables. `docs/preview.png` retrata una etapa anterior y no representa el ciclo conectado.
