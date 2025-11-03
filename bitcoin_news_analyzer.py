import requests
import feedparser
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import json
import re
from textblob import TextBlob
import time
import pandas as pd

class BitcoinNewsAnalyzer:
    def __init__(self):
        self.noticias = []
        self.fecha_hoy = datetime.now().date()
        
        # Headers para las requests
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # Fuentes de noticias
        self.fuentes = {
            'coindesk': 'https://www.coindesk.com/arc/outboundfeeds/rss/',
            'cointelegraph': 'https://cointelegraph.com/rss',
            'bitcoin_news': 'https://www.newsbtc.com/feed/',
            'decrypt': 'https://decrypt.co/feed',
            'bitcoinist': 'https://bitcoinist.com/feed/'
        }
    
    def obtener_noticias_rss(self):
        """
        Obtiene noticias de feeds RSS de diferentes fuentes
        """
        print("📡 Obteniendo noticias desde feeds RSS...")
        
        for fuente, url in self.fuentes.items():
            try:
                print(f"   • Procesando {fuente}...")
                feed = feedparser.parse(url)
                
                for entry in feed.entries:
                    # Verificar si la noticia es de hoy
                    fecha_hora_noticia = None
                    if hasattr(entry, 'published_parsed'):
                        fecha_hora_noticia = datetime(*entry.published_parsed[:6])
                    elif hasattr(entry, 'updated_parsed'):
                        fecha_hora_noticia = datetime(*entry.updated_parsed[:6])
                    else:
                        continue
                    
                    fecha_noticia = fecha_hora_noticia.date()
                    
                    # Solo noticias de hoy que mencionen Bitcoin
                    if (fecha_noticia == self.fecha_hoy and 
                        self.contiene_bitcoin(entry.title + ' ' + getattr(entry, 'summary', ''))):
                        
                        noticia = {
                            'titulo': entry.title,
                            'descripcion': getattr(entry, 'summary', ''),
                            'url': entry.link,
                            'fuente': fuente,
                            'fecha': fecha_noticia.strftime('%d/%m/%Y'),
                            'hora': fecha_hora_noticia.strftime('%H:%M:%S'),
                            'fecha_completa': fecha_hora_noticia.strftime('%d/%m/%Y %H:%M:%S'),
                            'sentimiento': self.analizar_sentimiento(entry.title + ' ' + getattr(entry, 'summary', ''))
                        }
                        self.noticias.append(noticia)
                
                time.sleep(1)  # Pausa entre requests
                
            except Exception as e:
                print(f"   ❌ Error procesando {fuente}: {e}")
    
    def obtener_noticias_twitter_api(self):
        """
        Simula obtener noticias de Twitter/X (requeriría API keys reales)
        """
        print("🐦 Simulando búsqueda en Twitter/X...")
        
        # En un entorno real, aquí usarías la API de Twitter
        # Por ahora, agregamos algunas noticias simuladas
        hora_actual = datetime.now()
        noticias_simuladas = [
            {
                'titulo': 'Bitcoin alcanza nuevo máximo intradía',
                'descripcion': 'El precio de Bitcoin ha mostrado un comportamiento alcista durante la sesión de hoy',
                'url': 'https://twitter.com/ejemplo',
                'fuente': 'twitter_simulado',
                'fecha': self.fecha_hoy.strftime('%d/%m/%Y'),
                'hora': hora_actual.strftime('%H:%M:%S'),
                'fecha_completa': hora_actual.strftime('%d/%m/%Y %H:%M:%S'),
                'sentimiento': 'positivo'
            }
        ]
        
        self.noticias.extend(noticias_simuladas)
        print("   • Noticias simuladas agregadas")
    
    def obtener_noticias_reddit(self):
        """
        Obtiene noticias relevantes de Reddit
        """
        print("📱 Buscando en Reddit...")
        
        try:
            # Reddit API sin autenticación (limitado pero funcional)
            subreddits = ['Bitcoin', 'CryptoCurrency', 'btc']
            
            for subreddit in subreddits:
                url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit=10"
                
                try:
                    response = requests.get(url, headers=self.headers)
                    if response.status_code == 200:
                        data = response.json()
                        
                        for post in data['data']['children']:
                            post_data = post['data']
                            
                            # Verificar si es de hoy
                            fecha_hora_post = datetime.fromtimestamp(post_data['created_utc'])
                            fecha_post = fecha_hora_post.date()
                            
                            if (fecha_post == self.fecha_hoy and 
                                self.contiene_bitcoin(post_data['title'] + ' ' + post_data.get('selftext', ''))):
                                
                                noticia = {
                                    'titulo': post_data['title'],
                                    'descripcion': post_data.get('selftext', '')[:200] + '...',
                                    'url': f"https://reddit.com{post_data['permalink']}",
                                    'fuente': f'reddit_r_{subreddit}',
                                    'fecha': fecha_post.strftime('%d/%m/%Y'),
                                    'hora': fecha_hora_post.strftime('%H:%M:%S'),
                                    'fecha_completa': fecha_hora_post.strftime('%d/%m/%Y %H:%M:%S'),
                                    'sentimiento': self.analizar_sentimiento(post_data['title'])
                                }
                                self.noticias.append(noticia)
                    
                    time.sleep(1)
                    
                except Exception as e:
                    print(f"   ❌ Error en subreddit {subreddit}: {e}")
                    
        except Exception as e:
            print(f"   ❌ Error general en Reddit: {e}")
    
    def contiene_bitcoin(self, texto):
        """
        Verifica si el texto contiene referencias a Bitcoin
        """
        palabras_clave = ['bitcoin', 'btc', 'crypto', 'cryptocurrency', 'blockchain']
        texto_lower = texto.lower()
        return any(palabra in texto_lower for palabra in palabras_clave)
    
    def analizar_sentimiento(self, texto):
        """
        Analiza el sentimiento del texto usando TextBlob
        """
        try:
            blob = TextBlob(texto)
            polaridad = blob.sentiment.polarity
            
            if polaridad > 0.1:
                return 'positivo'
            elif polaridad < -0.1:
                return 'negativo'
            else:
                return 'neutral'
        except:
            return 'neutral'
    
    def filtrar_duplicados(self):
        """
        Elimina noticias duplicadas basándose en títulos similares
        """
        noticias_unicas = []
        titulos_vistos = set()
        
        for noticia in self.noticias:
            # Crear una versión simplificada del título para comparar
            titulo_simple = re.sub(r'[^\w\s]', '', noticia['titulo'].lower())
            titulo_simple = ' '.join(titulo_simple.split()[:5])  # Primeras 5 palabras
            
            if titulo_simple not in titulos_vistos:
                titulos_vistos.add(titulo_simple)
                noticias_unicas.append(noticia)
        
        self.noticias = noticias_unicas
        print(f"🔄 Eliminados duplicados. Noticias únicas: {len(self.noticias)}")
    
    def generar_resumen(self):
        """
        Genera un resumen del análisis de noticias
        """
        if not self.noticias:
            print("❌ No se encontraron noticias de Bitcoin para hoy")
            return
        
        # Contar sentimientos
        sentimientos = {'positivo': 0, 'negativo': 0, 'neutral': 0}
        fuentes_count = {}
        
        for noticia in self.noticias:
            sentimientos[noticia['sentimiento']] += 1
            fuente = noticia['fuente']
            fuentes_count[fuente] = fuentes_count.get(fuente, 0) + 1
        
        # Mostrar resumen
        print("\n" + "="*70)
        print(f"📊 RESUMEN DE NOTICIAS DE BITCOIN - {self.fecha_hoy.strftime('%d/%m/%Y')}")
        print("="*70)
        print(f"Total de noticias encontradas: {len(self.noticias)}")
        print(f"Sentimiento general:")
        print(f"  • Positivas: {sentimientos['positivo']} ({sentimientos['positivo']/len(self.noticias)*100:.1f}%)")
        print(f"  • Negativas: {sentimientos['negativo']} ({sentimientos['negativo']/len(self.noticias)*100:.1f}%)")
        print(f"  • Neutrales: {sentimientos['neutral']} ({sentimientos['neutral']/len(self.noticias)*100:.1f}%)")
        
        print(f"\nFuentes de información:")
        for fuente, count in sorted(fuentes_count.items(), key=lambda x: x[1], reverse=True):
            print(f"  • {fuente}: {count} noticias")
    
    def mostrar_noticias(self, limite=10):
        """
        Muestra las noticias encontradas
        """
        if not self.noticias:
            return
        
        print(f"\n📰 NOTICIAS DE BITCOIN DEL DÍA (Mostrando {min(limite, len(self.noticias))} de {len(self.noticias)})")
        print("="*70)
        
        # Ordenar por fuente y sentimiento
        noticias_ordenadas = sorted(self.noticias, key=lambda x: (x['sentimiento'], x['fecha_completa']))
        
        for i, noticia in enumerate(noticias_ordenadas[:limite], 1):
            emoji_sentimiento = {'positivo': '📈', 'negativo': '📉', 'neutral': '📊'}
            
            print(f"\n{i}. {emoji_sentimiento[noticia['sentimiento']]} {noticia['titulo']}")
            print(f"   🏷️  Fuente: {noticia['fuente']}")
            print(f"   🕒 Fecha y hora: {noticia['fecha_completa']}")
            print(f"   📝 {noticia['descripcion'][:150]}...")
            print(f"   🔗 {noticia['url']}")
            print(f"   💭 Sentimiento: {noticia['sentimiento']}")
    
    def guardar_resultados(self):
        """
        Guarda los resultados en un archivo JSON y CSV
        """
        if not self.noticias:
            return
        
        fecha_str = self.fecha_hoy.strftime('%Y%m%d')
        
        # Guardar en JSON
        with open(f'bitcoin_noticias_{fecha_str}.json', 'w', encoding='utf-8') as f:
            json.dump(self.noticias, f, ensure_ascii=False, indent=2, default=str)
        
        # Guardar en CSV
        df = pd.DataFrame(self.noticias)
        df.to_csv(f'bitcoin_noticias_{fecha_str}.csv', index=False, encoding='utf-8')
        
        print(f"\n💾 Resultados guardados:")
        print(f"   • bitcoin_noticias_{fecha_str}.json")
        print(f"   • bitcoin_noticias_{fecha_str}.csv")
    
    def ejecutar_analisis_completo(self):
        """
        Ejecuta el análisis completo de noticias
        """
        print("🚀 Iniciando análisis de noticias de Bitcoin...")
        print(f"📅 Fecha de análisis: {self.fecha_hoy.strftime('%d/%m/%Y')}")
        
        # Obtener noticias de diferentes fuentes
        self.obtener_noticias_rss()
        self.obtener_noticias_twitter_api()
        self.obtener_noticias_reddit()
        
        # Procesar resultados
        self.filtrar_duplicados()
        self.generar_resumen()
        self.mostrar_noticias()
        self.guardar_resultados()
        
        print("\n✅ Análisis de noticias completado!")

def main():
    analyzer = BitcoinNewsAnalyzer()
    analyzer.ejecutar_analisis_completo()

if __name__ == "__main__":
    main()