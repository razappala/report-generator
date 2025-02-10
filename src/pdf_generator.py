# src/pdf_generator.py
from abc import ABC, abstractmethod
from jinja2 import Environment, FileSystemLoader
import io
from xhtml2pdf import pisa
import warnings
import tempfile
import os

class PDFGenerator(ABC):
    """Abstract base class for PDF generators"""
    
    def __init__(self):
        self.jinja_env = Environment(
            loader=FileSystemLoader('templates'),
            autoescape=True
        )
    
    def render_template(self, template_name: str, data: dict) -> str:
        """Render HTML template with provided data"""
        template = self.jinja_env.get_template(template_name)
        return template.render(**data)
    
    @abstractmethod
    def generate_pdf(self, html_content: str, css_file: str = None) -> bytes:
        """Generate PDF from HTML content"""
        pass

    def _apply_css(self, html_content: str, css_file: str) -> str:
        """Helper method to wrap content with CSS"""
        try:
            with open(css_file, 'r', encoding='utf-8') as f:
                css_content = f.read()
            return f'''
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset="UTF-8">
                    <style>
                        {css_content}
                    </style>
                </head>
                <body>
                    {html_content}
                </body>
                </html>
            '''
        except FileNotFoundError:
            warnings.warn(f"CSS file not found: {css_file}", UserWarning)
            return html_content

class XHTML2PDFGenerator(PDFGenerator):
    """xhtml2pdf implementation of PDF generator"""
    
    def generate_pdf(self, html_content: str, css_file: str = None) -> bytes:
        output = io.BytesIO()
        
        if css_file:
            html_content = self._apply_css(html_content, css_file)
        
        try:
            pisa_status = pisa.CreatePDF(
                src=html_content,
                dest=output,
                show_error_as_pdf=True,
                link_callback=lambda uri, rel: f"/app/static/{uri}"
            )
            
            if pisa_status.err:
                raise RuntimeError('Errors during PDF generation')
                
            return output.getvalue()
            
        except Exception as e:
            raise RuntimeError(f'Error generating PDF: {str(e)}')

class WeasyPrintGenerator(PDFGenerator):
    """WeasyPrint implementation of PDF generator"""
    
    def generate_pdf(self, html_content: str, css_file: str = None) -> bytes:
        try:
            from weasyprint import HTML
        except ImportError:
            raise ImportError(
                "WeasyPrint is not installed. Install with: pip install weasyprint"
            )
        
        if css_file:
            html_content = self._apply_css(html_content, css_file)
        
        buffer = io.BytesIO()
        HTML(string=html_content).write_pdf(buffer)
        return buffer.getvalue()

class PDFKitGenerator(PDFGenerator):
    """pdfkit implementation of PDF generator (requires wkhtmltopdf)"""

    def generate_pdf(self, html_content: str, css_file: str = None) -> bytes:
        try:
            import pdfkit
        except ImportError:
            raise ImportError(
                "pdfkit is not installed. Install with: pip install pdfkit\n"
                "Also install wkhtmltopdf: https://wkhtmltopdf.org/"
            )

        if css_file:
            html_content = self._apply_css(html_content, css_file)

        options = {
            'encoding': 'UTF-8',
            'page-size': 'A4',
            'viewport-size': '1280x1024',
            'quiet': '',
            'enable-local-file-access': '',
            'margin-top': '20mm',
            'margin-bottom': '20mm',
            'margin-left': '20mm',
            'margin-right': '20mm'
        }

        # Crear un archivo temporal
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            temp_filename = tmp_file.name

        try:
            # Generar el PDF en el archivo temporal
            pdfkit.from_string(
                input=html_content,
                output_path=temp_filename,
                options=options
            )

            # Leer el contenido del archivo temporal en un BytesIO
            with open(temp_filename, 'rb') as f:
                pdf_content = f.read()

        finally:
            # Eliminar el archivo temporal
            if os.path.exists(temp_filename):
                os.remove(temp_filename)

        return pdf_content

class PDFGeneratorFactory:
    """Factory class for creating PDF generators"""
    
    _GENERATORS = {
        'xhtml2pdf': XHTML2PDFGenerator,
        'pdfkit': PDFKitGenerator,
        'weasyprint': WeasyPrintGenerator,
    }
    
    @classmethod
    def create_generator(cls, generator_type: str = 'xhtml2pdf') -> PDFGenerator:
        generator_class = cls._GENERATORS.get(generator_type.lower())
        if not generator_class:
            raise ValueError(
                f"Unsupported generator type: {generator_type}. "
                f"Available: {', '.join(cls._GENERATORS.keys())}"
            )
        return generator_class()
    
    @classmethod
    def get_available_generators(cls):
        return list(cls._GENERATORS.keys())