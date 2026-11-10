# Especificación · Consola de riesgo ficticia

**Estado:** implementada. **Tipo:** demostración de interfaz. Ni los datos ni la función de evaluación son el motor privado de Trading System.

## Propósito

Mostrar cómo una UI puede hacer visibles los motivos de bloqueo antes de una acción simulada. La persona puede variar tres entradas ficticias y comprobar que cualquier control fallido detiene el camino ilustrativo. No se conecta a mercados ni permite operar.

## Requisitos funcionales

1. Mostrar modo `Simulation`, `DRY RUN Always on` y `Live orders Disabled` en todo momento.
2. Evaluar tres controles de muestra: frescura de datos, autoridad exclusiva y exposición ilustrativa no mayor que 60 unidades.
3. Mostrar `Blocked` si cualquiera falla; mostrar qué control pasó o falló y un mensaje explicativo.
4. Permitir cambiar dos casillas y un slider de 0 a 100; el límite 60 debe pasar y 61 debe bloquear.
5. Mostrar u ocultar una traza estática de cuatro eventos sintéticos.

## Fuera de alcance

Market data, modelos, prompts, estrategias, órdenes, APIs de exchange, backtesting, autenticación, persistencia, orquestación de agentes y parámetros de riesgo reales. La etiqueta `Eligible for simulation` no autoriza ninguna operación.

## Criterios de aceptación

| ID | Resultado observable |
| --- | --- |
| TS-01 | Escenario inicial apto para simulación, tres controles PASS y órdenes reales deshabilitadas. |
| TS-02 | Datos antiguos o falta de autoridad producen bloqueo. |
| TS-03 | Exposición 60 pasa; 61 bloquea; 0 vuelve a pasar. |
| TS-04 | La traza ficticia se abre y se cierra; no hay botón de ejecución. |
| TS-05 | `npm test` y `npm run build` terminan correctamente. |
