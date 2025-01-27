# Report Generator

Generador de reportes PDF para evaluaciones ISO.

## Instalación

1. Clonar el repositorio
2. Crear entorno virtual: `python -m venv venv`
3. Activar entorno virtual:
   - Windows: `venv\Scripts\activate`
   - Unix/MacOS: `source venv/bin/activate`
4. Instalar dependencias: `pip install -r requirements.txt`

## Uso

```python
from src.pdf_generator import PDFGeneratorFactory

# Crear generador
generator = PDFGeneratorFactory.create_generator('weasyprint')

# Generar PDF
pdf_content = generator.generate_pdf(html_content)