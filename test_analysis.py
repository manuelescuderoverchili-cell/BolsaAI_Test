"""
Script de prueba para verificar que todos los módulos funcionan correctamente
"""
import sys
import os

# Añadir el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    print("🔍 Importando módulos...")
    from market_analyzer import MarketAnalyzer
    from news_analyzer import NewsAnalyzer
    from pattern_analyzer import TechnicalPatternAnalyzer
    from predictive_analyzer import PredictiveAnalyzer
    from advanced_visualizer import AdvancedVisualizer
    from pdf_report_generator import PDFReportGenerator
    print("✅ Todos los módulos importados correctamente\n")
    
    print("🔍 Probando análisis con datos de prueba...")
    
    # Crear analizador de mercado
    analyzer = MarketAnalyzer("Bitcoin")
    print("✅ MarketAnalyzer creado")
    
    # Obtener datos (solo 7 días para la prueba)
    data = analyzer.get_data(period="7d", interval="1d")
    print(f"✅ Datos obtenidos: {len(data)} registros")
    
    # Calcular estadísticas
    stats = analyzer.calculate_statistics()
    print("✅ Estadísticas calculadas")
    
    # Detectar patrones
    pattern_analyzer = TechnicalPatternAnalyzer(data)
    patterns = pattern_analyzer.analyze_all_patterns()
    print(f"✅ Patrones detectados: {len(patterns.get('todos', []))}")
    
    # Generar predicciones
    predictive = PredictiveAnalyzer(data, patterns)
    prediction_report, predictions = predictive.generate_prediction_report()
    print(f"✅ Predicciones generadas: Dirección {predictions.get('direccion_probable', 'N/A')}")
    
    # Generar gráfico avanzado
    adv_viz = AdvancedVisualizer()
    graph_path = adv_viz.plot_patterns_marked(data, "Bitcoin", patterns, predictions)
    print(f"✅ Gráfico con patrones generado: {graph_path}")
    
    # Generar PDF (sin noticias para agilizar)
    pdf_gen = PDFReportGenerator()
    analysis_results = {
        'market_data': {'statistics': stats, 'trends': {}},
        'patrones': patterns,
        'predicciones': predictions,
        'noticias': []
    }
    pdf_path = pdf_gen.generate_complete_pdf_report("Bitcoin", analysis_results, [graph_path])
    print(f"✅ PDF generado: {pdf_path}")
    
    print("\n🎉 ¡Todas las pruebas completadas exitosamente!")
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
