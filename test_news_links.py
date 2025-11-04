"""
Script de prueba para verificar hipervínculos en PDF de análisis individual
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from market_analyzer import MarketAnalyzer
from news_analyzer import NewsAnalyzer
from visualizer import Visualizer
from pattern_analyzer import TechnicalPatternAnalyzer
from predictive_analyzer import PredictiveAnalyzer
from advanced_visualizer import AdvancedVisualizer
from pdf_report_generator import PDFReportGenerator

def test_pdf_with_news_links():
    """Prueba generación de PDF con hipervínculos a noticias"""
    
    print("\n" + "="*80)
    print("PRUEBA DE PDF CON HIPERVÍNCULOS A NOTICIAS")
    print("="*80 + "\n")
    
    asset_name = "Bitcoin"
    period = "1mo"
    interval = "1d"
    
    print(f"📊 Analizando {asset_name}...")
    
    # 1. Análisis de mercado
    print("   📈 Obteniendo datos de mercado...")
    market_analyzer = MarketAnalyzer(asset_name)
    data = market_analyzer.get_data(period=period, interval=interval)
    
    if len(data) < 5:
        print("❌ Datos insuficientes")
        return
    
    stats = market_analyzer.calculate_statistics()
    trends = market_analyzer.detect_trends()
    
    # 2. Análisis de noticias
    print("   📰 Buscando noticias...")
    news_analyzer = NewsAnalyzer(asset_name)
    news_analyzer.fetch_news(max_news=15)
    news_summary = news_analyzer.get_sentiment_summary()
    
    print(f"   ✅ Encontradas {news_summary['total']} noticias")
    
    # Verificar que las noticias tienen links
    noticias_con_link = [n for n in news_analyzer.noticias if n.get('link')]
    print(f"   🔗 {len(noticias_con_link)} noticias tienen enlaces")
    
    # 3. Análisis de patrones
    print("   🔍 Detectando patrones técnicos...")
    pattern_analyzer = TechnicalPatternAnalyzer(data)
    patterns = pattern_analyzer.analyze_all_patterns()
    
    # 4. Predicciones
    print("   🔮 Generando predicciones...")
    predictive_analyzer = PredictiveAnalyzer(data, patterns)
    prediction_report, predictions = predictive_analyzer.generate_prediction_report()
    
    # 5. Generar visualizaciones
    print("   📊 Generando gráficas...")
    adv_visualizer = AdvancedVisualizer()
    
    graph_paths = []
    # Gráfica con patrones marcados
    graph1 = adv_visualizer.plot_patterns_marked(data, asset_name, patterns, predictions)
    if graph1:
        graph_paths.append(graph1)
    
    # Gráfica de escenarios predictivos
    graph2 = adv_visualizer.plot_prediction_scenarios(data, asset_name, predictions)
    if graph2:
        graph_paths.append(graph2)
    
    # 6. Preparar datos para PDF
    analysis_results = {
        'asset_name': asset_name,
        'ticker': MarketAnalyzer.ASSETS[asset_name],
        'period': period,
        'interval': interval,
        'stats': stats,
        'trends': trends,
        'patterns': patterns,
        'predictions': predictions,
        'noticias': news_analyzer.noticias,
        'sentimiento_promedio': news_summary.get('sentimiento_promedio', 0),
        'prediction_report': prediction_report
    }
    
    # 7. Generar PDF
    print("\n   📄 Generando PDF con hipervínculos a noticias...")
    pdf_generator = PDFReportGenerator()
    pdf_path = pdf_generator.generate_complete_pdf_report(
        asset_name, 
        analysis_results, 
        graph_paths
    )
    
    print(f"\n✅ PDF generado exitosamente: {pdf_path}")
    print("\n🔍 El PDF debe contener:")
    print("   • Sección 'NOTICIAS DE ALTO IMPACTO' con top 5 noticias")
    print("   • Score de impacto para cada noticia")
    print("   • Hipervínculos clickeables (🔗 Leer noticia completa)")
    print("   • Clasificación por sentimiento (MUY POSITIVO, POSITIVO, NEUTRAL, NEGATIVO, MUY NEGATIVO)")
    print("   • Sección 'OTRAS NOTICIAS RECIENTES' con enlaces adicionales")
    
    print("\n" + "="*80)
    print("✅ PRUEBA COMPLETADA - Abre el PDF y verifica los hipervínculos")
    print("="*80 + "\n")

if __name__ == "__main__":
    test_pdf_with_news_links()
