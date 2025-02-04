# src/test_generator.py
import os
import shutil

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
    
def clean_output_folder():
    """Limpia la carpeta output antes de generar nuevos archivos."""
    output_folder = 'output'
    if os.path.exists(output_folder):
        # Eliminar todos los archivos en la carpeta output
        for filename in os.listdir(output_folder):
            file_path = os.path.join(output_folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"Error al eliminar {file_path}: {e}")
    else:
        # Crear la carpeta output si no existe
        os.makedirs(output_folder, exist_ok=True)

def test_generator():
    from pdf_generator import PDFGeneratorFactory
    
    # Limpiar la carpeta output antes de generar nuevos archivos
    clean_output_folder()
    
    print("\n" + "="*55)
    print("=== TESTEO DE TODOS LOS GENERADORES DISPONIBLES ===")
    print("="*55)
    
    # Obtener todos los tipos de generadores registrados
    available_generators = PDFGeneratorFactory.get_available_generators()
    
    results = {
        'success': [],
        'errors': []
    }

    for generator_type in available_generators:
        try:
            print(f"\n\n🔁 [{generator_type.upper()}] Iniciando prueba...")
            
            # Crear instancia del generador
            generator = PDFGeneratorFactory.create_generator(generator_type)
            print(f"✅ [{generator_type.upper()}] Factory creada")
            
            # Obtener datos de prueba
            data = get_test_data()
            
            # Fase 1: Generar HTML
            print(f"🖨️ [{generator_type.upper()}] Renderizando template...")
            html_content = generator.render_template('index.html', data)
            
            # Fase 2: Generar PDF
            print(f"📄 [{generator_type.upper()}] Convirtiendo a PDF...")
            pdf_content = generator.generate_pdf(
                html_content, 
                css_file='static/css/styles2.css'
            )
            
            # Guardar PDF
            # Guardar PDF en la carpeta output
            output_file = f'output/reporte_{generator_type}.pdf'
            with open(output_file, 'wb') as f:
                f.write(pdf_content)
            
            print(f"🎉 [{generator_type.upper()}] Éxito! Archivo: {output_file}")
            results['success'].append(generator_type)
            
        except ImportError as e:
            error_msg = f"🚫 [{generator_type.upper()}] Dependencias faltantes: {str(e)}"
            print(error_msg)
            results['errors'].append(error_msg)
            
        except Exception as e:
            error_msg = f"❌ [{generator_type.upper()}] Error: {type(e).__name__} - {str(e)}"
            print(error_msg)
            results['errors'].append(error_msg)
            
        print(f"⏳ [{generator_type.upper()}] Prueba completada")
        print("-" * 60)

    # Reporte final
    print("\n\n" + "="*55)
    print("=== RESUMEN FINAL ===")
    print(f"Generadores probados: {len(available_generators)}")
    print(f"✅ Éxitos: {len(results['success'])}")
    print(f"🚫 Errores: {len(results['errors'])}")
    
    if results['errors']:
        print("\nDetalle de errores:")
        for error in results['errors']:
            print(f"  • {error}")
    
    print("="*55 + "\n")
    
    return len(results['errors']) == 0

if __name__ == '__main__':
    print("\n" + "="*55)
    print("=== SISTEMA DE PRUEBAS DE GENERADORES PDF ===")
    print("="*55 + "\n")
    test_generator()