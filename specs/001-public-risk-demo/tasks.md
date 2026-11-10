# Plan y tareas · Demo pública Trading System

| Tarea | Evidencia | Estado |
| --- | --- | --- |
| Definir tres controles y umbral inventado | `evaluateDemo` | Hecho |
| Mostrar decisión explicable y fallo cerrado | `src/App.jsx` | Hecho |
| Mantener modo seco y órdenes reales deshabilitadas | UI y especificación | Hecho |
| Añadir traza estática, sin datos de mercado | `sampleEvents` | Hecho |
| Documentar alcance, diseño y decisión de aislamiento | `spec.md`, `sdd.md`, `docs/` | Hecho |
| Probar escenarios y compilar en CI | `src/App.test.jsx`, workflow | Hecho |

**Cierre:** `npm ci`, `npm test` y `npm run build` pasan; el repositorio no contiene estrategias, claves ni adaptadores de exchange. Las pruebas del sistema privado no se atribuyen a esta demo.
