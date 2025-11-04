"""
Visualizador avanzado con patrones marcados y predicciones
"""
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.patches as mpatches
from matplotlib.patches import Rectangle, FancyBboxPatch
import seaborn as sns
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
from typing import Dict, List

plt.style.use('seaborn-v0_8-darkgrid')


class AdvancedVisualizer:
    """Clase para generar visualizaciones avanzadas con patrones marcados"""
    
    def __init__(self, output_dir: str = "outputs/graphs"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        plt.rcParams['figure.figsize'] = (18, 12)
        plt.rcParams['font.size'] = 9
        
    def plot_patterns_marked(self, data: pd.DataFrame, asset_name: str,
                            patterns: Dict, predictions: Dict) -> str:
        """
        Crea un gráfico con patrones marcados y predicciones (con filtrado inteligente)
        
        Args:
            data: DataFrame con datos
            asset_name: Nombre del activo
            patterns: Patrones detectados
            predictions: Predicciones futuras
            
        Returns:
            Ruta del archivo guardado
        """
        fig = plt.figure(figsize=(20, 14))
        gs = fig.add_gridspec(4, 2, hspace=0.3, wspace=0.25)
        
        # FILTRADO INTELIGENTE DE DATOS - INCREMENTADO
        num_datos = len(data)
        
        # Determinar factor de submuestreo (más agresivo)
        if num_datos > 1000:
            step_data = max(1, num_datos // 250)  # Máximo 250 puntos (antes 400)
        elif num_datos > 500:
            step_data = max(1, num_datos // 300)  # Máximo 300 puntos
        else:
            step_data = 1
        
        if step_data > 1:
            data_filtered = data.iloc[::step_data].copy()
            print(f"   ℹ️ Datos filtrados: {num_datos} → {len(data_filtered)} puntos (cada {step_data})")
        else:
            data_filtered = data.copy()
        
        # Gráfico principal con patrones marcados
        ax_main = fig.add_subplot(gs[0:2, :])
        
        # Plotear precio con datos filtrados
        ax_main.plot(data_filtered.index, data_filtered['Close'], linewidth=2, color='#2E86AB', 
                    label='Precio', zorder=5)
        
        # Añadir medias móviles si existen
        if 'SMA_20' in data_filtered.columns:
            ax_main.plot(data_filtered.index, data_filtered['SMA_20'], linewidth=1.5, 
                        linestyle='--', color='#A23B72', alpha=0.7, label='SMA 20')
        if 'SMA_50' in data_filtered.columns:
            ax_main.plot(data_filtered.index, data_filtered['SMA_50'], linewidth=1.5, 
                        linestyle='--', color='#F18F01', alpha=0.7, label='SMA 50')
        
        # MARCAR PATRONES EN EL GRÁFICO (FILTRADO INTELIGENTE)
        patron_colors = {
            'Alcista': '#28a745',
            'Bajista': '#dc3545',
            'Neutral': '#ffc107'
        }
        
        patron_markers = {
            'Martillo (Hammer)': '^',
            'Estrella Fugaz': 'v',
            'Envolvente Alcista': '^',
            'Envolvente Bajista': 'v',
            'Doji': 'o',
            'Tres Soldados Blancos': '^',
            'Tres Cuervos Negros': 'v',
            'Doble Techo': 'v',
            'Doble Suelo': '^',
            'Ruptura de Resistencia': '^',
            'Ruptura de Soporte': 'v',
            'Divergencia Alcista': '^',
            'Divergencia Bajista': 'v'
        }
        
        # FILTRADO DE PATRONES: Mostrar solo los más relevantes
        patrones_todos = patterns.get('todos', [])
        
        # Calcular número máximo de patrones a mostrar según densidad de datos
        if num_datos > 500:
            max_patrones = 15  # Muy pocos patrones para alta densidad
        elif num_datos > 200:
            max_patrones = 25
        else:
            max_patrones = 40
        
        # Filtrar patrones: solo los más recientes y relevantes
        patrones_a_mostrar = patrones_todos[:max_patrones]
        print(f"   ℹ️ Patrones mostrados: {len(patrones_a_mostrar)}/{len(patrones_todos)} (evitar solapamiento)")
        
        # Marcar cada patrón filtrado
        patrones_marcados = {'Alcista': [], 'Bajista': [], 'Neutral': []}
        patrones_mostrados = 0
        
        for pattern in patrones_a_mostrar:
            try:
                fecha = pattern['fecha']
                tipo = pattern.get('tipo', pattern.get('señal', 'Neutral'))
                patron_nombre = pattern.get('patron', pattern.get('tipo', ''))
                
                # Encontrar el precio en esa fecha
                if fecha in data.index:
                    precio = data.loc[fecha, 'Close']
                    color = patron_colors.get(tipo, '#ffc107')
                    marker = patron_markers.get(patron_nombre, 'D')
                    
                    # Tamaño de marcador adaptativo (más pequeño si hay muchos datos)
                    marker_size = 150 if num_datos > 300 else 200
                    
                    # Marcar el punto
                    ax_main.scatter(fecha, precio, s=marker_size, marker=marker, 
                                  color=color, edgecolors='black', linewidth=2,
                                  zorder=10, alpha=0.8)
                    
                    # ANOTACIONES: Solo mostrar cada N patrones para evitar solapamiento
                    annotation_step = max(1, len(patrones_a_mostrar) // 12)  # Max 12 anotaciones
                    
                    if patrones_mostrados % annotation_step == 0:
                        offset = 0.02 * (data['Close'].max() - data['Close'].min())
                        y_pos = precio + offset if tipo == 'Alcista' else precio - offset
                        va = 'bottom' if tipo == 'Alcista' else 'top'
                        
                        # Tamaño de fuente adaptativo
                        fontsize = 6 if num_datos > 300 else 7
                        
                        ax_main.annotate(patron_nombre, xy=(fecha, precio),
                                       xytext=(fecha, y_pos),
                                       fontsize=fontsize, ha='center', va=va,
                                       bbox=dict(boxstyle='round,pad=0.3', 
                                               facecolor=color, alpha=0.6),
                                       arrowprops=dict(arrowstyle='->', 
                                                     connectionstyle='arc3,rad=0'))
                    
                    patrones_marcados[tipo].append(patron_nombre)
                    patrones_mostrados += 1
            except:
                continue
        
        # Añadir zona de predicción
        if predictions and predictions.get('rango_precio_estimado'):
            ultimo_idx = data.index[-1]
            # Crear fechas futuras para la proyección
            dias_proyeccion = 5
            fechas_futuras = pd.date_range(start=ultimo_idx, periods=dias_proyeccion+1, freq='D')[1:]
            
            precio_actual = data['Close'].iloc[-1]
            precio_objetivo = predictions['rango_precio_estimado']['objetivo']
            precio_min = predictions['rango_precio_estimado']['minimo']
            precio_max = predictions['rango_precio_estimado']['maximo']
            
            # Línea de proyección
            fechas_proyeccion = [ultimo_idx] + list(fechas_futuras)
            precios_proyeccion = [precio_actual] + [precio_objetivo] * dias_proyeccion
            
            ax_main.plot(fechas_proyeccion, precios_proyeccion, 
                        linestyle='--', linewidth=2, color='purple', 
                        label='Proyección', alpha=0.8)
            
            # Zona de confianza
            ax_main.fill_between(fechas_futuras, 
                                [precio_min]*dias_proyeccion,
                                [precio_max]*dias_proyeccion,
                                alpha=0.2, color='purple', label='Rango estimado')
        
        ax_main.set_title(f'Análisis Técnico Completo: {asset_name} - Patrones Detectados y Proyección',
                         fontsize=16, fontweight='bold', pad=20)
        ax_main.set_ylabel('Precio (USD)', fontsize=12, fontweight='bold')
        ax_main.legend(loc='best', fontsize=9, framealpha=0.9)
        ax_main.grid(True, alpha=0.3)
        
        # SINCRONIZAR EJE X: Guardar límites
        x_min = data_filtered.index.min()
        x_max = data_filtered.index.max()
        
        ax_main.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y'))
        ax_main.set_xlim(x_min, x_max)  # Aplicar límites
        plt.setp(ax_main.xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        # Gráfico de volumen con FILTRADO INTELIGENTE y EJE X SINCRONIZADO
        ax_vol = fig.add_subplot(gs[2, :])
        
        # Usar datos filtrados también para volumen
        colors_vol = ['green' if data_filtered['Close'].iloc[i] >= data_filtered['Open'].iloc[i] 
                     else 'red' for i in range(len(data_filtered))]
        
        # Ajustar ancho de barras según densidad
        bar_width = step_data * 0.8 if step_data > 1 else 0.8
        
        ax_vol.bar(data_filtered.index, data_filtered['Volume'], 
                  color=colors_vol, alpha=0.6, width=bar_width)
        
        # Marcar SOLO patrones de volumen extremo más relevantes (filtrado)
        patrones_volumen = patterns.get('volumen', [])
        max_vol_patterns = 8 if num_datos > 300 else 15  # Menos marcadores si hay muchos datos
        
        for pattern in patrones_volumen[:max_vol_patterns]:
            try:
                if pattern['fecha'] in data.index:
                    vol = data.loc[pattern['fecha'], 'Volume']
                    color = 'green' if 'Alcista' in pattern['patron'] else 'red'
                    
                    # Tamaño de estrella adaptativo
                    star_size = 250 if num_datos > 300 else 300
                    
                    ax_vol.scatter(pattern['fecha'], vol, s=star_size, marker='*',
                                 color='yellow', edgecolors=color, linewidth=3, zorder=10)
            except:
                continue
        
        vol_info = f'{len(data_filtered)} datos' if step_data > 1 else f'{num_datos} datos'
        ax_vol.set_title(f'Volumen de Transacciones ({vol_info}, Patrones Extremos Marcados)', 
                        fontsize=12, fontweight='bold')
        ax_vol.set_ylabel('Volumen', fontsize=10)
        ax_vol.grid(True, alpha=0.3)
        
        # EJE X SINCRONIZADO con gráfico principal
        ax_vol.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y'))
        ax_vol.set_xlim(x_min, x_max)  # MISMO RANGO que ax_main
        plt.setp(ax_vol.xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        # Panel de información de patrones
        ax_info = fig.add_subplot(gs[3, 0])
        ax_info.axis('off')
        
        info_text = "📊 PATRONES DETECTADOS:\n\n"
        info_text += f"📈 Alcistas: {len([p for p in patterns.get('todos', []) if p.get('tipo') == 'Alcista' or p.get('señal') == 'Alcista'])}\n"
        info_text += f"📉 Bajistas: {len([p for p in patterns.get('todos', []) if p.get('tipo') == 'Bajista' or p.get('señal') == 'Bajista'])}\n"
        info_text += f"➡️ Neutrales: {len([p for p in patterns.get('todos', []) if p.get('tipo') == 'Neutral'])}\n\n"
        
        info_text += "🔮 PREDICCIÓN:\n"
        if predictions:
            info_text += f"Dirección: {predictions.get('direccion_probable', 'N/A')}\n"
            info_text += f"Confianza: {predictions.get('confianza', 0):.1f}%\n"
        
        ax_info.text(0.1, 0.5, info_text, fontsize=11, verticalalignment='center',
                    bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
        
        # Leyenda de símbolos
        ax_legend = fig.add_subplot(gs[3, 1])
        ax_legend.axis('off')
        
        legend_text = "📌 SÍMBOLOS DE PATRONES:\n\n"
        legend_text += "▲ = Patrón Alcista\n"
        legend_text += "▼ = Patrón Bajista\n"
        legend_text += "● = Patrón Neutral\n"
        legend_text += "★ = Volumen Extremo\n"
        legend_text += "- - - = Proyección Futura\n"
        
        ax_legend.text(0.1, 0.5, legend_text, fontsize=10, verticalalignment='center',
                      bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
        
        plt.tight_layout()
        
        # Guardar
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{asset_name.replace(' ', '_')}_patrones_marcados_{timestamp}.png"
        filepath = os.path.join(self.output_dir, filename)
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✅ Gráfico con patrones marcados guardado: {filepath}")
        return filepath
    
    def plot_prediction_scenarios(self, data: pd.DataFrame, asset_name: str,
                                  predictions: Dict) -> str:
        """
        Crea un gráfico de escenarios de predicción
        
        Args:
            data: DataFrame con datos históricos
            asset_name: Nombre del activo
            predictions: Diccionario con predicciones
            
        Returns:
            Ruta del archivo guardado
        """
        fig, ax = plt.subplots(figsize=(16, 9))
        
        # Plotear histórico
        ax.plot(data.index, data['Close'], linewidth=2.5, color='#2E86AB', 
               label='Histórico', zorder=5)
        
        # Proyección de escenarios
        ultimo_idx = data.index[-1]
        dias_proyeccion = 7
        fechas_futuras = pd.date_range(start=ultimo_idx, periods=dias_proyeccion+1, freq='D')[1:]
        
        precio_actual = data['Close'].iloc[-1]
        
        for escenario in predictions.get('escenarios', []):
            precio_objetivo = escenario['precio_objetivo']
            nombre = escenario['nombre']
            prob = escenario['probabilidad']
            
            # Generar proyección con variación
            proyeccion = np.linspace(precio_actual, precio_objetivo, dias_proyeccion)
            fechas_proyeccion = [ultimo_idx] + list(fechas_futuras)
            precios_proyeccion = [precio_actual] + list(proyeccion)
            
            if 'Optimista' in nombre:
                color = '#28a745'
                linestyle = '-'
            elif 'Pesimista' in nombre:
                color = '#dc3545'
                linestyle = '-'
            else:
                color = '#ffc107'
                linestyle = '--'
            
            ax.plot(fechas_proyeccion, precios_proyeccion, 
                   linestyle=linestyle, linewidth=2.5, color=color,
                   label=f'{nombre} ({prob:.0f}%)', alpha=0.8)
        
        ax.set_title(f'Escenarios de Predicción: {asset_name}', 
                    fontsize=16, fontweight='bold', pad=20)
        ax.set_ylabel('Precio (USD)', fontsize=13, fontweight='bold')
        ax.set_xlabel('Fecha', fontsize=13, fontweight='bold')
        ax.legend(loc='best', fontsize=11, framealpha=0.9)
        ax.grid(True, alpha=0.3)
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y'))
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        plt.tight_layout()
        
        # Guardar
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{asset_name.replace(' ', '_')}_escenarios_{timestamp}.png"
        filepath = os.path.join(self.output_dir, filename)
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✅ Gráfico de escenarios guardado: {filepath}")
        return filepath
