"""
Módulo de análisis técnico avanzado y detección de patrones
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
from datetime import datetime


class TechnicalPatternAnalyzer:
    """Clase para detectar patrones técnicos y tendencias en datos de mercado"""
    
    def __init__(self, data: pd.DataFrame):
        """
        Inicializa el analizador de patrones
        
        Args:
            data: DataFrame con datos OHLCV (Open, High, Low, Close, Volume)
        """
        self.data = data.copy()
        self.patterns_found = []
        
    def detect_candlestick_patterns(self) -> List[Dict]:
        """
        Detecta patrones de velas japonesas
        
        Returns:
            Lista de patrones encontrados con detalles
        """
        patterns = []
        
        if len(self.data) < 3:
            return patterns
        
        for i in range(2, len(self.data)):
            # Obtener las últimas 3 velas
            prev2 = self.data.iloc[i-2]
            prev1 = self.data.iloc[i-1]
            current = self.data.iloc[i]
            
            # Calcular características de las velas
            prev2_body = abs(prev2['Close'] - prev2['Open'])
            prev1_body = abs(prev1['Close'] - prev1['Open'])
            current_body = abs(current['Close'] - current['Open'])
            
            prev2_range = prev2['High'] - prev2['Low']
            prev1_range = prev1['High'] - prev1['Low']
            current_range = current['High'] - current['Low']
            
            # PATRÓN 1: Martillo (Hammer) - Alcista
            if current_range > 0:
                lower_shadow = min(current['Open'], current['Close']) - current['Low']
                upper_shadow = current['High'] - max(current['Open'], current['Close'])
                
                if (lower_shadow > 2 * current_body and 
                    upper_shadow < current_body * 0.3 and
                    current['Close'] < prev1['Close']):
                    patterns.append({
                        'fecha': current.name,
                        'patron': 'Martillo (Hammer)',
                        'tipo': 'Alcista',
                        'confianza': 'Media',
                        'descripcion': 'Posible reversión alcista después de tendencia bajista',
                        'precio': current['Close']
                    })
            
            # PATRÓN 2: Estrella Fugaz (Shooting Star) - Bajista
            if current_range > 0:
                upper_shadow = current['High'] - max(current['Open'], current['Close'])
                lower_shadow = min(current['Open'], current['Close']) - current['Low']
                
                if (upper_shadow > 2 * current_body and 
                    lower_shadow < current_body * 0.3 and
                    current['Close'] > prev1['Close']):
                    patterns.append({
                        'fecha': current.name,
                        'patron': 'Estrella Fugaz',
                        'tipo': 'Bajista',
                        'confianza': 'Media',
                        'descripcion': 'Posible reversión bajista después de tendencia alcista',
                        'precio': current['Close']
                    })
            
            # PATRÓN 3: Envolvente Alcista (Bullish Engulfing)
            if (prev1['Close'] < prev1['Open'] and  # Vela anterior bajista
                current['Close'] > current['Open'] and  # Vela actual alcista
                current['Open'] < prev1['Close'] and
                current['Close'] > prev1['Open'] and
                current_body > prev1_body):
                patterns.append({
                    'fecha': current.name,
                    'patron': 'Envolvente Alcista',
                    'tipo': 'Alcista',
                    'confianza': 'Alta',
                    'descripcion': 'Fuerte señal de reversión alcista',
                    'precio': current['Close']
                })
            
            # PATRÓN 4: Envolvente Bajista (Bearish Engulfing)
            if (prev1['Close'] > prev1['Open'] and  # Vela anterior alcista
                current['Close'] < current['Open'] and  # Vela actual bajista
                current['Open'] > prev1['Close'] and
                current['Close'] < prev1['Open'] and
                current_body > prev1_body):
                patterns.append({
                    'fecha': current.name,
                    'patron': 'Envolvente Bajista',
                    'tipo': 'Bajista',
                    'confianza': 'Alta',
                    'descripcion': 'Fuerte señal de reversión bajista',
                    'precio': current['Close']
                })
            
            # PATRÓN 5: Doji - Indecisión
            if current_body < current_range * 0.1 and current_range > 0:
                patterns.append({
                    'fecha': current.name,
                    'patron': 'Doji',
                    'tipo': 'Neutral',
                    'confianza': 'Baja',
                    'descripcion': 'Indecisión del mercado, posible cambio de tendencia',
                    'precio': current['Close']
                })
            
            # PATRÓN 6: Tres Soldados Blancos - Alcista
            if i >= 2:
                if (prev2['Close'] > prev2['Open'] and
                    prev1['Close'] > prev1['Open'] and
                    current['Close'] > current['Open'] and
                    prev1['Close'] > prev2['Close'] and
                    current['Close'] > prev1['Close'] and
                    prev1['Open'] > prev2['Open'] and
                    current['Open'] > prev1['Open']):
                    patterns.append({
                        'fecha': current.name,
                        'patron': 'Tres Soldados Blancos',
                        'tipo': 'Alcista',
                        'confianza': 'Muy Alta',
                        'descripcion': 'Fuerte continuación alcista',
                        'precio': current['Close']
                    })
            
            # PATRÓN 7: Tres Cuervos Negros - Bajista
            if i >= 2:
                if (prev2['Close'] < prev2['Open'] and
                    prev1['Close'] < prev1['Open'] and
                    current['Close'] < current['Open'] and
                    prev1['Close'] < prev2['Close'] and
                    current['Close'] < prev1['Close'] and
                    prev1['Open'] < prev2['Open'] and
                    current['Open'] < prev1['Open']):
                    patterns.append({
                        'fecha': current.name,
                        'patron': 'Tres Cuervos Negros',
                        'tipo': 'Bajista',
                        'confianza': 'Muy Alta',
                        'descripcion': 'Fuerte continuación bajista',
                        'precio': current['Close']
                    })
        
        return patterns
    
    def detect_chart_patterns(self) -> List[Dict]:
        """
        Detecta patrones gráficos (soportes, resistencias, canales)
        
        Returns:
            Lista de patrones gráficos encontrados
        """
        patterns = []
        
        if len(self.data) < 10:
            return patterns
        
        closes = self.data['Close'].values
        highs = self.data['High'].values
        lows = self.data['Low'].values
        
        # PATRÓN: Doble Techo (Double Top) - Bajista
        for i in range(20, len(self.data)):
            window = closes[i-20:i]
            if len(window) >= 20:
                # Buscar dos picos similares
                peaks = []
                for j in range(1, len(window)-1):
                    if window[j] > window[j-1] and window[j] > window[j+1]:
                        peaks.append((j, window[j]))
                
                if len(peaks) >= 2:
                    # Verificar si los dos últimos picos son similares
                    if abs(peaks[-1][1] - peaks[-2][1]) / peaks[-1][1] < 0.03:
                        patterns.append({
                            'fecha': self.data.index[i],
                            'patron': 'Doble Techo',
                            'tipo': 'Bajista',
                            'confianza': 'Alta',
                            'descripcion': 'Patrón de reversión bajista - precio ha fallado dos veces en romper resistencia',
                            'precio': closes[i],
                            'nivel': peaks[-1][1]
                        })
        
        # PATRÓN: Doble Suelo (Double Bottom) - Alcista
        for i in range(20, len(self.data)):
            window = closes[i-20:i]
            if len(window) >= 20:
                # Buscar dos valles similares
                valleys = []
                for j in range(1, len(window)-1):
                    if window[j] < window[j-1] and window[j] < window[j+1]:
                        valleys.append((j, window[j]))
                
                if len(valleys) >= 2:
                    # Verificar si los dos últimos valles son similares
                    if abs(valleys[-1][1] - valleys[-2][1]) / valleys[-1][1] < 0.03:
                        patterns.append({
                            'fecha': self.data.index[i],
                            'patron': 'Doble Suelo',
                            'tipo': 'Alcista',
                            'confianza': 'Alta',
                            'descripcion': 'Patrón de reversión alcista - precio ha rebotado dos veces en soporte',
                            'precio': closes[i],
                            'nivel': valleys[-1][1]
                        })
        
        # PATRÓN: Ruptura de Resistencia
        if len(self.data) >= 30:
            # Calcular resistencia (máximo de los últimos 30 días)
            resistencia = self.data['High'].tail(30).max()
            precio_actual = self.data['Close'].iloc[-1]
            
            if precio_actual > resistencia * 1.01:  # Ruptura del 1%
                patterns.append({
                    'fecha': self.data.index[-1],
                    'patron': 'Ruptura de Resistencia',
                    'tipo': 'Alcista',
                    'confianza': 'Media',
                    'descripcion': f'Precio ha roto resistencia de ${resistencia:,.2f}',
                    'precio': precio_actual,
                    'nivel': resistencia
                })
        
        # PATRÓN: Ruptura de Soporte
        if len(self.data) >= 30:
            # Calcular soporte (mínimo de los últimos 30 días)
            soporte = self.data['Low'].tail(30).min()
            precio_actual = self.data['Close'].iloc[-1]
            
            if precio_actual < soporte * 0.99:  # Ruptura del 1%
                patterns.append({
                    'fecha': self.data.index[-1],
                    'patron': 'Ruptura de Soporte',
                    'tipo': 'Bajista',
                    'confianza': 'Media',
                    'descripcion': f'Precio ha roto soporte de ${soporte:,.2f}',
                    'precio': precio_actual,
                    'nivel': soporte
                })
        
        return patterns
    
    def detect_momentum_divergences(self) -> List[Dict]:
        """
        Detecta divergencias entre precio y momentum (RSI)
        
        Returns:
            Lista de divergencias encontradas
        """
        divergences = []
        
        if len(self.data) < 30:
            return divergences
        
        # Calcular RSI
        delta = self.data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        
        closes = self.data['Close'].values
        rsi_values = rsi.values
        
        # Buscar divergencias alcistas (precio baja, RSI sube)
        for i in range(30, len(self.data)):
            if not np.isnan(rsi_values[i]) and not np.isnan(rsi_values[i-20]):
                precio_cambio = (closes[i] - closes[i-20]) / closes[i-20]
                rsi_cambio = rsi_values[i] - rsi_values[i-20]
                
                # Divergencia Alcista: precio baja pero RSI sube
                if precio_cambio < -0.05 and rsi_cambio > 5:
                    divergences.append({
                        'fecha': self.data.index[i],
                        'tipo': 'Divergencia Alcista',
                        'señal': 'Alcista',
                        'confianza': 'Media',
                        'descripcion': 'Precio en mínimos más bajos pero RSI en mínimos más altos',
                        'precio': closes[i],
                        'rsi': rsi_values[i]
                    })
                
                # Divergencia Bajista: precio sube pero RSI baja
                if precio_cambio > 0.05 and rsi_cambio < -5:
                    divergences.append({
                        'fecha': self.data.index[i],
                        'tipo': 'Divergencia Bajista',
                        'señal': 'Bajista',
                        'confianza': 'Media',
                        'descripcion': 'Precio en máximos más altos pero RSI en máximos más bajos',
                        'precio': closes[i],
                        'rsi': rsi_values[i]
                    })
        
        return divergences
    
    def detect_volume_patterns(self) -> List[Dict]:
        """
        Detecta patrones de volumen significativos
        
        Returns:
            Lista de patrones de volumen
        """
        patterns = []
        
        if len(self.data) < 20 or 'Volume' not in self.data.columns:
            return patterns
        
        avg_volume = self.data['Volume'].tail(20).mean()
        
        for i in range(20, len(self.data)):
            current_volume = self.data['Volume'].iloc[i]
            current_price_change = (self.data['Close'].iloc[i] - self.data['Close'].iloc[i-1]) / self.data['Close'].iloc[i-1]
            
            # Volumen inusualmente alto
            if current_volume > avg_volume * 2:
                if current_price_change > 0:
                    patterns.append({
                        'fecha': self.data.index[i],
                        'patron': 'Volumen Alcista Extremo',
                        'tipo': 'Alcista',
                        'confianza': 'Alta',
                        'descripcion': f'Volumen {current_volume/avg_volume:.1f}x superior al promedio con subida de precio',
                        'precio': self.data['Close'].iloc[i],
                        'volumen': current_volume
                    })
                else:
                    patterns.append({
                        'fecha': self.data.index[i],
                        'patron': 'Volumen Bajista Extremo',
                        'tipo': 'Bajista',
                        'confianza': 'Alta',
                        'descripcion': f'Volumen {current_volume/avg_volume:.1f}x superior al promedio con caída de precio',
                        'precio': self.data['Close'].iloc[i],
                        'volumen': current_volume
                    })
        
        return patterns
    
    def analyze_all_patterns(self) -> Dict:
        """
        Ejecuta todos los análisis de patrones
        
        Returns:
            Diccionario con todos los patrones encontrados
        """
        print("🔍 Detectando patrones técnicos...")
        
        candlestick = self.detect_candlestick_patterns()
        chart = self.detect_chart_patterns()
        divergences = self.detect_momentum_divergences()
        volume = self.detect_volume_patterns()
        
        # Eliminar duplicados por fecha (mantener solo el más importante)
        all_patterns = candlestick + chart + divergences + volume
        
        # Ordenar por fecha (más recientes primero)
        all_patterns.sort(key=lambda x: x['fecha'], reverse=True)
        
        return {
            'velas_japonesas': candlestick,
            'patrones_graficos': chart,
            'divergencias': divergences,
            'volumen': volume,
            'total': len(all_patterns),
            'todos': all_patterns[:20]  # Los 20 más recientes
        }
    
    def generate_pattern_report(self, patterns_dict: Dict) -> str:
        """
        Genera un reporte detallado de patrones encontrados
        
        Args:
            patterns_dict: Diccionario con patrones encontrados
            
        Returns:
            String con el reporte formateado
        """
        report = """
╔══════════════════════════════════════════════════════════════╗
║      DETECCIÓN DE PATRONES Y TENDENCIAS TÉCNICAS
╚══════════════════════════════════════════════════════════════╝

📊 RESUMEN DE PATRONES DETECTADOS:
"""
        
        report += f"   • Total de patrones encontrados: {patterns_dict['total']}\n"
        report += f"   • Patrones de velas japonesas: {len(patterns_dict['velas_japonesas'])}\n"
        report += f"   • Patrones gráficos: {len(patterns_dict['patrones_graficos'])}\n"
        report += f"   • Divergencias de momentum: {len(patterns_dict['divergencias'])}\n"
        report += f"   • Patrones de volumen: {len(patterns_dict['volumen'])}\n\n"
        
        if patterns_dict['total'] == 0:
            report += "ℹ️ No se detectaron patrones significativos en el periodo analizado.\n"
            return report
        
        report += "🔝 PATRONES MÁS RECIENTES:\n\n"
        
        for i, pattern in enumerate(patterns_dict['todos'][:10], 1):
            fecha_str = pattern['fecha'].strftime("%d/%m/%Y") if hasattr(pattern['fecha'], 'strftime') else str(pattern['fecha'])
            
            # Emoji según el tipo
            emoji = "📈" if pattern.get('tipo') == 'Alcista' or pattern.get('señal') == 'Alcista' else "📉" if pattern.get('tipo') == 'Bajista' or pattern.get('señal') == 'Bajista' else "➡️"
            
            tipo_patron = pattern.get('patron', pattern.get('tipo', 'Patrón'))
            confianza = pattern.get('confianza', 'N/A')
            descripcion = pattern.get('descripcion', '')
            precio = pattern.get('precio', 0)
            
            report += f"{i}. {emoji} [{fecha_str}] {tipo_patron}\n"
            report += f"   Confianza: {confianza} | Precio: ${precio:,.2f}\n"
            report += f"   {descripcion}\n\n"
        
        # Análisis consolidado
        report += "💡 ANÁLISIS CONSOLIDADO:\n\n"
        
        alcistas = sum(1 for p in patterns_dict['todos'] if p.get('tipo') == 'Alcista' or p.get('señal') == 'Alcista')
        bajistas = sum(1 for p in patterns_dict['todos'] if p.get('tipo') == 'Bajista' or p.get('señal') == 'Bajista')
        neutrales = patterns_dict['total'] - alcistas - bajistas
        
        if alcistas > bajistas:
            report += f"   ✅ TENDENCIA PREDOMINANTE: ALCISTA\n"
            report += f"   • Patrones alcistas: {alcistas} ({alcistas/patterns_dict['total']*100:.1f}%)\n"
            report += f"   • Patrones bajistas: {bajistas} ({bajistas/patterns_dict['total']*100:.1f}%)\n"
            report += f"   • Interpretación: Los patrones sugieren una tendencia alcista\n"
        elif bajistas > alcistas:
            report += f"   ⚠️ TENDENCIA PREDOMINANTE: BAJISTA\n"
            report += f"   • Patrones bajistas: {bajistas} ({bajistas/patterns_dict['total']*100:.1f}%)\n"
            report += f"   • Patrones alcistas: {alcistas} ({alcistas/patterns_dict['total']*100:.1f}%)\n"
            report += f"   • Interpretación: Los patrones sugieren una tendencia bajista\n"
        else:
            report += f"   ℹ️ TENDENCIA PREDOMINANTE: NEUTRAL\n"
            report += f"   • El mercado muestra señales mixtas\n"
        
        return report
