"""
Script de prueba para verificar gráficas temporales en PDF comparativo
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from comparative_analyzer import ComparativeAnalyzer

def test_pdf_with_charts():
    """Prueba generación de PDF con gráficas temporales"""
    
    print("\n" + "="*80)
    print("PRUEBA DE PDF COMPARATIVO CON GRÁFICAS TEMPORALES")
    print("="*80 + "\n")
    
    # Crear analizador comparativo con solo 3 activos para prueba rápida
    comparative = ComparativeAnalyzer()
    
    print("🔍 Analizando solo 3 activos para prueba rápida...")
    print("   (Bitcoin, Apple, Tesla)\n")
    
    # Limitar activos para prueba rápida
    from market_analyzer import MarketAnalyzer
    original_assets = MarketAnalyzer.ASSETS.copy()
    MarketAnalyzer.ASSETS = {
        'Bitcoin': 'BTC-USD',
        'Apple': 'AAPL',
        'Tesla': 'TSLA'
    }
    
    try:
        # Ejecutar análisis
        def progress_callback(message, progress):
            print(f"[{progress*100:.0f}%] {message}")
        
        results = comparative.analyze_all_assets(
            period="1mo",
            interval="1d",
            progress_callback=progress_callback
        )
        
        print(f"\n✅ Análisis completado: {len(results)} activos")
        
        # Generar PDF con gráficas
        print("\n📄 Generando PDF con gráficas temporales...")
        pdf_path = comparative.generate_pdf_report(period="1mo", interval="1d")
        
        if pdf_path:
            print(f"\n✅ PDF generado exitosamente: {pdf_path}")
            print("\n🔍 El PDF debe contener:")
            print("   • Gráficas de evolución temporal para cada activo")
            print("   • Medias móviles SMA 20 y SMA 50")
            print("   • Análisis detallado de cada activo")
            
            print("\n" + "="*80)
            print("✅ PRUEBA COMPLETADA - Revisa el PDF generado")
            print("="*80 + "\n")
        else:
            print("\n⚠️ No se pudo generar el PDF")
    
    finally:
        # Restaurar activos originales
        MarketAnalyzer.ASSETS = original_assets

if __name__ == "__main__":
    test_pdf_with_charts()
