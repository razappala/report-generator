# src/pdf_generator.py
from abc import ABC, abstractmethod
from jinja2 import Environment, FileSystemLoader
import io
from xhtml2pdf import pisa

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

class XHTML2PDFGenerator(PDFGenerator):
    """XHTML2PDF implementation of PDF generator"""
    
    def generate_pdf(self, html_content: str, css_file: str = None) -> bytes:
        output = io.BytesIO()
        
        # Si hay archivo CSS, incluirlo en el HTML
        if css_file:
            try:
                with open(css_file, 'r', encoding='utf-8') as f:
                    css_content = f.read()
                html_content = f'''
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
                print(f"Advertencia: No se encontró el archivo CSS: {css_file}")
        
        # Convertir HTML a PDF
        try:
            pisa_status = pisa.CreatePDF(
                src=html_content,
                dest=output,
                show_error_as_pdf=True
            )
            
            # Verificar si hubo errores
            if pisa_status.err:
                raise Exception('Errores encontrados durante la generación del PDF')
                
            return output.getvalue()
            
        except Exception as e:
            raise Exception(f'Error al generar PDF: {str(e)}')

class PDFGeneratorFactory:
    """Factory class for creating PDF generators"""
    
    @staticmethod
    def create_generator(generator_type: str = 'xhtml2pdf') -> PDFGenerator:
        generators = {
            'xhtml2pdf': XHTML2PDFGenerator
        }
        
        generator_class = generators.get(generator_type.lower())
        if not generator_class:
            raise ValueError(f'Tipo de generador {generator_type} no soportado. Tipos disponibles: {", ".join(generators.keys())}')
        
        return generator_class()