# Recorrido del ciclo de papel

1. Iniciar la API Python y Vite según la [guía local](../03-desarrollo/GUIA_LOCAL.md). La pantalla indica si el historial usa PostgreSQL o memoria.
2. Pulsar **Run paper cycle**. La API devuelve fuentes ficticias REST/WebSocket, dos resultados de agentes, veredicto del revisor, evaluación de holdout, replay, controles y traza. El historial recibe un evento.
3. Desmarcar **Market data is fresh** y ejecutar otro ciclo: el control de frescura bloquea el camino de papel.
4. Restaurar frescura y desmarcar **Exclusive authority held**: falta autoridad y el camino se bloquea.
5. Activar **Context reviewer veto**: el revisor rechaza la entrada candidata; una entrada previamente rechazada nunca se promueve.
6. Variar **Illustrative exposure** entre 60 y 61: el primero alcanza el límite ficticio y el segundo se bloquea.

Cada cambio requiere ejecutar el ciclo de nuevo; la UI borra resultados anteriores para no presentarlos como actuales. No hay ruta de órdenes, conexión de cuenta ni estrategia privada. Las métricas no son resultados de mercado real.
