# Changelog

Todas las modificaciones relevantes de este proyecto se documentarán aquí.


---

## [1.0.3] - 2025-06-3

### Documentación
- Se modifica la salida por consola para informar mejor al usuario qué se está haciendo

---

## [1.0.2] - 2025-06-01

### Documentación
- Se actualizó el `README.md` para indicar que los workflows archivados no se exportan.

---

## [1.0.1] - 2025-06-01

### Cambiado
- Se actualizó la consulta SQL para excluir workflows archivados (`isArchived = false`).
- Como resultado, se eliminaron 5 archivos `.json` de workflows obsoletos en el directorio de exportación.

---

## [1.0.0] - 2025-06-01

### Agregado
- Primer versión funcional del CLI.
- Conexión por túnel SSH a PostgreSQL para obtener carpetas y workflows.
- Descarga de cada workflow vía API REST de n8n usando su ID.
- Organización de workflows por carpetas con sus archivos `.json`.
- Soporte para archivo `.env` personalizado por parámetro.
- Limpieza completa del directorio de destino antes de exportar.

---
