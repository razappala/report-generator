# src/test_generator.py

def get_test_data():
    return { 
        "empresa_evaluada": "TechCorp S.A.", 
        "estandar": "ISO 27001:2022", 
        "procesos": [ 
            { 
                "nombre": "Gestión de Riesgos", 
                "porcentaje_cumplimiento": 75, 
                "actividades": [ 
                    { 
                        "nombre": "Identificación de Activos", 
                        "porcentaje_cumplimiento": 80, 
                        "tareas": [ 
                            { 
                                "nombre": "Inventario de Activos", 
                                "porcentaje_cumplimiento": 90, 
                                "preguntas": [ 
                                    {"texto": "¿Existe un inventario actualizado de activos?", "cumplimiento": "Sí"}, 
                                    {"texto": "¿Se clasifican los activos por criticidad?", "cumplimiento": "No"} 
                                ] 
                            } 
                        ] 
                    } 
                ] 
            } 
        ], 
        "conclusiones": [ 
            "Cumplimiento general del 78% según los controles evaluados", 
            "Se requiere mejorar la documentación de procesos" 
        ], 
        "recomendaciones": [ 
            "Implementar sistema de gestión de activos antes de Q3 2024", 
            "Realizar auditoría interna trimestral" 
        ] 
    }

def test_generator():
    try:
        from pdf_generator import PDFGeneratorFactory
        
        print("\nIniciando generación de PDF...")
        
        # Crear instancia del generador
        generator = PDFGeneratorFactory.create_generator()
        
        # Obtener datos de prueba
        data = get_test_data()
        
        # Generar HTML desde el template
        print("Generando HTML desde template...")
        html_content = generator.render_template('report_template.html', data)
        
        # Generar PDF
        print("Generando PDF...")
        pdf_content = generator.generate_pdf(
            html_content,
            css_file='static/css/styles.css'
        )
        
        # Guardar PDF
        output_file = 'reporte.pdf'
        with open(output_file, 'wb') as f:
            f.write(pdf_content)
        
        print(f"PDF generado exitosamente: {output_file}")
        return True
    except Exception as e:
        print(f"Error al generar PDF: {str(e)}")
        return False

if __name__ == '__main__':
    print("=== Generador de Reportes PDF ===")
    test_generator()