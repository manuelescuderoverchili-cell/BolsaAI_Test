"""
Test para visualizar datos de 1 minuto con gaps del mercado
"""
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

# Descargar datos de 1 minuto para 7 días
ticker = "BTC-USD"  # Bitcoin 24/7 - sin gaps
# ticker = "AAPL"   # Acciones - con gaps (solo horario mercado)

print(f"Descargando {ticker} con intervalo 1m y periodo 7d...")
stock = yf.Ticker(ticker)
data = stock.history(period="7d", interval="1m")

print(f"\n📊 Datos obtenidos: {len(data)} registros")
print(f"📅 Desde: {data.index[0]}")
print(f"📅 Hasta: {data.index[-1]}")

# Analizar gaps
data_sorted = data.sort_index()
time_diffs = data_sorted.index.to_series().diff()
gaps = time_diffs[time_diffs > pd.Timedelta(minutes=2)]

print(f"\n🔍 Gaps encontrados (> 2 minutos): {len(gaps)}")
if len(gaps) > 0:
    print("\nPrimeros 10 gaps:")
    for idx, gap in gaps.head(10).items():
        print(f"  {idx}: {gap} de silencio")

# Visualización
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

# Gráfica 1: Con gaps (escala temporal continua)
ax1.plot(data.index, data['Close'], linewidth=0.5, color='blue')
ax1.set_title(f'{ticker} - Precio con gaps (escala temporal continua)', fontweight='bold')
ax1.set_xlabel('Tiempo')
ax1.set_ylabel('Precio ($)')
ax1.grid(True, alpha=0.3)

# Gráfica 2: Sin gaps (índice numérico)
ax2.plot(range(len(data)), data['Close'].values, linewidth=0.5, color='green')
ax2.set_title(f'{ticker} - Precio sin gaps (solo datos disponibles)', fontweight='bold')
ax2.set_xlabel('Índice de muestra')
ax2.set_ylabel('Precio ($)')
ax2.grid(True, alpha=0.3)

plt.tight_layout()
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"gaps_test_{ticker.replace('-', '')}_{timestamp}.png"
plt.savefig(filename, dpi=150, bbox_inches='tight')
print(f"\n✅ Gráfica guardada: {filename}")
plt.close()

print("\n" + "="*70)
print("CONCLUSIÓN:")
print("="*70)
if len(gaps) > 0:
    print("❌ Este activo tiene gaps (mercado cerrado fuera de horario)")
    print("   - Los gaps son NORMALES para acciones/ETFs")
    print("   - Solo hay datos cuando el mercado está operando")
else:
    print("✅ Este activo NO tiene gaps (opera 24/7)")
    print("   - Típico de criptomonedas")
