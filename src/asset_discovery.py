"""
Módulo para descubrir nuevos activos con alto potencial de crecimiento
"""
import yfinance as yf
import pandas as pd
import numpy as np
from typing import List, Dict, Tuple
from datetime import datetime, timedelta
import json
import os


class AssetDiscovery:
    """Clase para descubrir y analizar nuevos activos prometedores"""
    
    # Listado de activos candidatos a analizar (tickers populares y emergentes)
    CANDIDATE_TICKERS = {
        # Criptomonedas emergentes
        'Solana': 'SOL-USD',
        'Cardano': 'ADA-USD',
        'Polkadot': 'DOT-USD',
        'Avalanche': 'AVAX-USD',
        'Chainlink': 'LINK-USD',
        'Polygon': 'MATIC-USD',
        
        # Tecnología emergente
        'Palantir': 'PLTR',
        'Snowflake': 'SNOW',
        'CrowdStrike': 'CRWD',
        'Cloudflare': 'NET',
        'Datadog': 'DDOG',
        'MongoDB': 'MDB',
        'Unity': 'U',
        'Roblox': 'RBLX',
        
        # IA y semiconductores
        'Advanced Micro Devices': 'AMD',
        'Intel': 'INTC',
        'Qualcomm': 'QCOM',
        'Arm Holdings': 'ARM',
        'Broadcom': 'AVGO',
        
        # Fintech
        'Block (Square)': 'SQ',
        'PayPal': 'PYPL',
        'Coinbase': 'COIN',
        'Robinhood': 'HOOD',
        
        # Energía renovable
        'First Solar': 'FSLR',
        'Enphase Energy': 'ENPH',
        'SunPower': 'SPWR',
        'Plug Power': 'PLUG',
        
        # Biotecnología
        'Moderna': 'MRNA',
        'BioNTech': 'BNTX',
        'Illumina': 'ILMN',
        'CRISPR Therapeutics': 'CRSP',
        
        # E-commerce y retail
        'Shopify': 'SHOP',
        'Etsy': 'ETSY',
        'MercadoLibre': 'MELI',
        
        # Vehículos eléctricos
        'Rivian': 'RIVN',
        'Lucid': 'LCID',
        'NIO': 'NIO',
        'Li Auto': 'LI',
        
        # Gaming y entretenimiento
        'Sea Limited': 'SE',
        'DraftKings': 'DKNG',
        
        # Cloud y SaaS
        'Zoom': 'ZM',
        'DocuSign': 'DOCU',
        'Twilio': 'TWLO',
        'Okta': 'OKTA',
    }
    
    def __init__(self):
        """Inicializa el descubridor de activos"""
        self.discovered_assets = []
        self.config_file = "src/discovered_assets.json"
        
    def analyze_asset_potential(self, ticker: str, name: str) -> Dict:
        """
        Analiza el potencial de crecimiento de un activo
        
        Args:
            ticker: Símbolo del activo
            name: Nombre del activo
            
        Returns:
            Diccionario con análisis del potencial
        """
        try:
            # Obtener datos históricos
            stock = yf.Ticker(ticker)
            data = stock.history(period="6mo", interval="1d")
            
            if len(data) < 30:
                return None
            
            # Calcular métricas de crecimiento
            precio_actual = data['Close'].iloc[-1]
            precio_inicio = data['Close'].iloc[0]
            precio_30d = data['Close'].iloc[-30] if len(data) >= 30 else data['Close'].iloc[0]
            precio_90d = data['Close'].iloc[-90] if len(data) >= 90 else data['Close'].iloc[0]
            
            # Crecimiento
            crecimiento_6m = ((precio_actual - precio_inicio) / precio_inicio) * 100
            crecimiento_30d = ((precio_actual - precio_30d) / precio_30d) * 100
            crecimiento_90d = ((precio_actual - precio_90d) / precio_90d) * 100
            
            # Volatilidad
            volatilidad = data['Close'].pct_change().std() * 100
            
            # Volumen promedio (liquidez)
            volumen_promedio = data['Volume'].mean()
            volumen_reciente = data['Volume'].tail(10).mean()
            aumento_volumen = ((volumen_reciente - volumen_promedio) / volumen_promedio) * 100 if volumen_promedio > 0 else 0
            
            # Momentum (RSI simplificado)
            delta = data['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            rsi_actual = rsi.iloc[-1] if not pd.isna(rsi.iloc[-1]) else 50
            
            # Tendencia (SMA)
            sma_20 = data['Close'].rolling(window=20).mean().iloc[-1]
            sma_50 = data['Close'].rolling(window=50).mean().iloc[-1] if len(data) >= 50 else sma_20
            tendencia_alcista = precio_actual > sma_20 > sma_50
            
            # Calcular score de potencial (0-100)
            score = 0
            
            # Crecimiento reciente (30%)
            if crecimiento_30d > 10:
                score += 30
            elif crecimiento_30d > 5:
                score += 20
            elif crecimiento_30d > 0:
                score += 10
            
            # Crecimiento a medio plazo (25%)
            if crecimiento_90d > 20:
                score += 25
            elif crecimiento_90d > 10:
                score += 15
            elif crecimiento_90d > 0:
                score += 5
            
            # Momentum y RSI (20%)
            if 30 < rsi_actual < 70 and tendencia_alcista:
                score += 20
            elif tendencia_alcista:
                score += 10
            
            # Volumen creciente (15%)
            if aumento_volumen > 20:
                score += 15
            elif aumento_volumen > 0:
                score += 7
            
            # Volatilidad controlada (10%)
            if volatilidad < 3:
                score += 10
            elif volatilidad < 5:
                score += 5
            
            return {
                'nombre': name,
                'ticker': ticker,
                'precio_actual': float(precio_actual),
                'crecimiento_30d': float(crecimiento_30d),
                'crecimiento_90d': float(crecimiento_90d),
                'crecimiento_6m': float(crecimiento_6m),
                'volatilidad': float(volatilidad),
                'rsi': float(rsi_actual),
                'tendencia_alcista': bool(tendencia_alcista),
                'volumen_promedio': float(volumen_promedio),
                'aumento_volumen': float(aumento_volumen),
                'score_potencial': int(score),
                'fecha_analisis': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
        except Exception as e:
            print(f"⚠️ Error analizando {name} ({ticker}): {e}")
            return None
    
    def discover_promising_assets(self, min_score: int = 60, progress_callback=None) -> List[Dict]:
        """
        Descubre activos prometedores del catálogo de candidatos
        
        Args:
            min_score: Score mínimo para considerar un activo (0-100)
            progress_callback: Función para reportar progreso
            
        Returns:
            Lista de activos prometedores ordenados por score
        """
        print("\n🔍 BUSCANDO NUEVOS ACTIVOS PROMETEDORES...")
        print(f"   Analizando {len(self.CANDIDATE_TICKERS)} activos candidatos...")
        print(f"   Score mínimo requerido: {min_score}/100\n")
        
        promising_assets = []
        total = len(self.CANDIDATE_TICKERS)
        
        for idx, (name, ticker) in enumerate(self.CANDIDATE_TICKERS.items(), 1):
            if progress_callback:
                progress_callback(f"Analizando {name}...", idx / total)
            else:
                print(f"[{idx}/{total}] Analizando {name} ({ticker})...")
            
            result = self.analyze_asset_potential(ticker, name)
            
            if result and result['score_potencial'] >= min_score:
                promising_assets.append(result)
                print(f"   ✅ {name}: Score {result['score_potencial']}/100 - ¡PROMETEDOR!")
        
        # Ordenar por score
        promising_assets.sort(key=lambda x: x['score_potencial'], reverse=True)
        self.discovered_assets = promising_assets
        
        return promising_assets
    
    def save_discovered_assets(self) -> str:
        """
        Guarda los activos descubiertos en archivo JSON
        
        Returns:
            Ruta del archivo guardado
        """
        if not self.discovered_assets:
            return None
        
        os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
        
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump({
                'fecha_descubrimiento': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'total_activos': len(self.discovered_assets),
                'activos': self.discovered_assets
            }, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Activos descubiertos guardados en: {self.config_file}")
        return self.config_file
    
    def generate_discovery_report(self) -> str:
        """
        Genera un reporte de los activos descubiertos
        
        Returns:
            String con el reporte
        """
        if not self.discovered_assets:
            return "⚠️ No se han descubierto activos prometedores"
        
        report = """
╔══════════════════════════════════════════════════════════════════════════════╗
║              ACTIVOS EMERGENTES CON ALTO POTENCIAL DE CRECIMIENTO
╚══════════════════════════════════════════════════════════════════════════════╝

"""
        
        report += f"📊 Total de activos descubiertos: {len(self.discovered_assets)}\n"
        report += f"📅 Fecha de análisis: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n"
        
        report += "═══════════════════════════════════════════════════════════════════════════════\n"
        report += "                        🏆 TOP ACTIVOS DESCUBIERTOS\n"
        report += "═══════════════════════════════════════════════════════════════════════════════\n\n"
        
        medals = ["🥇", "🥈", "🥉"] + ["🏅"] * 10
        
        for idx, asset in enumerate(self.discovered_assets[:10], 1):
            medal = medals[idx-1] if idx <= len(medals) else "📌"
            
            report += f"{medal} #{idx} - {asset['nombre']} ({asset['ticker']})\n"
            report += f"   • Precio actual: ${asset['precio_actual']:,.2f}\n"
            report += f"   • Score de potencial: {asset['score_potencial']}/100\n"
            report += f"   • Crecimiento 30 días: {asset['crecimiento_30d']:+.2f}%\n"
            report += f"   • Crecimiento 90 días: {asset['crecimiento_90d']:+.2f}%\n"
            report += f"   • Crecimiento 6 meses: {asset['crecimiento_6m']:+.2f}%\n"
            report += f"   • Volatilidad: {asset['volatilidad']:.2f}%\n"
            report += f"   • RSI: {asset['rsi']:.1f}\n"
            report += f"   • Tendencia: {'📈 Alcista' if asset['tendencia_alcista'] else '📉 No alcista'}\n"
            report += f"   • Aumento de volumen: {asset['aumento_volumen']:+.1f}%\n\n"
        
        report += "\n═══════════════════════════════════════════════════════════════════════════════\n"
        report += "   💡 Estos activos pueden ser añadidos al análisis comparativo\n"
        report += "═══════════════════════════════════════════════════════════════════════════════\n"
        
        return report
    
    def get_assets_for_addition(self) -> Dict[str, str]:
        """
        Obtiene diccionario de activos para añadir a MarketAnalyzer.ASSETS
        
        Returns:
            Diccionario {nombre: ticker}
        """
        return {asset['nombre']: asset['ticker'] for asset in self.discovered_assets}
