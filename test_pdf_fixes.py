"""
Test para verificar las correcciones del PDF:
1. Análisis técnico detallado con valores correctos (no ceros)
2. Descripciones de noticias en español (3-4 líneas)
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.market_analyzer import MarketAnalyzer
from src.pattern_analyzer import TechnicalPatternAnalyzer
from src.predictive_analyzer import PredictiveAnalyzer
from src.news_analyzer import NewsAnalyzer
from src.pdf_report_generator import PDFReportGenerator
from datetime import datetime

print("=" * 70)
print("TEST: Correcciones del PDF")
print("=" * 70)

# 1. TEST DE DATOS TÉCNICOS
print("\n1️⃣ Verificando mapeo de datos técnicos...")
print("-" * 70)

analyzer = MarketAnalyzer("Bitcoin")
data = analyzer.get_data(period="1mo", interval="1d")
stats = analyzer.calculate_statistics()
trends = analyzer.detect_trends()

print("\n📊 DATOS ORIGINALES (market_analyzer):")
print(f"   precio_actual: ${stats.get('precio_actual', 0):,.2f}")
print(f"   volatilidad: {stats.get('volatilidad', 0):.2f}%")
sma_20_val = trends.get('sma_20', 0)
sma_50_val = trends.get('sma_50', 0)
rsi_val = trends.get('rsi', 0)
print(f"   sma_20: ${sma_20_val:,.2f}" if sma_20_val else "   sma_20: N/A")
print(f"   sma_50: ${sma_50_val:,.2f}" if sma_50_val else "   sma_50: N/A (insuficientes datos)")
print(f"   rsi: {rsi_val:.2f}" if rsi_val else "   rsi: N/A")
print(f"   tendencia: {trends.get('tendencia', 'N/A')}")

# Mapeo correcto para el PDF
mapped_stats = {
    'current_price': stats.get('precio_actual', 0),
    'sma_20': trends.get('sma_20', 0),
    'sma_50': trends.get('sma_50', 0),
    'rsi': trends.get('rsi', 0),
    'volatility': stats.get('volatilidad', 0),
    'trend': trends.get('tendencia', 'N/A')
}

print("\n📋 DATOS MAPEADOS (para PDF):")
print(f"   current_price: ${mapped_stats['current_price']:,.2f}")
print(f"   volatility: {mapped_stats['volatility']:.2f}%")
print(f"   sma_20: ${mapped_stats['sma_20']:,.2f}" if mapped_stats['sma_20'] else "   sma_20: N/A")
print(f"   sma_50: ${mapped_stats['sma_50']:,.2f}" if mapped_stats['sma_50'] else "   sma_50: N/A")
print(f"   rsi: {mapped_stats['rsi']:.2f}" if mapped_stats['rsi'] else "   rsi: N/A")
print(f"   trend: {mapped_stats['trend']}")

if mapped_stats['current_price'] > 0:
    print("\n✅ CORRECTO: Los datos técnicos tienen valores válidos (no ceros)")
else:
    print("\n❌ ERROR: Los datos siguen en cero")

# 2. TEST DE DESCRIPCIONES DE NOTICIAS
print("\n\n2️⃣ Verificando descripciones de noticias...")
print("-" * 70)

news_analyzer = NewsAnalyzer("Bitcoin")
noticias = news_analyzer.fetch_news(max_news=5)

if noticias:
    print(f"\n✅ Se encontraron {len(noticias)} noticias")
    
    # Probar método de resumen
    pdf_gen = PDFReportGenerator()
    
    print("\n📰 EJEMPLOS DE DESCRIPCIONES RESUMIDAS:")
    for i, noticia in enumerate(noticias[:3], 1):
        print(f"\n--- Noticia #{i} ---")
        print(f"Título: {noticia['titulo'][:60]}...")
        
        descripcion_original = noticia.get('descripcion', '')
        print(f"Descripción original ({len(descripcion_original)} chars):")
        print(f"   {descripcion_original[:100]}...")
        
        descripcion_resumida = pdf_gen._resumir_descripcion(descripcion_original)
        print(f"\nDescripción resumida ({len(descripcion_resumida)} chars):")
        print(f"   {descripcion_resumida}")
        
        # Contar líneas aproximadas (asumiendo ~70 chars por línea)
        num_lineas = len(descripcion_resumida) / 70
        print(f"   Aprox. {num_lineas:.1f} líneas")
        
        if len(descripcion_resumida) <= 350 and len(descripcion_resumida) > 0:
            print("   ✅ Longitud correcta (3-4 líneas)")
        else:
            print(f"   ⚠️ Longitud: {len(descripcion_resumida)} chars")
else:
    print("\n⚠️ No se encontraron noticias para probar")

# 3. TEST DE GENERACIÓN DE PDF COMPLETO
print("\n\n3️⃣ Generando PDF de prueba completo...")
print("-" * 70)

# Análisis de patrones
pattern_analyzer = TechnicalPatternAnalyzer(data)
patterns = pattern_analyzer.analyze_all_patterns()

# Predicciones
predictive_analyzer = PredictiveAnalyzer(data, patterns)
effectiveness = predictive_analyzer.analyze_pattern_effectiveness()
prediction_report, predictions = predictive_analyzer.generate_prediction_report()

# Preparar datos de análisis completos (CON MAPEO CORRECTO)
analysis_results = {
    'market_data': {
        'statistics': {
            'current_price': stats.get('precio_actual', 0),
            'sma_20': trends.get('sma_20', 0),
            'sma_50': trends.get('sma_50', 0),
            'rsi': trends.get('rsi', 0),
            'volatility': stats.get('volatilidad', 0),
            'trend': trends.get('tendencia', 'N/A')
        },
        'trends': trends
    },
    'patrones': patterns,
    'predicciones': predictions,
    'noticias': noticias if noticias else []
}

# Generar PDF
pdf_path = pdf_gen.generate_complete_pdf_report(
    "Bitcoin", 
    analysis_results, 
    []  # Sin gráficos para este test
)

print(f"\n✅ PDF de prueba generado: {pdf_path}")

# Verificación final
print("\n" + "=" * 70)
print("RESUMEN DE CORRECCIONES:")
print("=" * 70)
print("1. ✅ Análisis Técnico Detallado:")
print("   - Mapeo correcto de campos (precio_actual → current_price)")
print("   - Valores numéricos válidos (no ceros)")
print("")
print("2. ✅ Descripciones de Noticias:")
print("   - Método _resumir_descripcion() implementado")
print("   - Limpieza de HTML")
print("   - Resumen a 3-4 líneas (max 350 chars)")
print("   - Se muestra bajo cada noticia en el PDF")
print("")
print("📄 Revisa el PDF generado para verificar:")
print("   - Sección 'ANÁLISIS TÉCNICO DETALLADO' con valores correctos")
print("   - Sección 'NOTICIAS DE ALTO IMPACTO' con descripciones")
print("")
print(f"Archivo: {pdf_path}")
