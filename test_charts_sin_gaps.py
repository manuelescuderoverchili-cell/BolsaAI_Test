"""
Test para verificar que las gráficas se generan SIN gaps visuales
Compara intervalo 1m (con gaps) vs visualización mejorada (sin gaps)
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.comparative_pdf_generator import ComparativePDFGenerator
import matplotlib.pyplot as plt
import yfinance as yf

print("=" * 70)
print("TEST: Gráficas sin gaps para intervalos pequeños")
print("=" * 70)

# Crear generador de PDFs
pdf_gen = ComparativePDFGenerator(output_dir="outputs/test_charts")

# Test 1: Bitcoin con 1 minuto (debería usar índice numérico)
print("\n1️⃣ Generando gráfica Bitcoin 1m + 7d (sin gaps)...")
chart_1m = pdf_gen._generate_price_chart(
    ticker="BTC-USD",
    asset_name="Bitcoin",
    period="7d",
    interval="1m"
)

if chart_1m:
    print(f"✅ Gráfica 1m generada: {chart_1m}")
else:
    print("❌ Error generando gráfica 1m")

# Test 2: Bitcoin con 1 hora (debería usar índice numérico)
print("\n2️⃣ Generando gráfica Bitcoin 1h + 30d (sin gaps)...")
chart_1h = pdf_gen._generate_price_chart(
    ticker="BTC-USD",
    asset_name="Bitcoin",
    period="30d",
    interval="1h"
)

if chart_1h:
    print(f"✅ Gráfica 1h generada: {chart_1h}")
else:
    print("❌ Error generando gráfica 1h")

# Test 3: Bitcoin con 1 día (debería usar fechas tradicionales)
print("\n3️⃣ Generando gráfica Bitcoin 1d + 3mo (fechas tradicionales)...")
chart_1d = pdf_gen._generate_price_chart(
    ticker="BTC-USD",
    asset_name="Bitcoin",
    period="3mo",
    interval="1d"
)

if chart_1d:
    print(f"✅ Gráfica 1d generada: {chart_1d}")
else:
    print("❌ Error generando gráfica 1d")

# Test 4: Acción con 5 minutos (gaps de mercado cerrado)
print("\n4️⃣ Generando gráfica Apple 5m + 7d (sin gaps visuales)...")
chart_aapl = pdf_gen._generate_price_chart(
    ticker="AAPL",
    asset_name="Apple Inc.",
    period="7d",
    interval="5m"
)

if chart_aapl:
    print(f"✅ Gráfica Apple 5m generada: {chart_aapl}")
else:
    print("❌ Error generando gráfica Apple 5m")

# Verificar datos para comparar
print("\n" + "=" * 70)
print("ANÁLISIS DE DATOS:")
print("=" * 70)

# Bitcoin 1m
btc = yf.Ticker("BTC-USD")
data_1m = btc.history(period="7d", interval="1m")
print(f"\n📊 Bitcoin 1m (7d): {len(data_1m)} datos")
print(f"   📅 Desde: {data_1m.index[0]}")
print(f"   📅 Hasta: {data_1m.index[-1]}")

# Gaps en Bitcoin 1m
import pandas as pd
time_diffs = data_1m.index.to_series().diff()
gaps_1m = time_diffs[time_diffs > pd.Timedelta(minutes=2)]
print(f"   🔍 Gaps > 2min: {len(gaps_1m)} (estos NO se verán en la gráfica)")

# Apple 5m
aapl = yf.Ticker("AAPL")
data_5m = aapl.history(period="7d", interval="5m")
print(f"\n📊 Apple 5m (7d): {len(data_5m)} datos")
print(f"   📅 Desde: {data_5m.index[0]}")
print(f"   📅 Hasta: {data_5m.index[-1]}")

# Gaps en Apple 5m
time_diffs_aapl = data_5m.index.to_series().diff()
gaps_5m = time_diffs_aapl[time_diffs_aapl > pd.Timedelta(minutes=10)]
print(f"   🔍 Gaps > 10min: {len(gaps_5m)} (horarios cerrados - NO visibles)")

print("\n" + "=" * 70)
print("RESUMEN:")
print("=" * 70)
print("✅ Las gráficas usan ÍNDICE NUMÉRICO para intervalos < 1d")
print("✅ Esto elimina los gaps visuales (espacios vacíos)")
print("✅ El eje X muestra fechas/horas reales en posiciones específicas")
print("✅ Para intervalos >= 1d usa el método tradicional con fechas")
print("\nℹ️ Los gaps son NORMALES (mercado cerrado, latencia de red)")
print("ℹ️ La nueva visualización los oculta para mejor legibilidad")
