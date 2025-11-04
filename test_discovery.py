"""
Script de prueba para el descubrimiento de activos
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from asset_discovery import AssetDiscovery
from market_analyzer import MarketAnalyzer

def test_discovery():
    """Prueba el descubrimiento de activos"""
    
    print("\n" + "="*80)
    print("PRUEBA DE DESCUBRIMIENTO DE ACTIVOS")
    print("="*80 + "\n")
    
    # Crear descubridor
    discovery = AssetDiscovery()
    
    # Ejecutar búsqueda (solo top 10 para prueba rápida)
    print("🔍 Buscando activos prometedores (score >= 60)...")
    
    # Limitar a unos pocos para prueba rápida
    discovery.CANDIDATE_TICKERS = {
        'Solana': 'SOL-USD',
        'Palantir': 'PLTR',
        'AMD': 'AMD',
        'Shopify': 'SHOP',
        'Coinbase': 'COIN',
    }
    
    promising_assets = discovery.discover_promising_assets(min_score=50)
    
    # Generar reporte
    report = discovery.generate_discovery_report()
    print(report)
    
    # Guardar
    discovery.save_discovered_assets()
    
    if promising_assets:
        print(f"\n✅ Se encontraron {len(promising_assets)} activos prometedores")
        
        # Probar añadir al sistema
        print("\n" + "="*80)
        print("PRUEBA DE AÑADIR ACTIVOS AL SISTEMA")
        print("="*80 + "\n")
        
        print(f"Activos actuales en el sistema: {len(MarketAnalyzer.ASSETS)}")
        
        new_assets = discovery.get_assets_for_addition()
        added = MarketAnalyzer.add_new_assets(new_assets)
        
        print(f"\n✅ Se añadieron {added} nuevos activos")
        print(f"Total de activos ahora: {len(MarketAnalyzer.ASSETS)}")
        
        # Guardar configuración
        MarketAnalyzer.save_assets_to_file()
        
        print("\n" + "="*80)
        print("✅ PRUEBA COMPLETADA EXITOSAMENTE")
        print("="*80 + "\n")
    else:
        print("\n⚠️ No se encontraron activos con score >= 50")

if __name__ == "__main__":
    test_discovery()
