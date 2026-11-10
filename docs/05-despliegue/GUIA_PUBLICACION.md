# Publicación de la muestra estática

El repositorio está publicado como código fuente, sin sitio alojado declarado. Para producir el bundle:

```bash
npm ci
npm test
npm run build
```

Vite escribe `dist/`; un hosting estático puede servirlo sin backend. GitHub Actions valida test y build, pero no despliega. Antes de alojarlo, comprobar que `DRY RUN` y `Live orders Disabled` siguen visibles, que no aparece una acción de orden y que los eventos y parámetros permanecen ficticios.
