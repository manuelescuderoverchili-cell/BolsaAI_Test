"""
Analizador de noticias relacionadas con activos financieros
"""
import requests
import feedparser
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from textblob import TextBlob
import time
from typing import List, Dict
import warnings
warnings.filterwarnings('ignore')


class NewsAnalyzer:
    """Clase para obtener y analizar noticias de activos financieros"""
    
    # Mapeo de activos a términos de búsqueda (más completo)
    SEARCH_TERMS = {
        'Bitcoin': ['bitcoin', 'btc', 'btc-usd', 'cryptocurrency', 'crypto', 'digital currency', 'blockchain'],
        'Ethereum': ['ethereum', 'eth', 'eth-usd', 'crypto', 'defi', 'smart contract'],
        'Tesla': ['tesla', 'tsla', 'elon musk', 'electric vehicle', 'ev'],
        'Apple': ['apple', 'aapl', 'iphone', 'tim cook', 'ios', 'mac'],
        'Microsoft': ['microsoft', 'msft', 'windows', 'azure', 'satya nadella'],
        'Amazon': ['amazon', 'amzn', 'aws', 'jeff bezos', 'e-commerce'],
        'Google': ['google', 'googl', 'alphabet', 'android', 'search engine'],
        'NVIDIA': ['nvidia', 'nvda', 'gpu', 'ai chip', 'graphics card'],
        'Meta': ['meta', 'facebook', 'metaverse', 'instagram', 'mark zuckerberg'],
        'Netflix': ['netflix', 'nflx', 'streaming', 'entertainment'],
        'S&P 500': ['s&p 500', 'stock market', 'wall street', 'market index'],
        'Dow Jones': ['dow jones', 'djia', 'stock market', 'industrial average'],
        'NASDAQ': ['nasdaq', 'tech stocks', 'nasdaq composite'],
        'Oro': ['gold', 'oro', 'precious metals', 'gold price'],
        'Plata': ['silver', 'plata', 'precious metals', 'silver price']
    }
    
    def __init__(self, asset_name: str):
        """
        Inicializa el analizador de noticias
        
        Args:
            asset_name: Nombre del activo
        """
        self.asset_name = asset_name
        self.search_terms = self.SEARCH_TERMS.get(asset_name, [asset_name.lower()])
        self.noticias = []
        
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        # Fuentes RSS especializadas por tipo de activo
        self.fuentes = self._get_news_sources()
    
    def _get_news_sources(self) -> Dict[str, str]:
        """Obtiene las fuentes de noticias según el tipo de activo"""
        
        # Fuentes para criptomonedas (ampliadas)
        if self.asset_name in ['Bitcoin', 'Ethereum']:
            return {
                'coindesk': 'https://www.coindesk.com/arc/outboundfeeds/rss/',
                'cointelegraph': 'https://cointelegraph.com/rss',
                'decrypt': 'https://decrypt.co/feed',
                'bitcoin_magazine': 'https://bitcoinmagazine.com/.rss/full/',
                'newsbtc': 'https://www.newsbtc.com/feed/',
                'cryptonews': 'https://cryptonews.com/news/feed/',
                'coinjournal': 'https://coinjournal.net/feed/',
                'u_today': 'https://u.today/rss',
                'bitcoinist': 'https://bitcoinist.com/feed/',
                'cryptopotato': 'https://cryptopotato.com/feed/'
            }
        
        # Fuentes para tecnología (ampliadas)
        elif self.asset_name in ['Tesla', 'Apple', 'Microsoft', 'Amazon', 'Google', 'NVIDIA', 'Meta', 'Netflix']:
            return {
                'techcrunch': 'https://techcrunch.com/feed/',
                'theverge': 'https://www.theverge.com/rss/index.xml',
                'engadget': 'https://www.engadget.com/rss.xml',
                'arstechnica': 'https://feeds.arstechnica.com/arstechnica/index',
                'techmeme': 'https://www.techmeme.com/feed.xml',
                'venturebeat': 'https://venturebeat.com/feed/',
                'mashable_tech': 'https://mashable.com/feeds/rss/tech',
                'wired': 'https://www.wired.com/feed/rss',
                'zdnet': 'https://www.zdnet.com/news/rss.xml',
                'cnet': 'https://www.cnet.com/rss/news/'
            }
        
        # Fuentes generales de finanzas (ampliadas)
        else:
            return {
                'yahoo_finance': 'https://finance.yahoo.com/news/rssindex',
                'marketwatch': 'https://feeds.marketwatch.com/marketwatch/topstories/',
                'seekingalpha': 'https://seekingalpha.com/feed.xml',
                'investing': 'https://www.investing.com/rss/news.rss',
                'forbes_investing': 'https://www.forbes.com/investing/feed/',
                'cnbc': 'https://www.cnbc.com/id/100003114/device/rss/rss.html',
                'reuters_business': 'https://www.reutersagency.com/feed/?taxonomy=best-topics&post_type=best',
                'ft': 'https://www.ft.com/?format=rss',
                'wsj': 'https://feeds.a.dj.com/rss/RSSMarketsMain.xml',
                'bloomberg_markets': 'https://www.bloomberg.com/feed/podcast/etf-report.xml'
            }
    
    def fetch_news(self, max_news: int = 50) -> List[Dict]:
        """
        Obtiene noticias de las fuentes RSS
        
        Args:
            max_news: Número máximo de noticias a obtener
            
        Returns:
            Lista de diccionarios con información de noticias
        """
        print(f"🔍 Buscando noticias sobre {self.asset_name}...")
        self.noticias = []
        noticias_por_fuente = {}
        
        for fuente_nombre, fuente_url in self.fuentes.items():
            try:
                print(f"   📡 Consultando {fuente_nombre}...")
                feed = feedparser.parse(fuente_url)
                
                noticias_encontradas = 0
                for entry in feed.entries[:20]:  # Revisar hasta 20 por fuente
                    titulo = entry.get('title', '')
                    
                    # Intentar obtener descripción de múltiples campos
                    descripcion = (
                        entry.get('summary', '') or 
                        entry.get('description', '') or 
                        entry.get('content', [{}])[0].get('value', '') if entry.get('content') else '' or
                        entry.get('subtitle', '') or
                        titulo  # Si no hay descripción, usar el título como fallback
                    )
                    
                    # Limpiar HTML de la descripción si existe
                    if descripcion:
                        from html.parser import HTMLParser
                        class MLStripper(HTMLParser):
                            def __init__(self):
                                super().__init__()
                                self.reset()
                                self.strict = False
                                self.convert_charrefs= True
                                self.text = []
                            def handle_data(self, d):
                                self.text.append(d)
                            def get_data(self):
                                return ''.join(self.text)
                        
                        try:
                            s = MLStripper()
                            s.feed(descripcion)
                            descripcion = s.get_data().strip()
                        except:
                            pass  # Si falla, usar descripción original
                    
                    link = entry.get('link', '')
                    
                    # Filtrar por términos relacionados con el activo (búsqueda más flexible)
                    texto_completo = f"{titulo} {descripcion}".lower()
                    
                    # Búsqueda más permisiva - al menos un término debe coincidir
                    if any(term.lower() in texto_completo for term in self.search_terms):
                        
                        # Evitar duplicados por título
                        if titulo and not any(n['titulo'] == titulo for n in self.noticias):
                            
                            # Obtener fecha
                            try:
                                if hasattr(entry, 'published_parsed') and entry.published_parsed:
                                    fecha = datetime(*entry.published_parsed[:6])
                                elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                                    fecha = datetime(*entry.updated_parsed[:6])
                                else:
                                    fecha = datetime.now()
                            except:
                                fecha = datetime.now()
                            
                            # Análisis de sentimiento
                            sentimiento = self._analyze_sentiment(f"{titulo}. {descripcion}")
                            
                            self.noticias.append({
                                'titulo': titulo,
                                'descripcion': descripcion[:300],  # Limitar descripción
                                'link': link,
                                'fecha': fecha,
                                'fuente': fuente_nombre,
                                'sentimiento': sentimiento['polaridad'],
                                'sentimiento_label': sentimiento['label'],
                                'subjetividad': sentimiento['subjetividad']
                            })
                            
                            noticias_encontradas += 1
                            
                            if len(self.noticias) >= max_news:
                                break
                
                noticias_por_fuente[fuente_nombre] = noticias_encontradas
                print(f"      ✅ {noticias_encontradas} noticias de {fuente_nombre}")
                
                time.sleep(0.3)  # Evitar sobrecarga de requests
                
            except Exception as e:
                print(f"      ⚠️ Error al obtener noticias de {fuente_nombre}: {str(e)}")
                continue
            
            if len(self.noticias) >= max_news:
                break
        
        # Ordenar por fecha (más recientes primero)
        self.noticias.sort(key=lambda x: x['fecha'], reverse=True)
        
        print(f"\n✅ Total encontrado: {len(self.noticias)} noticias de {len(noticias_por_fuente)} fuentes")
        return self.noticias
    
    def _analyze_sentiment(self, text: str) -> Dict:
        """
        Analiza el sentimiento de un texto
        
        Args:
            text: Texto a analizar
            
        Returns:
            Diccionario con polaridad y subjetividad
        """
        try:
            blob = TextBlob(text)
            polaridad = blob.sentiment.polarity
            subjetividad = blob.sentiment.subjectivity
            
            # Clasificar sentimiento
            if polaridad > 0.1:
                label = "positivo"
            elif polaridad < -0.1:
                label = "negativo"
            else:
                label = "neutral"
            
            return {
                'polaridad': polaridad,
                'subjetividad': subjetividad,
                'label': label
            }
        except:
            return {
                'polaridad': 0,
                'subjetividad': 0,
                'label': 'neutral'
            }
    
    def get_sentiment_summary(self) -> Dict:
        """
        Genera un resumen del sentimiento de las noticias
        
        Returns:
            Diccionario con estadísticas de sentimiento
        """
        if not self.noticias:
            return {
                'total': 0,
                'positivas': 0,
                'negativas': 0,
                'neutrales': 0,
                'sentimiento_promedio': 0,
                'subjetividad_promedio': 0
            }
        
        positivas = sum(1 for n in self.noticias if n['sentimiento'] > 0.1)
        negativas = sum(1 for n in self.noticias if n['sentimiento'] < -0.1)
        neutrales = len(self.noticias) - positivas - negativas
        
        sentimiento_prom = sum(n['sentimiento'] for n in self.noticias) / len(self.noticias)
        subjetividad_prom = sum(n['subjetividad'] for n in self.noticias) / len(self.noticias)
        
        return {
            'total': len(self.noticias),
            'positivas': positivas,
            'negativas': negativas,
            'neutrales': neutrales,
            'sentimiento_promedio': sentimiento_prom,
            'subjetividad_promedio': subjetividad_prom
        }
    
    def get_news_summary(self) -> str:
        """
        Genera un resumen de las noticias encontradas
        
        Returns:
            String formateado con el resumen
        """
        if not self.noticias:
            return "❌ No se encontraron noticias relacionadas"
        
        sentiment = self.get_sentiment_summary()
        
        summary = f"""
╔══════════════════════════════════════════════════════════════╗
║         ANÁLISIS DE NOTICIAS: {self.asset_name.upper()}
╚══════════════════════════════════════════════════════════════╝

📰 RESUMEN DE NOTICIAS:
   • Total de noticias encontradas: {sentiment['total']}
   • Noticias positivas: {sentiment['positivas']} ({sentiment['positivas']/sentiment['total']*100:.1f}%)
   • Noticias negativas: {sentiment['negativas']} ({sentiment['negativas']/sentiment['total']*100:.1f}%)
   • Noticias neutrales: {sentiment['neutrales']} ({sentiment['neutrales']/sentiment['total']*100:.1f}%)

😊 SENTIMIENTO GENERAL:
   • Sentimiento promedio: {sentiment['sentimiento_promedio']:+.3f}
   • Subjetividad promedio: {sentiment['subjetividad_promedio']:.3f}
   • Tendencia: {'POSITIVA ✅' if sentiment['sentimiento_promedio'] > 0.1 else 'NEGATIVA ⚠️' if sentiment['sentimiento_promedio'] < -0.1 else 'NEUTRAL ℹ️'}

📋 ÚLTIMAS NOTICIAS:
"""
        
        # Mostrar las 5 noticias más recientes
        for i, noticia in enumerate(self.noticias[:5], 1):
            emoji = "📈" if noticia['sentimiento'] > 0.1 else "📉" if noticia['sentimiento'] < -0.1 else "➡️"
            fecha_str = noticia['fecha'].strftime("%d/%m/%Y %H:%M")
            
            summary += f"\n{i}. {emoji} [{fecha_str}] {noticia['titulo'][:80]}...\n"
            summary += f"   Sentimiento: {noticia['sentimiento_label'].upper()} ({noticia['sentimiento']:+.2f})\n"
        
        return summary
