# Publicación del código de muestra

El repositorio está publicado como código fuente, sin sitio alojado declarado. La interfaz actual necesita la API Python. Para ejecutarla, seguir la [guía local](../03-desarrollo/GUIA_LOCAL.md). Para producir el bundle:

```bash
npm ci
npm test
npm run build
```

Vite escribe `dist/`; ese directorio aislado no ofrece el ciclo conectado. GitHub Actions valida pruebas y build, pero no despliega. Antes de compartir el código, comprobar que el modo de papel y las órdenes desactivadas siguen visibles, que no aparecen claves ni rutas de órdenes y que los eventos y parámetros permanecen ficticios.
