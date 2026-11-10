# Estrategia de pruebas · Trading System público

La suite comprueba **la interfaz ilustrativa**, no el proyecto de trading privado. Usa Vitest, Testing Library y jsdom.

| Riesgo de la muestra | Verificación automática |
| --- | --- |
| Confundir elegibilidad con orden real | Estado inicial y `Live orders Disabled`. |
| Continuar con datos antiguos | Casilla de frescura produce `Blocked`. |
| Continuar sin autoridad | Casilla de autoridad produce `Missing` y bloqueo. |
| Error de borde en límite inventado | 60 pasa, 61 bloquea y 0 pasa. |
| Traza que aparenta ejecución | Se abre y cierra una muestra estática; permanece el texto de que no puede operar. |

## Comandos

```bash
npm ci
npm test
npm run test:coverage
npm run build
```

GitHub Actions ejecuta los comandos en push y pull request. El build comprueba que se produce el bundle, y los tests ejercitan controles y resultados del DOM.

La suite actual contiene **8 casos**. La medición local con V8 dio 100 % de sentencias, ramas, funciones y líneas instrumentadas de `src/App.jsx`. CI exige al menos 90 % en cada categoría. Ese porcentaje describe únicamente la lógica React de la muestra, no la seguridad de un sistema de trading.

**Límites:** no se prueban modelos, mercados, concurrencia distribuida, estrategias, ejecución, pérdidas, autenticación o rentabilidad. Ningún test de esta demo puede certificar que el sistema privado sea seguro para operar.
