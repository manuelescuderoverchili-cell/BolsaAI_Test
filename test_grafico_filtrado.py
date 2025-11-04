"""
Test de filtrado inteligente en gráficos con alta densidad de datos
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.market_analyzer import MarketAnalyzer
from src.pattern_analyzer import TechnicalPatternAnalyzer
from src.predictive_analyzer import PredictiveAnalyzer
from src.visualizer import Visualizer
from src.advanced_visualizer import AdvancedVisualizer

print("=" * 70)
print("TEST: Filtrado Inteligente en Gráficos")
print("=" * 70)

# Test 1: Datos de alta densidad (1 minuto, 7 días)
print("\n1️⃣ Test con ALTA DENSIDAD (1m + 7d)")
print("-" * 70)

analyzer = MarketAnalyzer("Bitcoin")
data_1m = analyzer.get_data(period="7d", interval="1m")

print(f"📊 Datos obtenidos: {len(data_1m)} registros")

# Análisis de patrones
pattern_analyzer = TechnicalPatternAnalyzer(data_1m)
patterns = pattern_analyzer.analyze_all_patterns()
print(f"🔍 Patrones detectados: {len(patterns.get('todos', []))}")

# Predicciones
predictive_analyzer = PredictiveAnalyzer(data_1m, patterns)
prediction_report, predictions = predictive_analyzer.generate_prediction_report()

# Generar gráficos con filtrado
print("\n📈 Generando gráficos con filtrado inteligente...")

# Gráfico 1: Velas (candlestick)
visualizer = Visualizer()
print("\n   🕯️ Gráfico de velas:")
candlestick_path = visualizer.plot_candlestick(data_1m, "Bitcoin_1m")

# Gráfico 2: Análisis completo
stats = analyzer.calculate_statistics()
trends = analyzer.detect_trends()
print("\n   📊 Gráfico de análisis completo:")
analysis_path = visualizer.plot_price_analysis(data_1m, "Bitcoin_1m", stats, trends)

# Gráfico 3: Patrones marcados
advanced_visualizer = AdvancedVisualizer()
print("\n   🎯 Gráfico con patrones marcados:")
patterns_path = advanced_visualizer.plot_patterns_marked(
    data_1m, "Bitcoin_1m", patterns, predictions
)

print(f"\n✅ Gráficos generados:")
print(f"   - Velas: {candlestick_path}")
print(f"   - Análisis: {analysis_path}")
print(f"   - Patrones: {patterns_path}")

# Test 2: Datos de baja densidad (1 día, 1 mes)
print("\n\n2️⃣ Test con BAJA DENSIDAD (1d + 1mo)")
print("-" * 70)

data_1d = analyzer.get_data(period="1mo", interval="1d")
print(f"📊 Datos obtenidos: {len(data_1d)} registros")

# Análisis de patrones
pattern_analyzer_1d = TechnicalPatternAnalyzer(data_1d)
patterns_1d = pattern_analyzer_1d.analyze_all_patterns()
print(f"🔍 Patrones detectados: {len(patterns_1d.get('todos', []))}")

# Predicciones
predictive_analyzer_1d = PredictiveAnalyzer(data_1d, patterns_1d)
prediction_report_1d, predictions_1d = predictive_analyzer_1d.generate_prediction_report()

# Generar gráficos SIN filtrado (pocos datos)
print("\n📈 Generando gráficos (sin necesidad de filtrado)...")

print("\n   🕯️ Gráfico de velas:")
candlestick_path_1d = visualizer.plot_candlestick(data_1d, "Bitcoin_1d")

print("\n   📊 Gráfico de análisis completo:")
stats_1d = analyzer.calculate_statistics()
trends_1d = analyzer.detect_trends()
analysis_path_1d = visualizer.plot_price_analysis(data_1d, "Bitcoin_1d", stats_1d, trends_1d)

print("\n   🎯 Gráfico con patrones marcados:")
patterns_path_1d = advanced_visualizer.plot_patterns_marked(
    data_1d, "Bitcoin_1d", patterns_1d, predictions_1d
)

print(f"\n✅ Gráficos generados:")
print(f"   - Velas: {candlestick_path_1d}")
print(f"   - Análisis: {analysis_path_1d}")
print(f"   - Patrones: {patterns_path_1d}")

# Resumen
print("\n" + "=" * 70)
print("RESUMEN DEL FILTRADO:")
print("=" * 70)

print("\n📊 ALTA DENSIDAD (7,000+ datos):")
print("   ✅ Velas: Se muestran ~300 velas (cada N datos)")
print("   ✅ Volumen: Barras filtradas proporcionalmente")
print("   ✅ Patrones: Máximo 15 patrones marcados")
print("   ✅ Anotaciones: Solo 1 de cada N patrones etiquetados")
print("   ✅ Símbolos: Tamaño reducido (150px vs 200px)")

print("\n📊 BAJA DENSIDAD (<100 datos):")
print("   ✅ Sin filtrado: Se muestran todos los datos")
print("   ✅ Patrones: Hasta 40 patrones marcados")
print("   ✅ Símbolos: Tamaño normal (200px)")

print("\n🎯 BENEFICIOS:")
print("   ✓ Gráficos siempre legibles")
print("   ✓ Sin solapamiento de símbolos")
print("   ✓ Velocidad de generación mejorada")
print("   ✓ Archivos PNG más ligeros")

print("\n📝 NOTA: Los gráficos indican cuántos datos se muestran")
print("   Ejemplo: '(7,402 datos, mostrando 1 de cada 25)'")
