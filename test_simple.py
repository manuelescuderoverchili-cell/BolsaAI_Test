"""Test simple del PredictiveAnalyzer"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from predictive_analyzer import PredictiveAnalyzer
from market_analyzer import MarketAnalyzer
from pattern_analyzer import TechnicalPatternAnalyzer

print("Obteniendo datos...")
analyzer = MarketAnalyzer("Bitcoin")
data = analyzer.get_data(period="7d", interval="1d")
print(f"Datos: {len(data)} registros")

print("Detectando patrones...")
pattern_analyzer = TechnicalPatternAnalyzer(data)
patterns = pattern_analyzer.analyze_all_patterns()
print(f"Patrones: {len(patterns.get('todos', []))}")

print("Generando predicciones...")
predictive = PredictiveAnalyzer(data, patterns)
prediction_report, predictions = predictive.generate_prediction_report()

print("\n" + "="*60)
print(prediction_report)
print("="*60)
print(f"\n✅ Dirección: {predictions['direccion_probable']}")
print(f"✅ Confianza: {predictions['confianza']:.1f}%")
print(f"✅ Precio objetivo: ${predictions['rango_precio_estimado']['objetivo']:.2f}")
