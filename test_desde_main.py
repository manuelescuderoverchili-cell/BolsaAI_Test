"""
Test que imita exactamente cómo main.py ejecuta el análisis comparativo
"""
import sys
import os

# Añadir src al path como lo hace main.py
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from comparative_analyzer import ComparativeAnalyzer

print("="*70)
print("TEST: Analisis Comparativo desde main.py")
print("="*70)
print()

# Crear analizador comparativo
comparative = ComparativeAnalyzer()

print("Analizando activos...")
print()

# Analizar todos los activos (sin callback para evitar problemas)
results = comparative.analyze_all_assets(
    period='1mo',
    interval='1d'
)

print(f"\nAnalisis completado: {len(results)} activos")
print()

# Generar PDF
print("Generando PDF...")
pdf_path = comparative.generate_pdf_report(period='1mo', interval='1d')

if pdf_path:
    print(f"\nPDF generado: {pdf_path}")
    
    # Verificar tamaño
    import os
    size = os.path.getsize(pdf_path)
    print(f"Tamano del PDF: {size:,} bytes")
    
    if size > 200000:
        print("OK - El PDF parece incluir graficos (>200KB)")
    else:
        print("ERROR - El PDF NO parece incluir graficos (<200KB)")
else:
    print("ERROR generando PDF")

print()
print("="*70)
print("TEST COMPLETADO")
print("="*70)
