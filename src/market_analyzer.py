"""
Analizador de mercados financieros
Obtiene datos de cualquier activo y realiza análisis técnico
"""
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, Tuple, Optional
import warnings
import json
import os
warnings.filterwarnings('ignore')


class MarketAnalyzer:
    """Clase para analizar activos financieros"""
    
    # Diccionario de activos disponibles
    ASSETS = {
        'Bitcoin': 'BTC-USD',
        'Ethereum': 'ETH-USD',
        'Tesla': 'TSLA',
        'Apple': 'AAPL',
        'Microsoft': 'MSFT',
        'Amazon': 'AMZN',
        'Google': 'GOOGL',
        'NVIDIA': 'NVDA',
        'Meta': 'META',
        'Netflix': 'NFLX',
        'S&P 500': '^GSPC',
        'Dow Jones': '^DJI',
        'NASDAQ': '^IXIC',
        'Oro': 'GC=F',
        'Plata': 'SI=F'
    }
    
    def __init__(self, asset_name: str):
        """
        Inicializa el analizador
        
        Args:
            asset_name: Nombre del activo (ej: 'Bitcoin', 'Tesla')
        """
        self.asset_name = asset_name
        self.ticker_symbol = self.ASSETS.get(asset_name, asset_name)
        self.ticker = yf.Ticker(self.ticker_symbol)
        self.data = None
        
    def get_data(self, period: str = "1mo", interval: str = "1d") -> pd.DataFrame:
        """
        Obtiene datos históricos del activo
        
        Args:
            period: Periodo de tiempo ('1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y')
            interval: Intervalo de datos ('1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo')
            
        Returns:
            DataFrame con los datos históricos
            
        Note:
            yfinance tiene restricciones sobre combinaciones periodo/intervalo:
            - Intervalos < 1h: máximo 7 días de datos
            - Intervalo 1h: máximo 730 días
            - Intervalo >= 1d: sin restricción importante
        """
        try:
            # Ajustar periodo según intervalo para evitar restricciones de yfinance
            adjusted_period = self._adjust_period_for_interval(period, interval)
            
            self.data = self.ticker.history(period=adjusted_period, interval=interval)
            
            if self.data.empty:
                raise ValueError(f"No se pudieron obtener datos para {self.asset_name}")
            
            # Información de debug
            print(f"   📊 Obtenidos {len(self.data)} datos para {self.asset_name}")
            print(f"   📅 Rango: {self.data.index[0]} a {self.data.index[-1]}")
            
            return self.data
        except Exception as e:
            raise Exception(f"Error al obtener datos: {str(e)}")
    
    def _adjust_period_for_interval(self, period: str, interval: str) -> str:
        """
        Ajusta el periodo según el intervalo para evitar restricciones de yfinance
        
        Args:
            period: Periodo solicitado
            interval: Intervalo solicitado
            
        Returns:
            Periodo ajustado
        """
        # Mapeo de restricciones de yfinance
        # Intervalos intraday (< 1d) tienen restricción de 60 días máximo
        intraday_intervals = ['1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h']
        
        if interval in intraday_intervals:
            # Para intervalos intraday, yfinance limita a ~60 días
            # Pero para 1m, 2m, 5m solo permite 7 días
            if interval in ['1m', '2m', '5m']:
                max_days_map = {
                    '5y': '7d',
                    '2y': '7d',
                    '1y': '7d',
                    '6mo': '7d',
                    '3mo': '7d',
                    '1mo': '7d',
                    '5d': '5d',
                    '1d': '1d'
                }
                adjusted = max_days_map.get(period, '7d')
                if adjusted != period:
                    print(f"   ⚠️ Periodo ajustado de '{period}' a '{adjusted}' (límite de yfinance para intervalo {interval})")
                return adjusted
            
            elif interval in ['15m', '30m']:
                # Para 15m y 30m: máximo 60 días
                max_days_map = {
                    '5y': '60d',
                    '2y': '60d',
                    '1y': '60d',
                    '6mo': '60d',
                    '3mo': '60d',
                    '1mo': '1mo',
                    '5d': '5d',
                    '1d': '1d'
                }
                adjusted = max_days_map.get(period, '60d')
                if adjusted != period:
                    print(f"   ⚠️ Periodo ajustado de '{period}' a '{adjusted}' (límite de yfinance para intervalo {interval})")
                return adjusted
            
            elif interval in ['60m', '90m', '1h']:
                # Para 1h: máximo 730 días
                max_days_map = {
                    '5y': '730d',
                    '2y': '2y',
                    '1y': '1y',
                    '6mo': '6mo',
                    '3mo': '3mo',
                    '1mo': '1mo',
                    '5d': '5d',
                    '1d': '1d'
                }
                adjusted = max_days_map.get(period, '730d')
                if adjusted != period:
                    print(f"   ⚠️ Periodo ajustado de '{period}' a '{adjusted}' (límite de yfinance para intervalo {interval})")
                return adjusted
        
        # Para intervalos diarios o mayores, no hay restricción importante
        return period
    
    def calculate_statistics(self) -> Dict:
        """
        Calcula estadísticas básicas del activo
        
        Returns:
            Diccionario con estadísticas
        """
        if self.data is None or self.data.empty:
            raise ValueError("No hay datos disponibles. Ejecuta get_data() primero.")
        
        precio_actual = self.data['Close'].iloc[-1]
        precio_inicial = self.data['Close'].iloc[0]
        precio_max = self.data['High'].max()
        precio_min = self.data['Low'].min()
        volumen_promedio = self.data['Volume'].mean()
        
        # Calcular variaciones
        variacion_absoluta = precio_actual - precio_inicial
        variacion_porcentual = (variacion_absoluta / precio_inicial) * 100
        
        # Calcular volatilidad (desviación estándar de los retornos)
        retornos = self.data['Close'].pct_change().dropna()
        volatilidad = retornos.std() * 100
        
        return {
            'precio_actual': precio_actual,
            'precio_inicial': precio_inicial,
            'precio_maximo': precio_max,
            'precio_minimo': precio_min,
            'variacion_absoluta': variacion_absoluta,
            'variacion_porcentual': variacion_porcentual,
            'volatilidad': volatilidad,
            'volumen_promedio': volumen_promedio,
            'num_datos': len(self.data)
        }
    
    def detect_trends(self) -> Dict:
        """
        Detecta tendencias y patrones en los datos
        
        Returns:
            Diccionario con información de tendencias
        """
        if self.data is None or self.data.empty:
            raise ValueError("No hay datos disponibles.")
        
        # Calcular medias móviles
        self.data['SMA_20'] = self.data['Close'].rolling(window=20).mean()
        self.data['SMA_50'] = self.data['Close'].rolling(window=50).mean()
        
        # Tendencia actual (basada en las últimas 20 observaciones)
        ultimos_precios = self.data['Close'].tail(20)
        tendencia = "alcista" if ultimos_precios.iloc[-1] > ultimos_precios.iloc[0] else "bajista"
        
        # Detectar cruces de medias móviles (señal de compra/venta)
        precio_actual = self.data['Close'].iloc[-1]
        sma_20 = self.data['SMA_20'].iloc[-1] if not pd.isna(self.data['SMA_20'].iloc[-1]) else None
        sma_50 = self.data['SMA_50'].iloc[-1] if not pd.isna(self.data['SMA_50'].iloc[-1]) else None
        
        señal = "neutral"
        if sma_20 and sma_50:
            if sma_20 > sma_50:
                señal = "compra (alcista)"
            else:
                señal = "venta (bajista)"
        
        # Calcular RSI (Relative Strength Index)
        rsi = self._calculate_rsi()
        
        # Detectar soportes y resistencias
        soporte = self.data['Low'].tail(30).min()
        resistencia = self.data['High'].tail(30).max()
        
        return {
            'tendencia': tendencia,
            'señal': señal,
            'sma_20': sma_20,
            'sma_50': sma_50,
            'rsi': rsi,
            'soporte': soporte,
            'resistencia': resistencia,
            'precio_vs_sma20': ((precio_actual - sma_20) / sma_20 * 100) if sma_20 else None,
            'precio_vs_sma50': ((precio_actual - sma_50) / sma_50 * 100) if sma_50 else None
        }
    
    def _calculate_rsi(self, period: int = 14) -> Optional[float]:
        """
        Calcula el RSI (Relative Strength Index)
        
        Args:
            period: Periodo para el cálculo del RSI
            
        Returns:
            Valor del RSI o None
        """
        if len(self.data) < period:
            return None
        
        delta = self.data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        
        return rsi.iloc[-1] if not pd.isna(rsi.iloc[-1]) else None
    
    def get_summary(self) -> str:
        """
        Genera un resumen completo del análisis
        
        Returns:
            String con el resumen formateado
        """
        stats = self.calculate_statistics()
        trends = self.detect_trends()
        
        summary = f"""
╔══════════════════════════════════════════════════════════════╗
║         ANÁLISIS COMPLETO: {self.asset_name.upper()}
╚══════════════════════════════════════════════════════════════╝

📊 ESTADÍSTICAS BÁSICAS:
   • Precio Actual: ${stats['precio_actual']:,.2f}
   • Precio Inicial (periodo): ${stats['precio_inicial']:,.2f}
   • Precio Máximo: ${stats['precio_maximo']:,.2f}
   • Precio Mínimo: ${stats['precio_minimo']:,.2f}
   • Variación: {stats['variacion_porcentual']:+.2f}% (${stats['variacion_absoluta']:+,.2f})
   • Volatilidad: {stats['volatilidad']:.2f}%
   • Volumen Promedio: {stats['volumen_promedio']:,.0f}

📈 ANÁLISIS TÉCNICO:
   • Tendencia Actual: {trends['tendencia'].upper()}
   • Señal: {trends['señal'].upper()}"""
        
        # Añadir SMA 20 si está disponible
        if trends['sma_20'] is not None:
            summary += f"\n   • SMA 20: ${trends['sma_20']:,.2f}"
            if trends['precio_vs_sma20'] is not None:
                summary += f" ({trends['precio_vs_sma20']:+.2f}% del precio)"
        
        # Añadir SMA 50 si está disponible
        if trends['sma_50'] is not None:
            summary += f"\n   • SMA 50: ${trends['sma_50']:,.2f}"
            if trends['precio_vs_sma50'] is not None:
                summary += f" ({trends['precio_vs_sma50']:+.2f}% del precio)"
        
        # Añadir RSI si está disponible
        if trends['rsi'] is not None:
            rsi_status = '(SOBRECOMPRA)' if trends['rsi'] > 70 else '(SOBREVENTA)' if trends['rsi'] < 30 else '(NEUTRAL)'
            summary += f"\n   • RSI (14): {trends['rsi']:.2f} {rsi_status}"
        
        summary += f"""
   • Soporte: ${trends['soporte']:,.2f}
   • Resistencia: ${trends['resistencia']:,.2f}

💡 INTERPRETACIÓN:
"""
        
        # Añadir interpretación
        if trends['rsi']:
            if trends['rsi'] > 70:
                summary += "   ⚠️ RSI indica SOBRECOMPRA - posible corrección a la baja\n"
            elif trends['rsi'] < 30:
                summary += "   ✅ RSI indica SOBREVENTA - posible rebote al alza\n"
            else:
                summary += "   ℹ️ RSI en zona neutral\n"
        
        if trends['tendencia'] == "alcista":
            summary += "   📈 Tendencia alcista dominante en el periodo\n"
        else:
            summary += "   📉 Tendencia bajista dominante en el periodo\n"
        
        if "compra" in trends['señal']:
            summary += "   ✅ Media móvil 20 > Media móvil 50 (señal alcista)\n"
        elif "venta" in trends['señal']:
            summary += "   ⚠️ Media móvil 20 < Media móvil 50 (señal bajista)\n"
        
        return summary
    
    @classmethod
    def add_new_assets(cls, new_assets: Dict[str, str]) -> int:
        """
        Añade nuevos activos al diccionario ASSETS
        
        Args:
            new_assets: Diccionario {nombre: ticker} de nuevos activos
            
        Returns:
            Número de activos añadidos
        """
        added = 0
        for name, ticker in new_assets.items():
            if name not in cls.ASSETS:
                cls.ASSETS[name] = ticker
                added += 1
                print(f"   ✅ Añadido: {name} ({ticker})")
            else:
                print(f"   ⚠️ Ya existe: {name} ({ticker})")
        
        return added
    
    @classmethod
    def save_assets_to_file(cls, filepath: str = "src/assets_config.json") -> str:
        """
        Guarda el diccionario ASSETS actualizado en un archivo
        
        Args:
            filepath: Ruta del archivo
            
        Returns:
            Ruta del archivo guardado
        """
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        config = {
            'fecha_actualizacion': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'total_activos': len(cls.ASSETS),
            'activos': cls.ASSETS
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Configuración de activos guardada en: {filepath}")
        return filepath
    
    @classmethod
    def load_assets_from_file(cls, filepath: str = "src/assets_config.json") -> int:
        """
        Carga activos desde un archivo de configuración
        
        Args:
            filepath: Ruta del archivo
            
        Returns:
            Número de activos cargados
        """
        if not os.path.exists(filepath):
            return 0
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            loaded_assets = config.get('activos', {})
            cls.ASSETS.update(loaded_assets)
            
            print(f"✅ Cargados {len(loaded_assets)} activos desde {filepath}")
            return len(loaded_assets)
        except Exception as e:
            print(f"⚠️ Error cargando activos: {e}")
            return 0
