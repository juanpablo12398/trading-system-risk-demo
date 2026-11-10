# ADR 001 · Muestra sin ruta de órdenes

**Estado:** vigente. La decisión de mantener desactivadas las órdenes se conserva en el [SDD 003](../../specs/003-connected-paper-cycle/sdd.md).

## Contexto

Un portfolio puede mostrar orquestación, evaluación y controles sin exponer cuentas, estrategia o capacidad operativa del sistema experimental.

## Decisión

La muestra ejecuta un ciclo Python **solo de papel** con datos y transporte de modelo ficticios. Los adaptadores de mercado son de solo lectura. FastAPI expone ciclo, modo e historial; no hay endpoint de órdenes. Los umbrales están rotulados como ilustrativos.

## Consecuencias

Se pueden comprobar contratos, agentes, controles, replay y auditoría en un recorrido conectado. La ausencia de ejecución limita el alcance de la evidencia y evita confundir la demo con un sistema desplegable o rentable.
