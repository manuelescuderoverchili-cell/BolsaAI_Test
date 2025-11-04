"""
Test simple para verificar las noticias y gráficos en el PDF comparativo
"""
from src.comparative_pdf_generator import ComparativePDFGenerator

# Datos de prueba simulados
fake_results = [
    {
        'activo': 'Bitcoin',
        'ticker': 'BTC-USD',
        'categoria': '🟢 MUY ALCISTA',
        'score_rentabilidad': 85.5,
        'precio_actual': 68500.00,
        'precio_objetivo': 75000.00,
        'retorno_esperado': 9.5,
        'direccion': 'Alcista',
        'confianza': 85,
        'rsi': 58.5,
        'volatilidad': 2.3,
        'patrones_alcistas': 5,
        'patrones_bajistas': 1,
        'tendencia': 'Alcista',
        'recomendacion': 'COMPRA FUERTE'
    },
    {
        'activo': 'Ethereum',
        'ticker': 'ETH-USD',
        'categoria': '🟢 ALCISTA',
        'score_rentabilidad': 72.3,
        'precio_actual': 2650.00,
        'precio_objetivo': 2900.00,
        'retorno_esperado': 9.4,
        'direccion': 'Alcista',
        'confianza': 75,
        'rsi': 55.2,
        'volatilidad': 2.8,
        'patrones_alcistas': 4,
        'patrones_bajistas': 2,
        'tendencia': 'Alcista',
        'recomendacion': 'COMPRA'
    },
    {
        'activo': 'Tesla',
        'ticker': 'TSLA',
        'categoria': '🟡 NEUTRAL-ALCISTA',
        'score_rentabilidad': 65.1,
        'precio_actual': 242.00,
        'precio_objetivo': 260.00,
        'retorno_esperado': 7.4,
        'direccion': 'Neutral',
        'confianza': 60,
        'rsi': 51.8,
        'volatilidad': 3.2,
        'patrones_alcistas': 3,
        'patrones_bajistas': 2,
        'tendencia': 'Neutral',
        'recomendacion': 'MANTENER'
    }
]

print("="*70)
print("TEST: PDF Comparativo con Noticias y Gráficos")
print("="*70)
print()

try:
    print("📄 Generando PDF comparativo...")
    print(f"   Activos incluidos: {len(fake_results)}")
    print()
    
    generator = ComparativePDFGenerator()
    pdf_path = generator.generate_comparative_pdf(
        results=fake_results,
        period='1mo',
        interval='1d'
    )
    
    print()
    print("="*70)
    print("✅ PDF GENERADO EXITOSAMENTE")
    print("="*70)
    print(f"\n📁 Archivo: {pdf_path}\n")
    
    print("🔍 Verifica que el PDF incluya:")
    print("   1. ✅ Tabla con 'Tiempo Estimado' en cada activo")
    print("   2. ✅ Gráfico histórico de precio para cada activo")
    print("   3. ✅ Sección '📰 NOTICIAS CLAVE RECIENTES' con:")
    print("      - Enlaces clickeables en azul")
    print("      - Descripciones en cursiva")
    print("      - Fechas de publicación")
    print("   4. ✅ Análisis y recomendación detallada")
    print()
    
except Exception as e:
    print(f"\n❌ Error generando PDF: {e}")
    import traceback
    traceback.print_exc()

print("="*70)
print("TEST COMPLETADO")
print("="*70)
