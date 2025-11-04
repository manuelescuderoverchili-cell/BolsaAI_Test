"""
Módulo de visualización de datos financieros
"""
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import pandas as pd
import numpy as np
from datetime import datetime
import os
from typing import Optional, List, Dict

# Configuración de estilo
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")


class Visualizer:
    """Clase para generar y guardar visualizaciones"""
    
    def __init__(self, output_dir: str = "outputs/graphs"):
        """
        Inicializa el visualizador
        
        Args:
            output_dir: Directorio donde guardar los gráficos
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        # Configurar matplotlib para mejor apariencia
        plt.rcParams['figure.figsize'] = (14, 8)
        plt.rcParams['font.size'] = 10
        plt.rcParams['axes.grid'] = True
        plt.rcParams['grid.alpha'] = 0.3
    
    def plot_price_analysis(self, data: pd.DataFrame, asset_name: str, 
                           stats: Dict, trends: Dict) -> str:
        """
        Crea un gráfico completo de análisis de precio (con filtrado inteligente)
        
        Args:
            data: DataFrame con los datos del activo
            asset_name: Nombre del activo
            stats: Diccionario con estadísticas
            trends: Diccionario con tendencias
            
        Returns:
            Ruta del archivo guardado
        """
        fig, axes = plt.subplots(3, 1, figsize=(16, 12))
        fig.suptitle(f'Análisis Completo: {asset_name}', fontsize=18, fontweight='bold')
        
        # FILTRADO INTELIGENTE
        num_datos = len(data)
        
        # INCREMENTADO: Filtrado más agresivo
        if num_datos > 1000:
            step = max(1, num_datos // 250)  # Máximo 250 puntos (antes 400)
        elif num_datos > 500:
            step = max(1, num_datos // 300)  # Máximo 300 puntos
        else:
            step = 1
        
        if step > 1:
            data_filtered = data.iloc[::step].copy()
            print(f"   ℹ️ Gráfico de análisis: {num_datos} → {len(data_filtered)} datos (cada {step})")
        else:
            data_filtered = data.copy()
        
        # Gráfico 1: Precio y Medias Móviles
        ax1 = axes[0]
        ax1.plot(data_filtered.index, data_filtered['Close'], label='Precio', linewidth=2, color='#2E86AB')
        
        if 'SMA_20' in data_filtered.columns and not data_filtered['SMA_20'].isna().all():
            ax1.plot(data_filtered.index, data_filtered['SMA_20'], label='SMA 20', 
                    linewidth=1.5, linestyle='--', color='#A23B72', alpha=0.8)
        
        if 'SMA_50' in data_filtered.columns and not data_filtered['SMA_50'].isna().all():
            ax1.plot(data_filtered.index, data_filtered['SMA_50'], label='SMA 50', 
                    linewidth=1.5, linestyle='--', color='#F18F01', alpha=0.8)
        
        # Añadir líneas de soporte y resistencia
        if trends.get('soporte'):
            ax1.axhline(y=trends['soporte'], color='green', 
                       linestyle=':', linewidth=2, alpha=0.6, label='Soporte')
        if trends.get('resistencia'):
            ax1.axhline(y=trends['resistencia'], color='red', 
                       linestyle=':', linewidth=2, alpha=0.6, label='Resistencia')
        
        info_text = f'({num_datos} datos' + (f', mostrando 1 de cada {step})' if step > 1 else ')')
        ax1.set_title(f'Evolución del Precio con Medias Móviles {info_text}', fontsize=14, fontweight='bold')
        ax1.set_ylabel('Precio (USD)', fontsize=12)
        ax1.legend(loc='best', fontsize=10)
        ax1.grid(True, alpha=0.3)
        
        # SINCRONIZAR EJE X: Guardar límites para aplicar a todos los gráficos
        x_min = data_filtered.index.min()
        x_max = data_filtered.index.max()
        
        # Formato de fechas
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y'))
        ax1.set_xlim(x_min, x_max)  # Aplicar límites
        plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        # Gráfico 2: Volumen (con datos filtrados y EJE X SINCRONIZADO)
        ax2 = axes[1]
        colors = ['green' if data_filtered['Close'].iloc[i] >= data_filtered['Open'].iloc[i] 
                 else 'red' for i in range(len(data_filtered))]
        bar_width = step * 0.8 if step > 1 else 0.8
        ax2.bar(data_filtered.index, data_filtered['Volume'], color=colors, alpha=0.6, width=bar_width)
        ax2.set_title('Volumen de Transacciones', fontsize=14, fontweight='bold')
        ax2.set_ylabel('Volumen', fontsize=12)
        ax2.grid(True, alpha=0.3)
        
        # Formato de fechas con MISMO EJE X
        ax2.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y'))
        ax2.set_xlim(x_min, x_max)  # SINCRONIZADO con ax1
        plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        # Gráfico 3: Retornos Diarios (con datos filtrados y EJE X SINCRONIZADO)
        ax3 = axes[2]
        returns = data_filtered['Close'].pct_change() * 100
        colors_returns = ['green' if r > 0 else 'red' for r in returns]
        ax3.bar(data_filtered.index, returns, color=colors_returns, alpha=0.6, width=bar_width)
        ax3.axhline(y=0, color='black', linestyle='-', linewidth=0.8)
        ax3.set_title('Retornos Diarios (%)', fontsize=14, fontweight='bold')
        ax3.set_ylabel('Retorno (%)', fontsize=12)
        ax3.set_xlabel('Fecha', fontsize=12)
        ax3.grid(True, alpha=0.3)
        
        # Formato de fechas con MISMO EJE X
        ax3.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y'))
        ax3.set_xlim(x_min, x_max)  # SINCRONIZADO con ax1 y ax2
        plt.setp(ax3.xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        # Añadir cuadro de texto con estadísticas
        textstr = f"""Estadísticas del Periodo:
Precio Actual: ${stats['precio_actual']:,.2f}
Variación: {stats['variacion_porcentual']:+.2f}%
Volatilidad: {stats['volatilidad']:.2f}%
RSI: {trends.get('rsi', 0):.1f}
Tendencia: {trends['tendencia'].upper()}"""
        
        props = dict(boxstyle='round', facecolor='wheat', alpha=0.8)
        ax1.text(0.02, 0.98, textstr, transform=ax1.transAxes, fontsize=10,
                verticalalignment='top', bbox=props)
        
        plt.tight_layout()
        
        # Guardar gráfico
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{asset_name.replace(' ', '_')}_analisis_{timestamp}.png"
        filepath = os.path.join(self.output_dir, filename)
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✅ Gráfico guardado: {filepath}")
        return filepath
    
    def plot_sentiment_analysis(self, noticias: List[Dict], asset_name: str, 
                                sentiment_summary: Dict) -> str:
        """
        Crea un gráfico de análisis de sentimiento de noticias
        
        Args:
            noticias: Lista de diccionarios con noticias
            asset_name: Nombre del activo
            sentiment_summary: Resumen de sentimientos
            
        Returns:
            Ruta del archivo guardado
        """
        if not noticias:
            print("⚠️ No hay noticias para visualizar")
            return ""
        
        fig, axes = plt.subplots(2, 2, figsize=(16, 10))
        fig.suptitle(f'Análisis de Sentimiento de Noticias: {asset_name}', 
                    fontsize=18, fontweight='bold')
        
        # Preparar datos
        df_news = pd.DataFrame(noticias)
        df_news['fecha'] = pd.to_datetime(df_news['fecha'])
        df_news = df_news.sort_values('fecha')
        
        # Gráfico 1: Distribución de sentimientos (pie chart)
        ax1 = axes[0, 0]
        labels = ['Positivas', 'Negativas', 'Neutrales']
        sizes = [sentiment_summary['positivas'], 
                sentiment_summary['negativas'], 
                sentiment_summary['neutrales']]
        colors = ['#28a745', '#dc3545', '#6c757d']
        explode = (0.1, 0.1, 0)
        
        ax1.pie(sizes, explode=explode, labels=labels, colors=colors,
               autopct='%1.1f%%', shadow=True, startangle=90)
        ax1.set_title('Distribución de Sentimientos', fontsize=12, fontweight='bold')
        
        # Gráfico 2: Evolución temporal del sentimiento
        ax2 = axes[0, 1]
        ax2.scatter(df_news['fecha'], df_news['sentimiento'], 
                   c=df_news['sentimiento'], cmap='RdYlGn', 
                   s=100, alpha=0.6, edgecolors='black', linewidth=0.5)
        ax2.axhline(y=0, color='black', linestyle='--', linewidth=1, alpha=0.5)
        ax2.set_title('Evolución del Sentimiento en el Tiempo', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Polaridad del Sentimiento', fontsize=10)
        ax2.set_xlabel('Fecha', fontsize=10)
        ax2.grid(True, alpha=0.3)
        ax2.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m'))
        plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        # Gráfico 3: Histograma de polaridad
        ax3 = axes[1, 0]
        ax3.hist(df_news['sentimiento'], bins=20, color='steelblue', 
                edgecolor='black', alpha=0.7)
        ax3.axvline(x=sentiment_summary['sentimiento_promedio'], 
                   color='red', linestyle='--', linewidth=2, 
                   label=f'Media: {sentiment_summary["sentimiento_promedio"]:.3f}')
        ax3.set_title('Distribución de Polaridad', fontsize=12, fontweight='bold')
        ax3.set_xlabel('Polaridad', fontsize=10)
        ax3.set_ylabel('Frecuencia', fontsize=10)
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        # Gráfico 4: Top fuentes de noticias
        ax4 = axes[1, 1]
        fuentes_count = df_news['fuente'].value_counts()
        fuentes_count.plot(kind='barh', ax=ax4, color='coral', edgecolor='black')
        ax4.set_title('Noticias por Fuente', fontsize=12, fontweight='bold')
        ax4.set_xlabel('Cantidad de Noticias', fontsize=10)
        ax4.set_ylabel('Fuente', fontsize=10)
        ax4.grid(True, alpha=0.3, axis='x')
        
        plt.tight_layout()
        
        # Guardar gráfico
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{asset_name.replace(' ', '_')}_sentimiento_{timestamp}.png"
        filepath = os.path.join(self.output_dir, filename)
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✅ Gráfico de sentimiento guardado: {filepath}")
        return filepath
    
    def plot_candlestick(self, data: pd.DataFrame, asset_name: str) -> str:
        """
        Crea un gráfico de velas (candlestick) con filtrado inteligente
        
        Args:
            data: DataFrame con los datos OHLC
            asset_name: Nombre del activo
            
        Returns:
            Ruta del archivo guardado
        """
        fig, ax = plt.subplots(figsize=(16, 8))
        
        # FILTRADO INTELIGENTE: Reducir datos si hay demasiados
        num_datos = len(data)
        
        # Calcular factor de submuestreo para mantener gráfico legible
        # INCREMENTADO: Más agresivo para evitar solapamiento
        if num_datos > 1000:
            step = max(1, num_datos // 200)  # Máximo 200 velas (antes 300)
        elif num_datos > 500:
            step = max(1, num_datos // 250)  # Máximo 250 velas
        else:
            step = 1
        
        if step > 1:
            data_filtered = data.iloc[::step].copy()
            print(f"   ℹ️ Filtrado aplicado: {num_datos} → {len(data_filtered)} velas (cada {step} datos)")
        else:
            data_filtered = data.copy()
        
        # Crear velas con datos filtrados
        for i in range(len(data_filtered)):
            date = data_filtered.index[i]
            open_price = data_filtered['Open'].iloc[i]
            close_price = data_filtered['Close'].iloc[i]
            high_price = data_filtered['High'].iloc[i]
            low_price = data_filtered['Low'].iloc[i]
            
            color = 'green' if close_price >= open_price else 'red'
            
            # Ajustar ancho de vela según densidad
            width = 0.6 * step if step > 1 else 0.6
            
            # Dibujar la línea vertical (high-low)
            ax.plot([date, date], [low_price, high_price], 
                   color=color, linewidth=1 if step > 1 else 1, solid_capstyle='round')
            
            # Dibujar el rectángulo (open-close)
            height = abs(close_price - open_price)
            bottom = min(open_price, close_price)
            
            ax.add_patch(plt.Rectangle((mdates.date2num(date) - width/2, bottom), 
                                       width, height, facecolor=color, 
                                       edgecolor=color, alpha=0.8))
        
        # Información sobre filtrado
        info_text = f'{num_datos} datos totales'
        if step > 1:
            info_text += f' (mostrando 1 de cada {step})'
        
        ax.set_title(f'Gráfico de Velas: {asset_name}\n{info_text}', 
                    fontsize=16, fontweight='bold')
        ax.set_ylabel('Precio (USD)', fontsize=12)
        ax.set_xlabel('Fecha', fontsize=12)
        ax.grid(True, alpha=0.3)
        
        # Ajustar formato de fechas según densidad
        if num_datos > 200:
            ax.xaxis.set_major_locator(mdates.AutoDateLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y'))
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        plt.tight_layout()
        
        # Guardar gráfico
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{asset_name.replace(' ', '_')}_candlestick_{timestamp}.png"
        filepath = os.path.join(self.output_dir, filename)
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✅ Gráfico de velas guardado: {filepath}")
        return filepath
