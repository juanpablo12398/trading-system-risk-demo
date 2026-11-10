# SDD 002 · Infraestructura pública de agentes

## Problema y alcance

La consola React 001 no prueba el trabajo con agentes declarado en el CV. Este recorte Python muestra mecanismos adaptados de los agentes privados sin publicar estrategia, señales, prompts ni conexiones de trading.

## Componentes

- `NewsReviewAgent`: obtiene fuentes inyectadas concurrentemente, tolera una fuente caída, deduplica titulares, solicita JSON al LLM y guarda resultado por namespace.
- `ClaudeClient`: transporte asíncrono inyectable, timeout, hasta tres intentos ante fallos transitorios y validación estricta de objeto JSON. `AnthropicTransport` es un adaptador opcional al SDK real; los tests no lo instancian.
- `SharedBrain`: memoria en proceso aislada por ciclo mediante `ContextVar`, con copias de entrada/salida.
- `run_agents`: fan-out con `asyncio.gather`, timeout por agente, resultado de error sin exponer mensajes y conteo final.

## Flujo de datos

1. El caller inicia ciclo en el task actual.
2. Provee funciones de fuentes y transporte; no hay red por defecto.
3. El agente consulta fuentes y llama al LLM solo con datos presentes.
4. Si el JSON no cumple contrato o el transporte falla, guarda `status=error`; no produce una señal aprobada.
5. El orquestador aísla el fallo de un agente y conserva el resultado de los demás.

## Seguridad y límites

No hay órdenes, exchange, estrategia ni umbrales. Los titulares en pruebas son ficticios. El transporte real requiere una clave entregada explícitamente al constructor; no hay clave en el repo. La memoria pública no usa la persistencia SQLite/PostgreSQL del proyecto privado. Esta muestra no valida rentabilidad, calidad del modelo ni operación en producción.

## Pruebas y criterios

Los 21 tests Python incluyen: respuesta JSON directa y cercada, rechazo de JSON inválido y arrays, llamada LLM simulada, reintentos agotados, timeout, aislamiento de memoria entre tareas, agente sin datos, fuente caída, respuesta LLM incompleta, paralelismo real, fallo y timeout de agentes. Se ejecutan en CI junto con los 8 tests React.

## Trazabilidad

Ver [procedencia exacta](../../docs/02-arquitectura/EXTRACCION_AGENTES.md). El recorte es una adaptación de mecanismos, no un volcado de código privado.
