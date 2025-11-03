import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.dates as mdates

def analizar_bitcoin():
    """
    Analiza la variación del Bitcoin en el día actual y genera un gráfico
    """
    
    # Obtener el símbolo de Bitcoin
    bitcoin = yf.Ticker("BTC-USD")
    
    # Obtener datos de hoy (últimas 24 horas con intervalos de 5 minutos)
    try:
        # Datos intradiarios de hoy
        data_hoy = bitcoin.history(period="1d", interval="5m")
        
        if data_hoy.empty:
            print("No se pudieron obtener datos de Bitcoin para hoy")
            return
        
        # Información básica
        precio_actual = data_hoy['Close'].iloc[-1]
        precio_apertura = data_hoy['Open'].iloc[0]
        precio_maximo = data_hoy['High'].max()
        precio_minimo = data_hoy['Low'].min()
        volumen_total = data_hoy['Volume'].sum()
        
        # Calcular variaciones
        variacion_absoluta = precio_actual - precio_apertura
        variacion_porcentual = (variacion_absoluta / precio_apertura) * 100
        
        # Mostrar información
        print("=" * 50)
        print("ANÁLISIS DE BITCOIN - " + datetime.now().strftime("%d/%m/%Y"))
        print("=" * 50)
        print(f"Precio actual: ${precio_actual:,.2f}")
        print(f"Precio de apertura: ${precio_apertura:,.2f}")
        print(f"Precio máximo del día: ${precio_maximo:,.2f}")
        print(f"Precio mínimo del día: ${precio_minimo:,.2f}")
        print(f"Variación absoluta: ${variacion_absoluta:,.2f}")
        print(f"Variación porcentual: {variacion_porcentual:.2f}%")
        print(f"Volumen total: {volumen_total:,.0f}")
        
        # Crear el gráfico
        crear_grafico(data_hoy, precio_apertura, precio_actual, variacion_porcentual)
        
    except Exception as e:
        print(f"Error al obtener datos: {e}")

def crear_grafico(data, precio_apertura, precio_actual, variacion_porcentual):
    """
    Crea un gráfico completo de la variación del Bitcoin
    """
    
    # Configurar el estilo del gráfico
    plt.style.use('seaborn-v0_8')
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
    
    # Gráfico 1: Precio a lo largo del día
    ax1.plot(data.index, data['Close'], linewidth=2, color='orange', label='Precio BTC')
    ax1.fill_between(data.index, data['Close'], alpha=0.3, color='orange')
    
    # Líneas de referencia
    ax1.axhline(y=precio_apertura, color='blue', linestyle='--', alpha=0.7, label=f'Apertura: ${precio_apertura:,.0f}')
    ax1.axhline(y=data['High'].max(), color='green', linestyle='--', alpha=0.7, label=f'Máximo: ${data["High"].max():,.0f}')
    ax1.axhline(y=data['Low'].min(), color='red', linestyle='--', alpha=0.7, label=f'Mínimo: ${data["Low"].min():,.0f}')
    
    # Escalar el eje Y para mostrar mejor las variaciones
    precio_min = data['Low'].min()
    precio_max = data['High'].max()
    rango = precio_max - precio_min
    margen = rango * 0.1  # 10% de margen arriba y abajo
    
    ax1.set_ylim(precio_min - margen, precio_max + margen)
    
    # Formatear el eje Y para mostrar más precisión
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
    
    ax1.set_title(f'Bitcoin (BTC-USD) - Variación del día {datetime.now().strftime("%d/%m/%Y")}\n'
                  f'Variación: {variacion_porcentual:+.2f}% | Rango: ${rango:,.0f}', fontsize=16, fontweight='bold')
    ax1.set_ylabel('Precio (USD)', fontsize=12)
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Formatear el eje x para mostrar horas
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax1.xaxis.set_major_locator(mdates.HourLocator(interval=2))
    plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45)
    
    # Gráfico 2: Volumen de transacciones
    ax2.bar(data.index, data['Volume'], width=0.003, alpha=0.6, color='purple')
    ax2.set_title('Volumen de Transacciones', fontsize=14, fontweight='bold')
    ax2.set_ylabel('Volumen', fontsize=12)
    ax2.set_xlabel('Hora del día', fontsize=12)
    ax2.grid(True, alpha=0.3)
    
    # Formatear el eje Y del volumen para mejor legibilidad
    ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1e9:.1f}B' if x >= 1e9 else f'{x/1e6:.0f}M'))
    
    # Formatear el eje x para el gráfico de volumen
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax2.xaxis.set_major_locator(mdates.HourLocator(interval=2))
    plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45)
    
    # Ajustar diseño
    plt.tight_layout()
    
    # Guardar el gráfico
    nombre_archivo = f"bitcoin_analisis_{datetime.now().strftime('%Y%m%d')}.png"
    plt.savefig(nombre_archivo, dpi=300, bbox_inches='tight')
    print(f"\n📊 Gráfico guardado como: {nombre_archivo}")
    
    # Mostrar el gráfico
    plt.show()

def obtener_datos_historicos():
    """
    Obtiene datos históricos de Bitcoin para comparación
    """
    bitcoin = yf.Ticker("BTC-USD")
    
    # Datos de la última semana
    data_semana = bitcoin.history(period="7d")
    
    if not data_semana.empty:
        print("\n" + "=" * 50)
        print("DATOS HISTÓRICOS (ÚLTIMA SEMANA)")
        print("=" * 50)
        
        # Comparar con días anteriores
        precio_hace_7_dias = data_semana['Close'].iloc[0]
        precio_actual = data_semana['Close'].iloc[-1]
        variacion_semanal = ((precio_actual - precio_hace_7_dias) / precio_hace_7_dias) * 100
        
        print(f"Precio hace 7 días: ${precio_hace_7_dias:,.2f}")
        print(f"Variación semanal: {variacion_semanal:+.2f}%")

if __name__ == "__main__":
    print("🚀 Iniciando análisis de Bitcoin...")
    print("📈 Obteniendo datos en tiempo real...")
    
    # Ejecutar análisis principal
    analizar_bitcoin()
    
    # Mostrar datos históricos para contexto
    obtener_datos_historicos()
    
    print("\n✅ Análisis completado!")