# Estrategia de pruebas · Trading System público

La suite comprueba la interfaz ilustrativa y el recorte Python de agentes, no el proyecto de trading privado. Usa Vitest, Testing Library, jsdom y `unittest` estándar.

| Riesgo de la muestra | Verificación automática |
| --- | --- |
| Confundir elegibilidad con orden real | Estado inicial y `Live orders Disabled`. |
| Continuar con datos antiguos | Casilla de frescura produce `Blocked`. |
| Continuar sin autoridad | Casilla de autoridad produce `Missing` y bloqueo. |
| Error de borde en límite inventado | 60 pasa, 61 bloquea y 0 pasa. |
| Traza que aparenta ejecución | Se abre y cierra una muestra estática; permanece el texto de que no puede operar. |
| Fallo parcial del sistema de agentes | Orquestador conserva resultados sanos ante excepción y timeout. |
| Ruta LLM no ejercitada | Transporte falso comprueba entrada/salida, reintentos, JSON inválido y timeout. |
| Cruce de memoria entre ciclos | Dos tareas concurrentes no leen el valor de la otra. |
| Fuente caída o sin datos | Agente sigue con fuente sana y no llama al LLM si no hay titulares. |
| Modelo intenta promover una entrada rechazada | Revisor no la envía al LLM; veto y revisión manual no se convierten en aprobación. |

## Comandos

```bash
npm ci
npm test
npm run test:coverage
npm run build
python -m unittest discover -s agent_sample -p 'test_*.py' -v
```

GitHub Actions ejecuta los comandos en push y pull request. El build comprueba que se produce el bundle, y los tests ejercitan controles y resultados del DOM.

La suite contiene **8 casos React y 30 Python**. La medición local con V8 dio 100 % de sentencias, ramas, funciones y líneas instrumentadas de `src/App.jsx`. CI exige al menos 90 % en cada categoría. Ese porcentaje describe únicamente la lógica React de la muestra, no el módulo Python ni la seguridad de un sistema de trading.

**Límites:** los tests Python usan fuentes y transporte falsos. No prueban modelos reales, mercados, concurrencia distribuida, estrategias, ejecución, pérdidas, autenticación o rentabilidad. Ningún test de esta demo puede certificar que el sistema privado sea seguro para operar.
