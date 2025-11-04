"""
Script de prueba para verificar ajuste automático de periodos según intervalo
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from market_analyzer import MarketAnalyzer

def test_interval_limits():
    """Prueba las limitaciones de intervalos y ajustes automáticos"""
    
    print("\n" + "="*80)
    print("PRUEBA DE AJUSTE AUTOMÁTICO DE PERIODOS SEGÚN INTERVALO")
    print("="*80 + "\n")
    
    test_cases = [
        # (periodo, intervalo, descripción)
        ("1y", "1m", "1 año con intervalo 1 minuto - Debe ajustar a 7d"),
        ("3mo", "5m", "3 meses con intervalo 5 minutos - Debe ajustar a 7d"),
        ("6mo", "15m", "6 meses con intervalo 15 minutos - Debe ajustar a 60d"),
        ("1y", "1h", "1 año con intervalo 1 hora - OK, sin ajuste"),
        ("5y", "1h", "5 años con intervalo 1 hora - Debe ajustar a 730d"),
        ("1mo", "1d", "1 mes con intervalo 1 día - OK, sin ajuste"),
        ("5d", "1m", "5 días con intervalo 1 minuto - OK, sin ajuste"),
    ]
    
    for periodo, intervalo, descripcion in test_cases:
        print(f"\n{'='*80}")
        print(f"TEST: {descripcion}")
        print(f"Solicitado: periodo={periodo}, intervalo={intervalo}")
        print(f"{'='*80}")
        
        try:
            analyzer = MarketAnalyzer("Bitcoin")
            data = analyzer.get_data(period=periodo, interval=intervalo)
            
            print(f"✅ Datos obtenidos exitosamente")
            print(f"   📊 Cantidad de registros: {len(data)}")
            print(f"   📅 Primer registro: {data.index[0]}")
            print(f"   📅 Último registro: {data.index[-1]}")
            print(f"   🕐 Diferencia temporal: {data.index[-1] - data.index[0]}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n" + "="*80)
    print("RESUMEN DE LIMITACIONES DE YFINANCE:")
    print("="*80)
    print("""
    📌 Intervalos de 1m, 2m, 5m:
       • Máximo 7 días de datos
       • Ideal para análisis intraday de corto plazo
    
    📌 Intervalos de 15m, 30m:
       • Máximo 60 días de datos
       • Bueno para análisis de swing trading
    
    📌 Intervalos de 1h:
       • Máximo 730 días (2 años)
       • Excelente para análisis de medio plazo
    
    📌 Intervalos de 1d, 1wk, 1mo:
       • Sin restricción práctica importante
       • Perfecto para análisis de largo plazo
    
    💡 El sistema ajusta automáticamente el periodo cuando se exceden los límites
    """)
    
    print("="*80)
    print("✅ PRUEBA COMPLETADA")
    print("="*80 + "\n")

if __name__ == "__main__":
    test_interval_limits()
