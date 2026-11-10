# Guía de desarrollo local

Requisitos: Python 3.11+, Node.js y npm. Docker con Compose permite probar la persistencia PostgreSQL; sin ella, la API declara que usa memoria. No se requieren cuenta de exchange ni clave de modelo.

```bash
docker compose up -d
python -m pip install -r requirements-demo.txt
```

Definir `POSTGRES_DSN=postgresql://postgres:postgres@127.0.0.1:5433/trading_public_demo` en la terminal del servidor y ejecutar:

```bash
uvicorn agent_sample.api_app:app --host 127.0.0.1 --port 8082
```

En otra terminal:

```bash
npm ci
npm run dev
```

Abrir `http://localhost:5173`. Vite reenvía `/api` a FastAPI. El botón ejecuta un ciclo Python con entradas y transporte de modelo ficticios; el resultado y el historial se obtienen desde la API. `exchange.py` ofrece adaptadores REST/WebSocket de **solo lectura**, probados con transportes simulados, pero el escenario de la UI no llama a mercados reales.

```bash
python -m unittest discover -s agent_sample -p 'test_*.py' -v
npm run test:coverage
npm run build
```

GitHub Actions define `TEST_POSTGRES_DSN` para ejercitar la prueba PostgreSQL. No añadir claves, cuentas, reglas reales o rutas de órdenes al repositorio público.
