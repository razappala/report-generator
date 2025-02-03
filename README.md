# PDF Report Generator

Generador de reportes PDF utilizando diferentes librerías de Python (`xhtml2pdf`, `WeasyPrint`, `pdfkit`).

## 🚀 Ejecución del Proyecto

1. **Construir la imagen de Docker:**

```bash
docker build -t pdf-generator:latest .
```

2. **Ejecutar las pruebas:**

```bash
docker run --rm -it \
  -v $(pwd)/src:/app/src \
  -v $(pwd)/static:/app/static \
  -v $(pwd)/tests:/app/tests \
  -v $(pwd)/output:/app/output \
  -v $(pwd)/templates:/app/templates \
  -v $(pwd)/requirements.txt:/app/requirements.txt \
  pdf-generator:latest bash -c "find . -name '*.pyc' -delete && python src/test_generator.py"
```

### 🔍 Descripción de los volúmenes:
- `src`: Código fuente del generador.
- `static`: Archivos estáticos (CSS, JS, imágenes).
- `tests`: Scripts de prueba.
- `output`: Directorio donde se guardan los PDFs generados.
- `templates`: Plantillas HTML para la generación de reportes.
- `requirements.txt`: Archivo de dependencias de Python.

## 📝 Notas
- El comando elimina archivos `.pyc` antes de ejecutar pruebas para evitar errores de caché.
- Los PDFs generados se almacenan en la carpeta `output` del host.

---

**Requisitos:** Docker y Python instalados en el entorno de desarrollo.