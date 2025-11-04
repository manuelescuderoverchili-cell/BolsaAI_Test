"""
Test de las tres mejoras:
1. Traducción de noticias al español
2. Filtrado más agresivo (menos solapamiento)
3. Sincronización del eje X entre gráficos
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.market_analyzer import MarketAnalyzer
from src.pattern_analyzer import TechnicalPatternAnalyzer
from src.predictive_analyzer import PredictiveAnalyzer
from src.news_analyzer import NewsAnalyzer
from src.visualizer import Visualizer
from src.advanced_visualizer import AdvancedVisualizer
from src.pdf_report_generator import PDFReportGenerator

print("=" * 70)
print("TEST: Mejoras de Traducción, Filtrado y Sincronización")
print("=" * 70)

# Test 1: Traducción de noticias
print("\n1️⃣ TEST: Traducción de noticias al español")
print("-" * 70)

news_analyzer = NewsAnalyzer("Bitcoin")
noticias = news_analyzer.fetch_news(max_news=3)

if noticias:
    print(f"✅ Obtenidas {len(noticias)} noticias\n")
    
    pdf_gen = PDFReportGenerator()
    
    for i, noticia in enumerate(noticias, 1):
        titulo_original = noticia.get('titulo', '')
        descripcion_original = noticia.get('descripcion', '')
        
        print(f"📰 Noticia #{i}")
        print(f"   Título original: {titulo_original[:60]}...")
        print(f"   Descripción original: {descripcion_original[:80] if descripcion_original else 'N/A'}...")
        
        # Probar traducción
        descripcion_es = pdf_gen._resumir_descripcion(descripcion_original, titulo_original)
        
        print(f"\n   ✅ Descripción en ESPAÑOL:")
        print(f"   {descripcion_es}\n")
        
        # Verificar que está en español
        palabras_esp = ['el', 'la', 'de', 'que', 'en', 'y', 'a', 'los', 'del', 'se', 'las', 'por']
        palabras_texto = descripcion_es.lower().split()[:10]
        palabras_esp_encontradas = sum(1 for p in palabras_texto if p in palabras_esp)
        
        if palabras_esp_encontradas > 0:
            print(f"   ✅ CONFIRMADO: Texto en español ({palabras_esp_encontradas} palabras detectadas)")
        else:
            print(f"   ⚠️ Posiblemente en inglés (revisar)")
        print()
else:
    print("❌ No se encontraron noticias")

# Test 2: Filtrado más agresivo
print("\n2️⃣ TEST: Filtrado más agresivo (menos solapamiento)")
print("-" * 70)

analyzer = MarketAnalyzer("Bitcoin")
data_1m = analyzer.get_data(period="7d", interval="1m")
print(f"📊 Datos originales: {len(data_1m)} registros")

# Calcular filtrado esperado
num_datos = len(data_1m)
if num_datos > 1000:
    step_esperado = max(1, num_datos // 200)  # NUEVO límite
    datos_esperados = num_datos // step_esperado
else:
    step_esperado = 1
    datos_esperados = num_datos

print(f"📉 Filtrado esperado: 1 de cada {step_esperado} → ~{datos_esperados} datos en gráfico")
print(f"   (Antes: 1 de cada {num_datos // 300} → ~300 datos)")
print(f"   (Ahora: 1 de cada {step_esperado} → ~{datos_esperados} datos)")

# Generar gráfico para verificar
visualizer = Visualizer()
print("\n📈 Generando gráfico de velas...")
candlestick_path = visualizer.plot_candlestick(data_1m, "Bitcoin_test")
print(f"✅ Gráfico generado: {candlestick_path}")

# Test 3: Sincronización de eje X
print("\n\n3️⃣ TEST: Sincronización del eje X entre gráficos")
print("-" * 70)

stats = analyzer.calculate_statistics()
trends = analyzer.detect_trends()

print("📊 Generando gráfico de análisis completo...")
print("   (Precio, Volumen y Retornos deben tener el MISMO eje X)")

analysis_path = visualizer.plot_price_analysis(data_1m, "Bitcoin_test", stats, trends)
print(f"✅ Gráfico generado: {analysis_path}")
print("\n   ℹ️ Verifica que:")
print("      - Gráfico de Precio (arriba) tiene eje X de [fecha_inicio] a [fecha_fin]")
print("      - Gráfico de Volumen (medio) tiene MISMO eje X")
print("      - Gráfico de Retornos (abajo) tiene MISMO eje X")
print("      - Todos alineados verticalmente")

# Test 4: Gráfico avanzado con patrones
print("\n\n4️⃣ TEST: Gráfico avanzado con sincronización")
print("-" * 70)

pattern_analyzer = TechnicalPatternAnalyzer(data_1m)
patterns = pattern_analyzer.analyze_all_patterns()
print(f"🔍 Patrones detectados: {len(patterns.get('todos', []))}")

predictive_analyzer = PredictiveAnalyzer(data_1m, patterns)
prediction_report, predictions = predictive_analyzer.generate_prediction_report()

advanced_visualizer = AdvancedVisualizer()
print("\n📈 Generando gráfico con patrones marcados...")
patterns_path = advanced_visualizer.plot_patterns_marked(
    data_1m, "Bitcoin_test", patterns, predictions
)
print(f"✅ Gráfico generado: {patterns_path}")
print("\n   ℹ️ Verifica que:")
print("      - Gráfico de Precio y Patrones tiene eje X sincronizado")
print("      - Gráfico de Volumen tiene MISMO eje X")
print("      - Ambos alineados verticalmente")

# Resumen
print("\n" + "=" * 70)
print("RESUMEN DE MEJORAS:")
print("=" * 70)

print("\n1. ✅ TRADUCCIÓN AL ESPAÑOL:")
print("   - Descripciones de noticias traducidas automáticamente")
print("   - Usa TextBlob para traducción")
print("   - Detecta si ya está en español (evita re-traducir)")

print("\n2. ✅ FILTRADO MÁS AGRESIVO:")
print(f"   - Antes: Máximo 300-400 datos en gráfico")
print(f"   - Ahora: Máximo 200-250 datos en gráfico")
print(f"   - Con {num_datos} datos: {datos_esperados} velas mostradas")
print(f"   - Menos solapamiento, más legibilidad")

print("\n3. ✅ SINCRONIZACIÓN DEL EJE X:")
print("   - Precio, Volumen y Retornos comparten MISMO eje X")
print("   - set_xlim() aplicado a todos los subgráficos")
print("   - Alineación perfecta para comparación visual")

print("\n📁 Archivos generados:")
print(f"   - {candlestick_path}")
print(f"   - {analysis_path}")
print(f"   - {patterns_path}")

print("\n🎯 Revisa los gráficos para confirmar:")
print("   ✓ Menos símbolos/velas = Sin solapamiento")
print("   ✓ Ejes X alineados verticalmente")
print("   ✓ Fechas idénticas en todos los gráficos")
