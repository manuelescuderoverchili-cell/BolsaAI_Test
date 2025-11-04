"""
Comparación visual: Gráfica CON gaps vs SIN gaps
"""
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

print("Descargando Bitcoin 1m (7 días)...")
btc = yf.Ticker("BTC-USD")
data = btc.history(period="7d", interval="1m")

print(f"✅ {len(data)} datos obtenidos")

# Crear figura con 2 subgráficas
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 8))

# === GRÁFICA 1: CON GAPS (método antiguo - escala temporal) ===
ax1.plot(data.index, data['Close'], color='red', linewidth=0.8, alpha=0.7)
ax1.set_title('❌ MÉTODO ANTIGUO: Escala temporal (CON gaps visibles)', 
             fontsize=13, fontweight='bold', color='red')
ax1.set_xlabel('Tiempo real')
ax1.set_ylabel('Precio ($)')
ax1.grid(True, alpha=0.3)
ax1.tick_params(axis='x', rotation=45)

# Añadir anotación sobre gaps
time_diffs = data.index.to_series().diff()
gaps = time_diffs[time_diffs > pd.Timedelta(minutes=2)]
ax1.text(0.02, 0.98, f'⚠️ {len(gaps)} gaps visibles (espacios vacíos)', 
        transform=ax1.transAxes, fontsize=10, verticalalignment='top',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

# === GRÁFICA 2: SIN GAPS (método nuevo - índice numérico) ===
x_values = range(len(data))
ax2.plot(x_values, data['Close'].values, color='green', linewidth=0.8)
ax2.set_title('✅ MÉTODO NUEVO: Índice numérico (SIN gaps - continuo)', 
             fontsize=13, fontweight='bold', color='green')
ax2.set_xlabel('Índice de muestra (solo datos disponibles)')
ax2.set_ylabel('Precio ($)')
ax2.grid(True, alpha=0.3)

# Configurar etiquetas del eje X mostrando fechas reales
num_labels = 12
step = max(1, len(data) // num_labels)
tick_positions = list(range(0, len(data), step))
tick_labels = [data.index[i].strftime('%d/%m %H:%M') for i in tick_positions]
ax2.set_xticks(tick_positions)
ax2.set_xticklabels(tick_labels, rotation=45, ha='right')

# Añadir anotación
ax2.text(0.02, 0.98, f'✅ {len(data)} datos continuos sin espacios vacíos', 
        transform=ax2.transAxes, fontsize=10, verticalalignment='top',
        bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.5))

plt.tight_layout()

# Guardar
filename = f"comparacion_gaps_vs_nogaps_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
plt.savefig(filename, dpi=200, bbox_inches='tight', facecolor='white')
print(f"\n✅ Comparación guardada: {filename}")
plt.close()

print("\n" + "="*70)
print("EXPLICACIÓN:")
print("="*70)
print("❌ MÉTODO ANTIGUO (arriba):")
print("   - Usa escala temporal real")
print("   - Muestra gaps/espacios cuando no hay datos")
print("   - Menos legible para intervalos pequeños")
print("")
print("✅ MÉTODO NUEVO (abajo):")
print("   - Usa índice numérico (0, 1, 2, 3...)")
print("   - Gráfica continua sin espacios vacíos")
print("   - Eje X muestra fechas reales en posiciones específicas")
print("   - Mucho más legible y profesional")
print("")
print(f"📊 Total de datos: {len(data)}")
print(f"🔍 Gaps encontrados: {len(gaps)}")
print(f"⏱️ Periodo: {data.index[0]} a {data.index[-1]}")
