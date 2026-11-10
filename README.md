# Trading System · muestra pública de ingeniería

La interfaz React ejecuta un **ciclo de papel** en una API Python/FastAPI. El ciclo normaliza dos entradas con formato REST y WebSocket, coordina agentes, usa una frontera Claude inyectable, evalúa predicciones sintéticas, reproduce decisiones históricas ficticias, aplica controles y guarda una traza en PostgreSQL cuando está configurado. Todo el recorrido se puede seguir en [el código](agent_sample/pipeline.py) y [la interfaz](src/App.jsx).

**El sistema experimental completo es privado.** Esta muestra adapta mecanismos de su arquitectura. Las entradas, respuestas del modelo, métricas y límites numéricos son inventados; no incluyen estrategia, señales privadas, claves, cuentas ni ejecución de órdenes. El ciclo visible usa transportes ficticios; los adaptadores de [lectura REST/WebSocket](agent_sample/exchange.py) están separados y probados con transportes simulados. El [adaptador Anthropic](agent_sample/llm.py) es opcional y no se invoca desde la interfaz.

## Qué permite comprobar del CV

| Afirmación | Evidencia pública | Límite |
| --- | --- | --- |
| Multiagentes Python, asincronía y estado compartido | [orquestador](agent_sample/orchestrator.py), [agente de contexto](agent_sample/agents.py), [agente de calidad y flujo](agent_sample/pipeline.py), [revisor acotado](agent_sample/reviewer.py), [memoria por ciclo](agent_sample/brain.py) | Se publican patrones adaptados, no todos los agentes privados |
| Claude API | [cliente y adaptador SDK](agent_sample/llm.py), pruebas de JSON, reintentos, fallos y veto | En demo se usa un transporte falso; no se hacen llamadas pagas |
| Datos de exchange REST/WebSocket | [lectores de solo lectura](agent_sample/exchange.py), pruebas de HTTP GET y frame WebSocket | No hay conexión a un exchange durante el demo |
| PostgreSQL y auditoría | [almacén JSONB](agent_sample/audit.py), [prueba integrada](agent_sample/test_full_sample.py) | La alternativa en memoria se indica en pantalla si no se configura PostgreSQL |
| Evaluación ML y backtesting | [métricas holdout y replay de papel](agent_sample/evaluation.py), pruebas de información futura y drawdown | Observaciones y aprobaciones son ficticias; no se publica ni entrena el modelo privado |
| Controles de riesgo y trazabilidad | [gates de demostración](agent_sample/risk.py), [pipeline](agent_sample/pipeline.py), [API](agent_sample/api_app.py) | El límite de exposición no corresponde al sistema real |

## Ejecutar localmente

Requisitos: Python 3.11+, Node.js y Docker.

```bash
docker compose up -d
python -m pip install -r requirements-demo.txt
```

Definí `POSTGRES_DSN=postgresql://postgres:postgres@127.0.0.1:5433/trading_public_demo` en tu terminal y ejecutá:

```bash
uvicorn agent_sample.api_app:app --host 127.0.0.1 --port 8082
```

En otra terminal:

```bash
npm ci
npm run dev
```

Abrí `http://localhost:5173`. La interfaz usa el proxy de Vite hacia la API local. Sin `POSTGRES_DSN`, la API usa memoria y lo declara en el panel; las demás capacidades de la muestra siguen funcionando.

## Verificación

```bash
python -m unittest discover -s agent_sample -p 'test_*.py' -v
npm run test:coverage
npm run build
```

[GitHub Actions](.github/workflows/verify.yml) ejecuta también la prueba de ida y vuelta contra PostgreSQL. La [documentación](docs/00-indice/INDICE.md) incluye los SDD por etapa, decisiones, límites y matriz de pruebas.

**Alcance:** muestra de ingeniería en modo papel, no asesoramiento financiero ni sistema de trading desplegable. Copyright © Juan Pablo Verdondoni. No se concede licencia de reutilización.
