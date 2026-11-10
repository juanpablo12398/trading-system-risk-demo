# SDD 003 · Ciclo público conectado y solo de papel

## Propósito y límites

Esta muestra reproduce mecanismos de ingeniería del Trading System privado con datos, respuestas de modelo y umbrales inventados. Los SDD 001 y 002 describen etapas anteriores; este SDD define el recorrido integrado actual. No hay claves, cuentas, señales propietarias, órdenes ni inferencia sobre rentabilidad.

## Recorrido observable

1. `src/App.jsx` solicita modo e historial a FastAPI y envía un escenario a `/api/demo/cycle`.
2. `agent_sample/pipeline.py` obtiene dos cotizaciones ficticias con formato REST y WebSocket mediante las interfaces de `exchange.py`. Los adaptadores reales de lectura se prueban con clientes simulados, sin contactar a un exchange.
3. `SharedBrain` abre un ciclo. `run_agents` coordina en paralelo un agente de contexto y uno de calidad de datos. `ClaudeClient` recibe un transporte ficticio; la frontera Anthropic opcional está aislada en `llm.py`.
4. `ReviewGuardAgent` revisa una entrada previamente aprobada y conserva el rechazo anterior. El modelo no puede convertir una entrada rechazada en aprobada.
5. `evaluation.py` calcula métricas de holdout y reproduce decisiones de papel con filas fijas, comprobando que no se use información posterior.
6. `risk.py` calcula controles de frescura, autoridad, completitud, revisión y exposición con un umbral ilustrativo. Cualquier fallo bloquea el camino de papel. `live_orders` permanece desactivado.
7. `audit.py` guarda el resultado y la traza en JSONB de PostgreSQL si se configura `POSTGRES_DSN`; de lo contrario usa memoria y la UI lo indica.

## Responsabilidades y contratos

| Capa | Responsabilidad | Fuera del recorte |
| --- | --- | --- |
| React/Vite | Escenarios, resultados, métricas y trazas | Operación de cuentas |
| FastAPI | Contratos de ciclo, modo e historial | Rutas de órdenes |
| Agentes y memoria | Orquestación asincrónica, contexto y revisión acotada | Agentes y prompts privados |
| Evaluación y controles | Holdout, replay y bloqueo de muestra | Modelo, estrategia y límites reales |
| PostgreSQL | Historial de eventos ficticios | Registros de operaciones reales |

## Criterios de aceptación

- La interfaz obtiene un ciclo generado por Python y permite observar fuentes, agentes, revisión, métricas, controles, traza e historial.
- Datos antiguos, falta de autoridad, veto, exposición superior al umbral y datos incompletos bloquean el camino.
- El adaptador de mercado solo lee; las rutas HTTP no incluyen órdenes.
- Pruebas Python cubren el flujo, adaptadores, errores parciales, evaluación, límites y persistencia PostgreSQL en CI. Pruebas React cubren el consumo de API y los cambios de escenario.
- La documentación distingue siempre los mecanismos verificables del comportamiento del sistema privado.

## Trazabilidad y límites de evidencia

La [matriz del README](../../README.md#qué-permite-comprobar-del-cv) enlaza afirmaciones técnicas con archivos y pruebas. El ciclo de la UI usa datos y transporte de modelo ficticios: muestra integración y responsabilidades, pero no demuestra desempeño del modelo privado ni seguridad para operar.
