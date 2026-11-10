# SDD 004 · Evidencia predictiva sintética

## Necesidad

La etapa 003 permitía evaluar probabilidades ya provistas, pero no mostraba
entrenamiento ni inferencia. La afirmación del CV sobre modelos predictivos
necesita un ejemplo verificable sin revelar el modelo, las variables, las
señales o los datos del sistema privado.

## Alcance y diseño

- `agent_sample/predictive.py` ajusta una regresión lineal de un rezago a
  valores de un índice totalmente ficticio. Es un modelo supervisado mínimo,
  elegido por ser inspeccionable, no por su utilidad para operar.
- El prefijo temporal es el único conjunto de entrenamiento. El sufijo es un
  holdout posterior; el primer pronóstico solo recibe el último dato del
  prefijo. No se reentrena con resultados del holdout.
- Se informa MAE del modelo y de una referencia de persistencia. No se
  interpreta la diferencia como ventaja económica.
- `pipeline.py` añade esta evaluación al ciclo conectado y a la traza.
  `src/App.jsx` muestra los resultados devueltos por la API.

## Límites de publicación

Los números, coeficientes ajustados y umbrales son ficticios. No se publica
ningún artefacto entrenado, variable real, etiqueta privada, dataset,
estrategia, prompt, acceso a exchange ni ruta de órdenes. La muestra demuestra
la separación entre entrenamiento y evaluación, no reproduce el ML privado ni
acredita su desempeño.

## Pruebas

`test_predictive.py` verifica ajuste e inferencia, comparación con la línea
de base, ausencia de influencia de valores futuros en el primer pronóstico,
serie constante, entradas inválidas y presencia del resultado en el ciclo
FastAPI. La suite completa del repositorio se ejecuta en GitHub Actions.

## Criterios de aceptación

1. Hay código y pruebas públicos de entrenamiento e inferencia sintéticos.
2. El ciclo React → FastAPI → Python muestra las métricas reales de ese código.
3. No aparecen datos, pesos ni reglas del sistema privado.
4. El resultado no se presenta como una estrategia rentable o lista para
   producción.
