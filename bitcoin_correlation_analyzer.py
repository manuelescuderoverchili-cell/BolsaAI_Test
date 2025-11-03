import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta
import yfinance as yf
from textblob import TextBlob
import seaborn as sns
from collections import Counter
import matplotlib.dates as mdates

class BitcoinCorrelationAnalyzer:
    def __init__(self):
        self.datos_precio = None
        self.noticias = None
        self.fecha_hoy = datetime.now().date()
        self.correlaciones = {}
        
    def cargar_datos_precio(self):
        """
        Carga los datos de precio de Bitcoin del día actual
        """
        print("📈 Cargando datos de precio de Bitcoin...")
        
        try:
            bitcoin = yf.Ticker("BTC-USD")
            # Datos intradiarios de hoy con intervalos de 5 minutos
            self.datos_precio = bitcoin.history(period="1d", interval="5m")
            
            if not self.datos_precio.empty:
                print(f"   ✅ Datos de precio cargados: {len(self.datos_precio)} puntos de datos")
                return True
            else:
                print("   ❌ No se pudieron cargar datos de precio")
                return False
                
        except Exception as e:
            print(f"   ❌ Error cargando datos de precio: {e}")
            return False
    
    def cargar_noticias(self):
        """
        Carga las noticias desde el archivo JSON generado por el analizador de noticias
        """
        print("📰 Cargando noticias de Bitcoin...")
        
        try:
            fecha_str = self.fecha_hoy.strftime('%Y%m%d')
            archivo_noticias = f'bitcoin_noticias_{fecha_str}.json'
            
            with open(archivo_noticias, 'r', encoding='utf-8') as f:
                self.noticias = json.load(f)
            
            print(f"   ✅ Noticias cargadas: {len(self.noticias)} noticias")
            return True
            
        except FileNotFoundError:
            print(f"   ❌ No se encontró el archivo {archivo_noticias}")
            print("   💡 Asegúrate de ejecutar primero bitcoin_news_analyzer.py")
            return False
        except Exception as e:
            print(f"   ❌ Error cargando noticias: {e}")
            return False
    
    def preparar_datos_para_analisis(self):
        """
        Prepara y sincroniza los datos de precio y noticias por tiempo
        """
        print("🔄 Preparando datos para análisis temporal...")
        
        # Convertir noticias a DataFrame con timestamps
        noticias_df = []
        for noticia in self.noticias:
            try:
                # Convertir fecha_completa a datetime
                timestamp = datetime.strptime(noticia['fecha_completa'], '%d/%m/%Y %H:%M:%S')
                
                noticias_df.append({
                    'timestamp': timestamp,
                    'titulo': noticia['titulo'],
                    'sentimiento': noticia['sentimiento'],
                    'fuente': noticia['fuente'],
                    'sentimiento_score': self.convertir_sentimiento_a_numero(noticia['sentimiento'])
                })
            except Exception as e:
                print(f"   ⚠️ Error procesando noticia: {e}")
                continue
        
        self.noticias_df = pd.DataFrame(noticias_df)
        
        # Preparar datos de precio
        self.datos_precio.reset_index(inplace=True)
        self.datos_precio['timestamp'] = self.datos_precio['Datetime']
        
        print(f"   ✅ Datos preparados: {len(self.noticias_df)} noticias, {len(self.datos_precio)} puntos de precio")
    
    def convertir_sentimiento_a_numero(self, sentimiento):
        """
        Convierte sentimiento textual a valor numérico para análisis
        """
        conversion = {
            'positivo': 1,
            'neutral': 0,
            'negativo': -1
        }
        return conversion.get(sentimiento, 0)
    
    def analizar_correlacion_temporal(self):
        """
        Analiza la correlación entre noticias y movimientos de precio en diferentes ventanas de tiempo
        """
        print("🔍 Analizando correlaciones temporales...")
        
        # Agrupar noticias por horas
        self.noticias_df['hora'] = self.noticias_df['timestamp'].dt.floor('h')
        noticias_por_hora = self.noticias_df.groupby('hora').agg({
            'sentimiento_score': ['mean', 'count'],
            'titulo': lambda x: list(x)
        }).reset_index()
        
        noticias_por_hora.columns = ['hora', 'sentimiento_promedio', 'cantidad_noticias', 'titulos']
        
        # Agrupar precios por horas (convertir a timezone naive)
        self.datos_precio['timestamp'] = self.datos_precio['timestamp'].dt.tz_localize(None)
        self.datos_precio['hora'] = self.datos_precio['timestamp'].dt.floor('h')
        precios_por_hora = self.datos_precio.groupby('hora').agg({
            'Close': ['first', 'last', 'min', 'max'],
            'Volume': 'sum'
        }).reset_index()
        
        precios_por_hora.columns = ['hora', 'precio_inicio', 'precio_fin', 'precio_min', 'precio_max', 'volumen']
        precios_por_hora['variacion_horaria'] = ((precios_por_hora['precio_fin'] - precios_por_hora['precio_inicio']) / precios_por_hora['precio_inicio']) * 100
        
        # Combinar datos
        self.datos_combinados = pd.merge(precios_por_hora, noticias_por_hora, on='hora', how='outer')
        self.datos_combinados.fillna(0, inplace=True)
        
        # Calcular correlaciones
        if len(self.datos_combinados) > 1:
            correlacion_sentimiento_precio = np.corrcoef(
                self.datos_combinados['sentimiento_promedio'].fillna(0),
                self.datos_combinados['variacion_horaria'].fillna(0)
            )[0, 1]
            
            correlacion_cantidad_volumen = np.corrcoef(
                self.datos_combinados['cantidad_noticias'].fillna(0),
                self.datos_combinados['volumen'].fillna(0)
            )[0, 1]
            
            self.correlaciones = {
                'sentimiento_precio': correlacion_sentimiento_precio,
                'cantidad_volumen': correlacion_cantidad_volumen
            }
            
            print(f"   📊 Correlación sentimiento-precio: {correlacion_sentimiento_precio:.3f}")
            print(f"   📊 Correlación cantidad noticias-volumen: {correlacion_cantidad_volumen:.3f}")
        
    def identificar_eventos_significativos(self):
        """
        Identifica momentos donde hay grandes movimientos de precio y alta actividad noticiosa
        """
        print("🎯 Identificando eventos significativos...")
        
        # Calcular percentiles para identificar eventos extremos
        umbral_precio = np.percentile(np.abs(self.datos_combinados['variacion_horaria']), 75)
        umbral_noticias = np.percentile(self.datos_combinados['cantidad_noticias'], 75)
        
        # Encontrar eventos significativos
        eventos = self.datos_combinados[
            (np.abs(self.datos_combinados['variacion_horaria']) > umbral_precio) |
            (self.datos_combinados['cantidad_noticias'] > umbral_noticias)
        ].copy()
        
        if not eventos.empty:
            eventos['tipo_evento'] = eventos.apply(self.clasificar_evento, axis=1)
            self.eventos_significativos = eventos.sort_values('hora')
            
            print(f"   ✅ Encontrados {len(self.eventos_significativos)} eventos significativos")
        else:
            self.eventos_significativos = pd.DataFrame()
            print("   ℹ️ No se encontraron eventos significativos")
    
    def clasificar_evento(self, row):
        """
        Clasifica el tipo de evento basado en precio y noticias
        """
        precio_alto = abs(row['variacion_horaria']) > np.percentile(np.abs(self.datos_combinados['variacion_horaria']), 75)
        noticias_altas = row['cantidad_noticias'] > np.percentile(self.datos_combinados['cantidad_noticias'], 75)
        
        if precio_alto and noticias_altas:
            if row['variacion_horaria'] > 0 and row['sentimiento_promedio'] > 0:
                return "📈 Subida con noticias positivas"
            elif row['variacion_horaria'] < 0 and row['sentimiento_promedio'] < 0:
                return "📉 Bajada con noticias negativas"
            elif row['variacion_horaria'] > 0 and row['sentimiento_promedio'] < 0:
                return "⚡ Subida a pesar de noticias negativas"
            elif row['variacion_horaria'] < 0 and row['sentimiento_promedio'] > 0:
                return "🔄 Bajada a pesar de noticias positivas"
            else:
                return "📊 Movimiento con noticias neutrales"
        elif precio_alto:
            return "💹 Movimiento sin noticias relevantes"
        elif noticias_altas:
            return "📢 Muchas noticias sin movimiento significativo"
        else:
            return "📊 Evento menor"
    
    def generar_visualizaciones(self):
        """
        Genera gráficos que muestran la correlación entre precio y noticias
        """
        print("📊 Generando visualizaciones...")
        
        # Configurar el estilo
        plt.style.use('seaborn-v0_8')
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        
        # Gráfico 1: Precio vs Sentimiento por hora
        if not self.datos_combinados.empty:
            horas = self.datos_combinados['hora']
            
            # Precio
            ax1.plot(horas, self.datos_combinados['variacion_horaria'], 
                    color='orange', linewidth=2, label='Variación precio (%)')
            ax1_twin = ax1.twinx()
            ax1_twin.bar(horas, self.datos_combinados['sentimiento_promedio'], 
                        alpha=0.6, color='blue', label='Sentimiento promedio', width=0.03)
            
            ax1.set_title('Variación de Precio vs Sentimiento de Noticias', fontweight='bold')
            ax1.set_ylabel('Variación precio (%)', color='orange')
            ax1_twin.set_ylabel('Sentimiento promedio', color='blue')
            ax1.tick_params(axis='x', rotation=45)
            
            # Gráfico 2: Volumen vs Cantidad de noticias
            ax2.bar(horas, self.datos_combinados['volumen']/1e9, 
                   alpha=0.6, color='purple', label='Volumen (B)')
            ax2_twin = ax2.twinx()
            ax2_twin.plot(horas, self.datos_combinados['cantidad_noticias'], 
                         color='red', marker='o', label='Cantidad noticias')
            
            ax2.set_title('Volumen vs Cantidad de Noticias', fontweight='bold')
            ax2.set_ylabel('Volumen (Miles de millones)', color='purple')
            ax2_twin.set_ylabel('Cantidad de noticias', color='red')
            ax2.tick_params(axis='x', rotation=45)
        
        # Gráfico 3: Distribución de sentimientos
        if not self.noticias_df.empty:
            sentimientos = self.noticias_df['sentimiento'].value_counts()
            colors = {'positivo': 'green', 'negativo': 'red', 'neutral': 'gray'}
            ax3.pie(sentimientos.values, labels=sentimientos.index, autopct='%1.1f%%',
                   colors=[colors.get(sent, 'gray') for sent in sentimientos.index])
            ax3.set_title('Distribución de Sentimientos en Noticias', fontweight='bold')
        
        # Gráfico 4: Correlación scatter
        if not self.datos_combinados.empty and len(self.datos_combinados) > 1:
            scatter = ax4.scatter(self.datos_combinados['sentimiento_promedio'], 
                                self.datos_combinados['variacion_horaria'],
                                s=self.datos_combinados['cantidad_noticias']*50,
                                alpha=0.6, c=self.datos_combinados['volumen'], 
                                cmap='viridis')
            ax4.set_xlabel('Sentimiento promedio')
            ax4.set_ylabel('Variación precio (%)')
            ax4.set_title('Correlación: Sentimiento vs Variación de Precio', fontweight='bold')
            plt.colorbar(scatter, ax=ax4, label='Volumen')
        
        plt.tight_layout()
        
        # Guardar gráfico
        fecha_str = self.fecha_hoy.strftime('%Y%m%d')
        nombre_archivo = f"bitcoin_correlacion_{fecha_str}.png"
        plt.savefig(nombre_archivo, dpi=300, bbox_inches='tight')
        print(f"   💾 Gráfico guardado: {nombre_archivo}")
        
        plt.show()
    
    def generar_reporte_final(self):
        """
        Genera un reporte final con conclusiones del análisis
        """
        print("\n" + "="*80)
        print(f"📋 REPORTE DE CORRELACIÓN BITCOIN - {self.fecha_hoy.strftime('%d/%m/%Y')}")
        print("="*80)
        
        # Estadísticas generales
        if self.datos_precio is not None and not self.datos_precio.empty:
            precio_inicial = self.datos_precio['Close'].iloc[0]
            precio_final = self.datos_precio['Close'].iloc[-1]
            variacion_total = ((precio_final - precio_inicial) / precio_inicial) * 100
            
            print(f"💰 RESUMEN DE PRECIOS:")
            print(f"   • Precio inicial: ${precio_inicial:,.2f}")
            print(f"   • Precio final: ${precio_final:,.2f}")
            print(f"   • Variación total del día: {variacion_total:+.2f}%")
            print(f"   • Volatilidad (std): {self.datos_precio['Close'].pct_change().std()*100:.2f}%")
        
        if self.noticias is not None:
            sentimientos = Counter([n['sentimiento'] for n in self.noticias])
            print(f"\n📰 RESUMEN DE NOTICIAS:")
            print(f"   • Total de noticias: {len(self.noticias)}")
            print(f"   • Positivas: {sentimientos['positivo']} ({sentimientos['positivo']/len(self.noticias)*100:.1f}%)")
            print(f"   • Negativas: {sentimientos['negativo']} ({sentimientos['negativo']/len(self.noticias)*100:.1f}%)")
            print(f"   • Neutrales: {sentimientos['neutral']} ({sentimientos['neutral']/len(self.noticias)*100:.1f}%)")
        
        # Correlaciones
        if self.correlaciones:
            print(f"\n🔗 ANÁLISIS DE CORRELACIONES:")
            corr_sent = self.correlaciones['sentimiento_precio']
            corr_vol = self.correlaciones['cantidad_volumen']
            
            print(f"   • Correlación sentimiento-precio: {corr_sent:.3f}")
            if abs(corr_sent) > 0.3:
                print(f"     → {'Correlación FUERTE' if abs(corr_sent) > 0.5 else 'Correlación MODERADA'}")
            else:
                print(f"     → Correlación DÉBIL")
            
            print(f"   • Correlación noticias-volumen: {corr_vol:.3f}")
            if abs(corr_vol) > 0.3:
                print(f"     → {'Correlación FUERTE' if abs(corr_vol) > 0.5 else 'Correlación MODERADA'}")
            else:
                print(f"     → Correlación DÉBIL")
        
        # Eventos significativos
        if hasattr(self, 'eventos_significativos') and not self.eventos_significativos.empty:
            print(f"\n🎯 EVENTOS SIGNIFICATIVOS:")
            for idx, evento in self.eventos_significativos.iterrows():
                print(f"   • {evento['hora'].strftime('%H:%M')} - {evento['tipo_evento']}")
                print(f"     Variación: {evento['variacion_horaria']:+.2f}% | Noticias: {evento['cantidad_noticias']}")
        
        # Conclusiones
        print(f"\n🎯 CONCLUSIONES:")
        
        if self.correlaciones:
            if abs(self.correlaciones['sentimiento_precio']) > 0.3:
                if self.correlaciones['sentimiento_precio'] > 0:
                    print("   ✅ Las noticias positivas tienden a correlacionarse con subidas de precio")
                else:
                    print("   ⚠️ Hay una correlación inversa entre sentimiento y precio (contraintuitivo)")
            else:
                print("   📊 No hay una correlación fuerte entre sentimiento de noticias y precio")
        
        if hasattr(self, 'eventos_significativos') and not self.eventos_significativos.empty:
            coincidencias = len(self.eventos_significativos[
                self.eventos_significativos['tipo_evento'].str.contains('positivas|negativas')
            ])
            total_eventos = len(self.eventos_significativos)
            
            if coincidencias / total_eventos > 0.5:
                print("   ✅ La mayoría de movimientos significativos coinciden con el sentimiento de las noticias")
            else:
                print("   ⚠️ Los movimientos de precio no siempre coinciden con el sentimiento de las noticias")
        
        print("\n" + "="*80)
    
    def ejecutar_analisis_completo(self):
        """
        Ejecuta el análisis completo de correlación
        """
        print("🚀 Iniciando análisis de correlación Bitcoin...")
        
        # Cargar datos
        if not self.cargar_datos_precio():
            return False
        
        if not self.cargar_noticias():
            return False
        
        # Procesar y analizar
        self.preparar_datos_para_analisis()
        self.analizar_correlacion_temporal()
        self.identificar_eventos_significativos()
        self.generar_visualizaciones()
        self.generar_reporte_final()
        
        print("\n✅ Análisis de correlación completado!")
        return True

def main():
    analyzer = BitcoinCorrelationAnalyzer()
    analyzer.ejecutar_analisis_completo()

if __name__ == "__main__":
    main()