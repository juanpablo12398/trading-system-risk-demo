# Guía de desarrollo local

**Requisito:** Node.js 24 y npm. No se necesita exchange, feed de mercado, base de datos, modelo ni archivo `.env`.

```bash
npm ci
npm run dev
npm test
npm run build
npm run preview
```

`src/App.jsx` contiene las entradas ficticias, `evaluateDemo` y la traza estática. `src/styles.css` compone la consola adaptable. `src/App.test.jsx` prueba bloqueos, límite y traza; `vitest.config.js` configura jsdom. `src/main.jsx` monta la pantalla.

Si se cambia el límite ilustrativo, actualizar juntos la etiqueta de la UI, la especificación, el SDD y el test de borde. Nunca reemplazarlo por un parámetro real ni añadir claves o rutas de órdenes al repositorio público.
