# Extracción pública de agentes

## Procedencia

Esta muestra se adaptó del proyecto experimental de Juan Pablo Verdondoni. No es una copia literal ni una versión ejecutable del motor completo.

| Muestra pública | Capacidad mostrada | Qué se conserva |
| --- | --- | --- |
| `agent_sample/orchestrator.py` | Orquestación paralela | `asyncio.gather`, timeout individual, aislamiento de errores y resumen |
| `agent_sample/brain.py` | Memoria compartida | Ciclo por `ContextVar`, namespaces y lecturas/escrituras aisladas |
| `agent_sample/llm.py` | Cliente Claude | Cliente inyectable, reintentos transitorios, timeout y validación de JSON |
| `agent_sample/agents.py` | Agente de noticias | Fuentes concurrentes, fallo parcial, deduplicación, análisis LLM y escritura al brain |
| `agent_sample/reviewer.py` | Revisor LLM acotado | Solo recibe entradas preaprobadas; puede advertir o vetar, nunca promover una rechazada |

El recorrido usa fuentes y respuestas LLM ficticias; la memoria por ciclo reside en proceso y el historial de auditoría puede usar PostgreSQL. El cliente privado registra tokens y presupuesto; la muestra no demuestra esas funciones. El código de producción usa prompts, fuentes, modelo de datos y agentes adicionales que aquí no se incluyen.

## Flujo verificable

1. El caller inicia un ciclo del brain.
2. El agente recoge dos o más fuentes concurrentemente y tolera que una falle.
3. Si hay titulares, usa `ClaudeClient.ask` y exige un objeto JSON con `summary`.
4. El resultado se guarda en un namespace del ciclo.
5. El revisor puede leer ese contexto y evaluar entradas preaprobadas. Su salida no puede aprobar una entrada rechazada; un fallo del LLM exige revisión manual.
6. El orquestador puede correr agentes independientes en paralelo con timeout propio.

La prueba usa un transporte falso: verifica la ruta LLM, reintentos, JSON inválido, timeouts, fallos parciales y separación de ciclos. No hace llamadas pagas ni operaciones de exchange.

## Límites de publicación

Se omitieron estrategia, umbrales, señales, prompts privados, fuentes reales, credenciales y ejecución de órdenes. La UI React consume resultados de FastAPI generados por Python. El [modelo predictivo sintético](../../specs/004-synthetic-prediction/sdd.md) muestra entrenamiento e inferencia sin exponer el modelo privado. Las pruebas públicas no sustituyen la suite del proyecto privado.
