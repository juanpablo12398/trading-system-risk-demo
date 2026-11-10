# Estrategia de pruebas · Trading System público

La suite comprueba el **ciclo de papel publicado** con Vitest/Testing Library y `unittest`. No certifica el sistema privado ni su aptitud para operar.

| Riesgo | Verificación automática |
| --- | --- |
| La UI simula un resultado sin backend | Tests de `App.jsx` y `api.js` comprueban solicitudes, respuesta y error. |
| Datos de mercado incorrectos o falta parcial | Tests de normalización, REST GET, WebSocket, fuente caída y símbolo incompatible. |
| Fallo o fuga de contexto entre agentes | Orquestador, memoria por ciclo, timeout y fallos parciales. |
| Modelo o revisor promueve entrada rechazada | Tests del transporte, JSON, reintentos, veto y rechazo preexistente. |
| Evaluación usa información futura | Tests de holdout, replay y rechazo de filas posteriores. |
| El modelo predictivo aprende del holdout | Tests de entrenamiento cronológico, primer pronóstico invariante ante valores futuros, comparación con persistencia y bloqueo del ciclo por calidad insuficiente. |
| Un control fallido permite continuar | Tests de frescura, autoridad, completitud, veto y borde de exposición. |
| Se pierde auditoría | Prueba de ida y vuelta en PostgreSQL de CI; memoria en local sin base. |
| Se expone una ruta de orden | Test del contrato HTTP comprueba que no existe. |

```bash
python -m unittest discover -s agent_sample -p 'test_*.py' -v
npm ci
npm run test:coverage
npm run build
```

La suite publica pruebas React y Python para el ciclo conectado y el modelo predictivo sintético. En la última medición local, `App.jsx` y `api.js` alcanzaron 97,77 % de sentencias, 94 % de ramas, 90,9 % de funciones y 100 % de líneas; CI exige mínimos de 75/65/75/75 %. Una prueba Python de PostgreSQL se omite sin `TEST_POSTGRES_DSN` y se ejecuta con el servicio de CI.

Los adaptadores de mercado y modelo se prueban con dobles: no se contacta a un exchange ni a Claude en CI. El replay usa observaciones ficticias. Ninguna prueba demuestra rendimiento, rentabilidad, resistencia distribuida o seguridad del sistema privado.
