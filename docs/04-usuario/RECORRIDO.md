# Recorrido de la demo

1. Ejecutar `npm ci` y `npm run dev`; abrir la dirección local de Vite.
2. Observar `Simulation`, `DRY RUN Always on`, tres PASS y `Live orders Disabled`.
3. Desmarcar `Market data is fresh`: la decisión cambia a `Blocked` y se identifica el control fallido.
4. Restaurar ese control y desmarcar `Exclusive authority held`: aparece `Missing` y se bloquea el camino.
5. Restaurar la autoridad y mover el slider a 60 y 61; el primero pasa y el segundo bloquea.
6. Abrir `Show sample trace` y volver a ocultarla; los cuatro eventos son estáticos y ficticios.

No hay rutas de compra, venta o envío de órdenes. La UI no usa feeds de mercado.
