"""
Test de la comparativa mejorada con noticias, tiempo de retorno y gráficos
"""
from src.comparative_analyzer import ComparativeAnalyzer
from src.comparative_pdf_generator import ComparativePDFGenerator
from datetime import datetime

# Configuración
activos = {
    'Bitcoin': 'BTC-USD',
    'Ethereum': 'ETH-USD',
    'Tesla': 'TSLA'
}

period = '1mo'  # 1 mes de datos
interval = '1d'  # Intervalo diario

print("="*70)
print("TEST: Análisis Comparativo Mejorado")
print("="*70)
print(f"\n📊 Activos a analizar: {len(activos)}")
print(f"📅 Periodo: {period}")
print(f"⏱️ Intervalo: {interval}\n")

# Crear analizador comparativo
comparative = ComparativeAnalyzer()

print(f"\n{'='*70}")
print(f"🔍 ANALIZANDO TODOS LOS ACTIVOS")
print(f"{'='*70}\n")

try:
    # Realizar análisis de todos los activos
    results = comparative.analyze_all_assets(
        period=period,
        interval=interval,
        callback=lambda msg: print(f"   {msg}")
    )
    
    print(f"\n✅ Análisis completado: {len(results)} activos procesados")
    
    for r in results[:3]:  # Mostrar top 3
        print(f"\n   {r['activo']} ({r['ticker']})")
        print(f"      Score: {r['score_rentabilidad']:.1f}/100")
        print(f"      Dirección: {r['direccion']} ({r['confianza']:.0f}%)")
        print(f"      Retorno: {r['retorno_esperado']:+.2f}%")
    
except Exception as e:
    print(f"❌ Error en análisis: {e}")
    import traceback
    traceback.print_exc()
    results = []

print(f"\n{'='*70}")
print(f"📈 GENERANDO PDF COMPARATIVO MEJORADO")
print(f"{'='*70}\n")

if results:
    print(f"✅ {len(results)} activos analizados exitosamente\n")
    print("📄 Generando PDF con:")
    print("   ✅ Tiempo estimado hasta retorno esperado")
    print("   ✅ Noticias clave con enlaces")
    print("   ✅ Gráficos históricos de cada activo")
    print("   ✅ Análisis detallado de oportunidades\n")
    
    try:
        generator = ComparativePDFGenerator()
        pdf_path = generator.generate_comparative_pdf(results, period, interval)
        
        print(f"\n{'='*70}")
        print(f"✅ PDF GENERADO EXITOSAMENTE")
        print(f"{'='*70}")
        print(f"📁 Ruta: {pdf_path}\n")
        
        print("🔍 Contenido incluido:")
        print(f"   🏆 Top {min(5, len(results))} mejores oportunidades")
        print("   📊 Gráficos históricos individuales")
        print("   📰 3 noticias clave por activo (con enlaces)")
        print("   ⏱️ Tiempo estimado de retorno")
        print("   📋 Análisis detallado y recomendaciones")
        print("   ⚠️ Advertencias de riesgos")
        
    except Exception as e:
        print(f"❌ Error generando PDF: {e}")
        import traceback
        traceback.print_exc()
else:
    print("❌ No hay resultados para generar el PDF")

print(f"\n{'='*70}")
print("TEST COMPLETADO")
print(f"{'='*70}\n")
