Aquí tienes el archivo `README.md` completo y actualizado, ajustado para reflejar los cambios realizados en el enfoque del proyecto:

---

# Report Generator

Este proyecto es un generador de informes en formato PDF que utiliza diferentes bibliotecas de Python (`xhtml2pdf`, `WeasyPrint`, `pdfkit`) para convertir plantillas HTML en archivos PDF. El proyecto está diseñado para ser ejecutado en un contenedor Docker, lo que facilita la instalación de dependencias y librerías sin necesidad de configurar un entorno local.

## Estructura del Proyecto

La estructura del proyecto es la siguiente:

```
REPORT_GENERATOR/
│
├── output/                  # Carpeta donde se guardan los archivos PDF generados
├── src/                     # Código fuente del proyecto
│   ├── __pycache__/         # Caché de Python (generado automáticamente)
│   ├── __init__.py          # Archivo de inicialización del módulo
│   ├── pdf_generator.py     # Lógica principal para generar PDFs
│   └── test_generator.py    # Script para probar los generadores de PDF
│
├── static/                  # Archivos estáticos (CSS, imágenes, etc.)
│   ├── css/                 # Archivos CSS
│   │   └── styles.css       # Estilos para las plantillas HTML
│   ├── img/                 # Imágenes (opcional)
│   └── templates/           # Plantillas HTML
│       └── report_template.html  # Plantilla base para los informes
│
├── tests/                   # Pruebas unitarias
│   ├── __init__.py          # Archivo de inicialización del módulo de pruebas
│   └── test_pdf_generator.py  # Pruebas para los generadores de PDF
│
├── venv/                    # Entorno virtual (opcional, no incluido en Docker)
│   ├── Dockerfile           # Archivo Dockerfile para construir la imagen
│   └── requirements.txt     # Dependencias de Python
│
├── Dockerfile               # Dockerfile para construir la imagen del proyecto
└── README.md                # Este archivo
```

---

## Requisitos

- **Docker**: Asegúrate de tener Docker instalado en tu sistema. Puedes descargarlo desde [aquí](https://www.docker.com/get-started).
- **Git**: Para clonar el repositorio.

---

## Clonar el Proyecto

Para clonar el repositorio, ejecuta el siguiente comando en tu terminal:

```bash
git clone https://github.com/tu-usuario/report-generator.git
cd report-generator
```

---

## Construir la Imagen Docker

Para construir la imagen Docker del proyecto, ejecuta el siguiente comando en la raíz del proyecto:

```bash
docker build -t pdf-generator:latest .
```

### ¿Cuándo Reconstruir la Imagen?

Solo necesitas reconstruir la imagen Docker en los siguientes casos:
1. **Cambias las dependencias**: Si modificas `requirements.txt` o agregas nuevas bibliotecas.
2. **Modificas el `Dockerfile`**: Si cambias la configuración del contenedor (por ejemplo, instalas nuevas herramientas del sistema).
3. **Cambias la estructura del proyecto**: Si agregas nuevos directorios o archivos que no están incluidos en la imagen.

---

## Ejecutar el Contenedor

Una vez que la imagen esté construida, puedes ejecutar el contenedor con el siguiente comando:

```bash
docker run --rm -it \
  -v $(pwd)/output:/app/output \
  pdf-generator:latest
```

### Explicación

- **`-v $(pwd)/output:/app/output`**: Monta la carpeta `output` del host en `/app/output` del contenedor. Aquí se guardarán los archivos PDF generados.
- **No es necesario montar volúmenes para el código fuente**: Todo el código y recursos se copian en la imagen Docker durante la construcción.

---

## Flujo de Trabajo Eficiente

1. **Edita los archivos en tu host**:
   - Realiza los cambios que necesites en los archivos del proyecto (por ejemplo, `src/pdf_generator.py`, `static/templates/report_template.html`, etc.).

2. **Reconstruir la imagen (solo si es necesario)**:
   - Si cambiaste dependencias o el `Dockerfile`, reconstruye la imagen:
     ```bash
     docker build -t pdf-generator:latest .
     ```

3. **Ejecutar el contenedor**:
   - Ejecuta el contenedor para probar los cambios:
     ```bash
     docker run --rm -it \
       -v $(pwd)/output:/app/output \
       pdf-generator:latest
     ```

4. **Verifica los resultados**:
   - Los archivos PDF generados se guardarán en la carpeta `output` en tu host.

---

## Probar los Generadores de PDF

El proyecto incluye un script de prueba (`test_generator.py`) que prueba todos los generadores de PDF disponibles (`xhtml2pdf`, `WeasyPrint`, `pdfkit`). Este script se ejecuta automáticamente al iniciar el contenedor.

### Resultados de la Prueba

- Los archivos PDF generados se guardarán en la carpeta `output` en tu host.
- Si algún generador falla, se mostrará un mensaje de error en la consola.

---

## Dependencias

Las dependencias del proyecto están listadas en el archivo `requirements.txt`. Estas dependencias se instalan automáticamente al construir la imagen Docker.

---

## Personalización

### Plantillas HTML

Puedes modificar o agregar nuevas plantillas HTML en la carpeta `static/templates`. Asegúrate de que las plantillas sigan la estructura esperada por el script `pdf_generator.py`.

### Estilos CSS

Los estilos CSS se encuentran en `static/css/styles.css`. Puedes modificar este archivo para cambiar el diseño de los informes generados.

---

## Contribuir

Si deseas contribuir a este proyecto, sigue estos pasos:

1. Haz un fork del repositorio.
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`).
3. Realiza tus cambios y haz commit (`git commit -m 'Añadir nueva funcionalidad'`).
4. Haz push a la rama (`git push origin feature/nueva-funcionalidad`).
5. Abre un Pull Request.

---

## Licencia

Este proyecto está bajo la licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.

---

### Nota Final

Este flujo de trabajo simplificado te permite editar el código directamente en tu host y usar Docker principalmente para gestionar dependencias y librerías. ¡Esperamos que sea útil y que disfrutes usando este generador de informes! 😊

---

Con este `README.md` actualizado, los usuarios tendrán una guía clara y detallada para clonar, construir, ejecutar y personalizar el proyecto sin necesidad de reconstruir la imagen Docker constantemente. ¡Espero que sea útil! 😊