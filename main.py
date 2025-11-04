"""
Aplicación de Análisis de Mercados Financieros
Interfaz gráfica con CustomTkinter
"""
import customtkinter as ctk
from tkinter import messagebox, scrolledtext
import threading
from datetime import datetime
import os
import sys

# Añadir el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from market_analyzer import MarketAnalyzer
from news_analyzer import NewsAnalyzer
from visualizer import Visualizer
from pattern_analyzer import TechnicalPatternAnalyzer
from report_generator import ReportGenerator
from predictive_analyzer import PredictiveAnalyzer
from advanced_visualizer import AdvancedVisualizer
from pdf_report_generator import PDFReportGenerator
from comparative_analyzer import ComparativeAnalyzer
from asset_discovery import AssetDiscovery


class MarketAnalysisApp:
    """Aplicación principal de análisis de mercados"""
    
    def __init__(self):
        # Cargar activos guardados
        MarketAnalyzer.load_assets_from_file()
        
        # Configurar tema
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Crear ventana principal
        self.root = ctk.CTk()
        self.root.title("📊 Análisis de Mercados Financieros")
        self.root.geometry("1200x800")
        
        # Variables
        self.analyzing = False
        
        # Crear interfaz
        self.create_widgets()
        
    def create_widgets(self):
        """Crea todos los widgets de la interfaz"""
        
        # ============ PANEL IZQUIERDO (Controles) ============
        left_panel = ctk.CTkFrame(self.root, width=300, corner_radius=10)
        left_panel.pack(side="left", fill="both", padx=10, pady=10)
        left_panel.pack_propagate(False)
        
        # Título
        title = ctk.CTkLabel(left_panel, text="📊 Market Analyzer", 
                            font=ctk.CTkFont(size=24, weight="bold"))
        title.pack(pady=20, padx=20)
        
        # Separador
        separator1 = ctk.CTkFrame(left_panel, height=2, fg_color="gray")
        separator1.pack(fill="x", padx=20, pady=10)
        
        # Selector de Activo
        label_asset = ctk.CTkLabel(left_panel, text="Selecciona el Activo:", 
                                   font=ctk.CTkFont(size=14, weight="bold"))
        label_asset.pack(pady=(10, 5), padx=20, anchor="w")
        
        self.asset_var = ctk.StringVar(value="Bitcoin")
        asset_menu = ctk.CTkOptionMenu(
            left_panel,
            variable=self.asset_var,
            values=list(MarketAnalyzer.ASSETS.keys()),
            width=260,
            height=35,
            font=ctk.CTkFont(size=12)
        )
        asset_menu.pack(pady=5, padx=20)
        
        # Selector de Periodo
        label_period = ctk.CTkLabel(left_panel, text="Periodo de Tiempo:", 
                                    font=ctk.CTkFont(size=14, weight="bold"))
        label_period.pack(pady=(20, 5), padx=20, anchor="w")
        
        self.period_var = ctk.StringVar(value="1 mes")
        period_menu = ctk.CTkOptionMenu(
            left_panel,
            variable=self.period_var,
            values=["1 día", "5 días", "1 mes", "3 meses", "6 meses", "1 año", "2 años", "5 años"],
            width=260,
            height=35,
            font=ctk.CTkFont(size=12)
        )
        period_menu.pack(pady=5, padx=20)
        
        # Selector de Intervalo
        label_interval = ctk.CTkLabel(left_panel, text="Intervalo de Datos:", 
                                      font=ctk.CTkFont(size=14, weight="bold"))
        label_interval.pack(pady=(20, 5), padx=20, anchor="w")
        
        self.interval_var = ctk.StringVar(value="1 día")
        interval_menu = ctk.CTkOptionMenu(
            left_panel,
            variable=self.interval_var,
            values=["1 minuto", "5 minutos", "15 minutos", "1 hora", "1 día", "1 semana"],
            width=260,
            height=35,
            font=ctk.CTkFont(size=12),
            command=self.update_data_warning
        )
        interval_menu.pack(pady=5, padx=20)
        
        # Label de advertencia sobre limitaciones de datos
        self.warning_label = ctk.CTkLabel(
            left_panel, 
            text="", 
            font=ctk.CTkFont(size=10),
            text_color="#ff9800",
            wraplength=240
        )
        self.warning_label.pack(pady=5, padx=20)
        self.update_data_warning()  # Actualizar advertencia inicial
        
        # Separador
        separator2 = ctk.CTkFrame(left_panel, height=2, fg_color="gray")
        separator2.pack(fill="x", padx=20, pady=20)
        
        # Opciones de análisis
        label_options = ctk.CTkLabel(left_panel, text="Opciones de Análisis:", 
                                     font=ctk.CTkFont(size=14, weight="bold"))
        label_options.pack(pady=(10, 5), padx=20, anchor="w")
        
        self.include_news = ctk.CTkCheckBox(left_panel, text="Incluir análisis de noticias",
                                           font=ctk.CTkFont(size=12))
        self.include_news.pack(pady=5, padx=20, anchor="w")
        self.include_news.select()
        
        self.save_graphs = ctk.CTkCheckBox(left_panel, text="Guardar gráficos",
                                          font=ctk.CTkFont(size=12))
        self.save_graphs.pack(pady=5, padx=20, anchor="w")
        self.save_graphs.select()
        
        # Botón de Análisis
        self.analyze_button = ctk.CTkButton(
            left_panel,
            text="🚀 Iniciar Análisis",
            command=self.start_analysis,
            width=260,
            height=45,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#28a745",
            hover_color="#218838"
        )
        self.analyze_button.pack(pady=20, padx=20)
        
        # Botón de Análisis Comparativo
        self.compare_button = ctk.CTkButton(
            left_panel,
            text="📊 Comparar TODOS los Activos",
            command=self.start_comparative_analysis,
            width=260,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#007bff",
            hover_color="#0056b3"
        )
        self.compare_button.pack(pady=10, padx=20)
        
        # Botón de Descubrimiento de Activos
        self.discovery_button = ctk.CTkButton(
            left_panel,
            text="🔍 Descubrir Nuevos Activos",
            command=self.start_asset_discovery,
            width=260,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#28a745",
            hover_color="#1e7e34"
        )
        self.discovery_button.pack(pady=10, padx=20)
        
        # Barra de progreso
        self.progress = ctk.CTkProgressBar(left_panel, width=260)
        self.progress.pack(pady=10, padx=20)
        self.progress.set(0)
        
        # Estado
        self.status_label = ctk.CTkLabel(left_panel, text="Listo", 
                                        font=ctk.CTkFont(size=11),
                                        text_color="gray")
        self.status_label.pack(pady=5, padx=20)
        
        # ============ PANEL DERECHO (Resultados) ============
        right_panel = ctk.CTkFrame(self.root, corner_radius=10)
        right_panel.pack(side="right", fill="both", expand=True, padx=(0, 10), pady=10)
        
        # Título del panel
        results_title = ctk.CTkLabel(right_panel, text="📈 Resultados del Análisis", 
                                    font=ctk.CTkFont(size=20, weight="bold"))
        results_title.pack(pady=15, padx=20)
        
        # Área de texto para resultados
        self.results_text = ctk.CTkTextbox(right_panel, 
                                          font=ctk.CTkFont(family="Consolas", size=11),
                                          wrap="word")
        self.results_text.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Mensaje inicial
        welcome_message = """
╔══════════════════════════════════════════════════════════════╗
║     BIENVENIDO AL ANALIZADOR DE MERCADOS FINANCIEROS        ║
╚══════════════════════════════════════════════════════════════╝

🎯 INSTRUCCIONES:

1. Selecciona el activo que deseas analizar (Bitcoin, Tesla, etc.)
2. Elige el periodo de tiempo (desde 1 día hasta 5 años)
3. Selecciona el intervalo de datos deseado
4. Marca las opciones de análisis que necesites
5. Haz clic en "Iniciar Análisis"

📊 ANÁLISIS INCLUIDOS:

✅ Análisis técnico completo del precio
✅ Cálculo de indicadores (SMA, RSI, soportes/resistencias)
✅ Detección de tendencias y patrones
✅ Análisis de volumen de transacciones
✅ Análisis de sentimiento de noticias (opcional)
✅ Generación de gráficos profesionales

📁 ARCHIVOS GENERADOS:

• Los gráficos se guardarán en: outputs/graphs/
• Los reportes se guardarán en: outputs/reports/

¡Listo para comenzar! Selecciona tus opciones y presiona el botón.
        """
        self.results_text.insert("1.0", welcome_message)
        self.results_text.configure(state="disabled")
    
    def update_data_warning(self, *args):
        """Actualiza la advertencia sobre limitaciones de datos según intervalo seleccionado"""
        interval = self.interval_var.get()
        
        warnings = {
            "1 minuto": "⚠️ Intervalo de 1m: Máximo 7 días de datos disponibles",
            "5 minutos": "⚠️ Intervalo de 5m: Máximo 7 días de datos disponibles",
            "15 minutos": "⚠️ Intervalo de 15m: Máximo 60 días de datos disponibles",
            "1 hora": "⚠️ Intervalo de 1h: Máximo 730 días de datos disponibles",
            "1 día": "",
            "1 semana": ""
        }
        
        warning_text = warnings.get(interval, "")
        self.warning_label.configure(text=warning_text)
    
    def get_period_code(self) -> str:
        """Convierte el periodo seleccionado al código de yfinance"""
        period_map = {
            "1 día": "1d",
            "5 días": "5d",
            "1 mes": "1mo",
            "3 meses": "3mo",
            "6 meses": "6mo",
            "1 año": "1y",
            "2 años": "2y",
            "5 años": "5y"
        }
        return period_map.get(self.period_var.get(), "1mo")
    
    def get_interval_code(self) -> str:
        """Convierte el intervalo seleccionado al código de yfinance"""
        interval_map = {
            "1 minuto": "1m",
            "5 minutos": "5m",
            "15 minutos": "15m",
            "1 hora": "1h",
            "1 día": "1d",
            "1 semana": "1wk"
        }
        return interval_map.get(self.interval_var.get(), "1d")
    
    def update_status(self, message: str, progress: float = None):
        """Actualiza el mensaje de estado y la barra de progreso"""
        self.status_label.configure(text=message)
        if progress is not None:
            self.progress.set(progress)
        self.root.update()
    
    def append_results(self, text: str):
        """Añade texto al área de resultados"""
        self.results_text.configure(state="normal")
        self.results_text.insert("end", text + "\n")
        self.results_text.see("end")
        self.results_text.configure(state="disabled")
        self.root.update()
    
    def clear_results(self):
        """Limpia el área de resultados"""
        self.results_text.configure(state="normal")
        self.results_text.delete("1.0", "end")
        self.results_text.configure(state="disabled")
    
    def start_analysis(self):
        """Inicia el análisis en un thread separado"""
        if self.analyzing:
            messagebox.showwarning("Análisis en curso", 
                                 "Ya hay un análisis en progreso. Por favor espera.")
            return
        
        # Iniciar en un thread separado para no bloquear la UI
        thread = threading.Thread(target=self.perform_analysis, daemon=True)
        thread.start()
    
    def perform_analysis(self):
        """Realiza el análisis completo"""
        try:
            self.analyzing = True
            self.analyze_button.configure(state="disabled", text="⏳ Analizando...")
            
            # Limpiar resultados anteriores
            self.clear_results()
            
            # Obtener parámetros
            asset_name = self.asset_var.get()
            period = self.get_period_code()
            interval = self.get_interval_code()
            
            self.update_status(f"Iniciando análisis de {asset_name}...", 0.1)
            
            # Header
            header = f"""
╔══════════════════════════════════════════════════════════════╗
║  ANÁLISIS COMPLETO - {asset_name.upper()}
║  Fecha: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}
║  Periodo: {self.period_var.get()} | Intervalo: {self.interval_var.get()}
╚══════════════════════════════════════════════════════════════╝
"""
            self.append_results(header)
            
            # ============ ANÁLISIS DE MERCADO ============
            self.update_status("Obteniendo datos del mercado...", 0.2)
            self.append_results("\n⏳ Descargando datos históricos...")
            
            analyzer = MarketAnalyzer(asset_name)
            data = analyzer.get_data(period=period, interval=interval)
            
            self.append_results(f"✅ Datos obtenidos: {len(data)} registros")
            
            self.update_status("Calculando estadísticas...", 0.4)
            self.append_results("\n⏳ Calculando estadísticas y tendencias...")
            
            stats = analyzer.calculate_statistics()
            trends = analyzer.detect_trends()
            summary = analyzer.get_summary()
            
            self.append_results(summary)
            
            # ============ ANÁLISIS DE PATRONES TÉCNICOS ============
            self.update_status("Detectando patrones técnicos...", 0.5)
            self.append_results("\n\n⏳ Analizando patrones de velas, gráficos y tendencias...")
            
            pattern_analyzer = TechnicalPatternAnalyzer(data)
            patterns = pattern_analyzer.analyze_all_patterns()
            pattern_report = pattern_analyzer.generate_pattern_report(patterns)
            
            self.append_results(pattern_report)
            
            # ============ ANÁLISIS DE NOTICIAS ============
            noticias = []
            news_analyzer = None
            if self.include_news.get():
                self.update_status("Analizando noticias...", 0.6)
                self.append_results("\n\n⏳ Buscando y analizando noticias relacionadas...")
                
                news_analyzer = NewsAnalyzer(asset_name)
                noticias = news_analyzer.fetch_news(max_news=50)  # Aumentado a 50 noticias
                
                if noticias:
                    news_summary = news_analyzer.get_news_summary()
                    self.append_results(news_summary)
                else:
                    self.append_results("\n⚠️ No se encontraron noticias recientes")
            
            # ============ ANÁLISIS PREDICTIVO ============
            self.update_status("Generando predicciones basadas en patrones...", 0.7)
            self.append_results("\n\n⏳ Analizando efectividad de patrones y generando predicciones...")
            
            predictive_analyzer = PredictiveAnalyzer(data, patterns)
            effectiveness = predictive_analyzer.analyze_pattern_effectiveness()
            prediction_report, predictions = predictive_analyzer.generate_prediction_report()
            
            self.append_results(prediction_report)
            
            # ============ GENERAR GRÁFICOS AVANZADOS CON PATRONES MARCADOS ============
            graph_paths = []
            if self.save_graphs.get():
                self.update_status("Generando gráficos avanzados...", 0.8)
                self.append_results("\n\n⏳ Generando visualizaciones con patrones marcados...")
                
                advanced_visualizer = AdvancedVisualizer()
                
                # Gráfico principal con patrones marcados y predicciones
                main_graph_path = advanced_visualizer.plot_patterns_marked(
                    data, asset_name, patterns, predictions
                )
                graph_paths.append(main_graph_path)
                self.append_results(f"\n✅ Gráfico con patrones marcados: {main_graph_path}")
                
                # Gráfico de escenarios de predicción
                scenarios_path = advanced_visualizer.plot_prediction_scenarios(
                    data, asset_name, predictions
                )
                graph_paths.append(scenarios_path)
                self.append_results(f"✅ Gráfico de escenarios: {scenarios_path}")
                
                # También generar gráficos tradicionales
                visualizer = Visualizer()
                
                # Gráfico de velas
                candlestick_path = visualizer.plot_candlestick(data, asset_name)
                graph_paths.append(candlestick_path)
                self.append_results(f"✅ Gráfico de velas guardado: {candlestick_path}")
                
                # Gráfico de sentimiento de noticias
                if self.include_news.get() and noticias and news_analyzer:
                    sentiment_summary = news_analyzer.get_sentiment_summary()
                    sentiment_path = visualizer.plot_sentiment_analysis(
                        noticias, asset_name, sentiment_summary
                    )
                    graph_paths.append(sentiment_path)
                    self.append_results(f"✅ Gráfico de sentimiento guardado: {sentiment_path}")
            
            # ============ GENERAR REPORTE PDF ============
            self.update_status("Generando reporte PDF con gráficos...", 0.9)
            self.append_results("\n\n⏳ Generando reporte PDF completo con gráficos embebidos...")
            
            # Preparar datos de análisis completos (mapear correctamente para el PDF)
            analysis_results = {
                'market_data': {
                    'statistics': {
                        'current_price': stats.get('precio_actual', 0),
                        'sma_20': trends.get('sma_20', 0),
                        'sma_50': trends.get('sma_50', 0),
                        'rsi': trends.get('rsi', 0),
                        'volatility': stats.get('volatilidad', 0),
                        'trend': trends.get('tendencia', 'N/A')
                    },
                    'trends': trends
                },
                'patrones': patterns,
                'predicciones': predictions,
                'noticias': noticias if noticias else []
            }
            
            # Generar PDF
            pdf_generator = PDFReportGenerator()
            pdf_path = pdf_generator.generate_complete_pdf_report(
                asset_name, analysis_results, graph_paths
            )
            self.append_results(f"✅ Reporte PDF completo guardado: {pdf_path}")
            
            # También generar reporte de texto (opcional)
            report_gen = ReportGenerator()
            news_summary_data = news_analyzer.get_sentiment_summary() if news_analyzer and noticias else None
            text_report_path = report_gen.generate_complete_report(
                asset_name, self.period_var.get(), stats, trends, patterns, news_summary_data
            )
            self.append_results(f"✅ Reporte de texto guardado: {text_report_path}")
            
            # ============ FINALIZAR ============
            self.update_status("✅ Análisis completado", 1.0)
            
            footer = f"""
\n╔══════════════════════════════════════════════════════════════╗
║  ✅ ANÁLISIS COMPLETADO EXITOSAMENTE
║  Los archivos han sido guardados en la carpeta 'outputs/'
╚══════════════════════════════════════════════════════════════╝
"""
            self.append_results(footer)
            
            messagebox.showinfo("¡Éxito!", 
                              f"El análisis de {asset_name} se completó correctamente.\n"
                              f"Los archivos están en la carpeta 'outputs/'")
            
        except Exception as e:
            error_msg = f"\n\n❌ ERROR: {str(e)}\n"
            self.append_results(error_msg)
            self.update_status(f"❌ Error en el análisis", 0)
            messagebox.showerror("Error", f"Ocurrió un error durante el análisis:\n{str(e)}")
        
        finally:
            self.analyzing = False
            self.analyze_button.configure(state="normal", text="🚀 Iniciar Análisis")
    
    def start_comparative_analysis(self):
        """Inicia el análisis comparativo en un thread separado"""
        if self.analyzing:
            messagebox.showwarning("Análisis en curso", 
                                 "Ya hay un análisis en progreso. Por favor espera.")
            return
        
        # Confirmar con el usuario
        result = messagebox.askyesno(
            "Análisis Comparativo",
            f"Esto analizará TODOS los {len(MarketAnalyzer.ASSETS)} activos disponibles.\n"
            f"El proceso puede tardar varios minutos.\n\n"
            f"¿Deseas continuar?"
        )
        
        if not result:
            return
        
        # Iniciar en un thread separado para no bloquear la UI
        thread = threading.Thread(target=self.perform_comparative_analysis, daemon=True)
        thread.start()
    
    def perform_comparative_analysis(self):
        """Realiza el análisis comparativo de todos los activos"""
        try:
            self.analyzing = True
            self.analyze_button.configure(state="disabled")
            self.compare_button.configure(state="disabled", text="⏳ Analizando...")
            
            # Limpiar resultados anteriores
            self.clear_results()
            
            # Obtener parámetros
            period = self.get_period_code()
            interval = self.get_interval_code()
            
            self.update_status("Iniciando análisis comparativo...", 0.05)
            
            # Header
            header = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║               ANÁLISIS COMPARATIVO DE TODOS LOS ACTIVOS
║               Fecha: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}
║               Periodo: {self.period_var.get()} | Intervalo: {self.interval_var.get()}
╚══════════════════════════════════════════════════════════════════════════════╝

🔍 Analizando {len(MarketAnalyzer.ASSETS)} activos...
"""
            self.append_results(header)
            
            # Crear analizador comparativo
            comparative = ComparativeAnalyzer()
            
            # Analizar todos los activos con callback de progreso
            def progress_callback(message, progress):
                self.update_status(message, progress)
                self.append_results(f"   {message}")
            
            results = comparative.analyze_all_assets(
                period=period,
                interval=interval,
                progress_callback=progress_callback
            )
            
            self.update_status("Generando reporte comparativo...", 0.92)
            self.append_results("\n\n📊 Generando reporte comparativo...")
            
            # Generar reporte de texto
            report = comparative.generate_comparative_report()
            self.append_results(report)
            
            # Exportar a CSV
            csv_path = comparative.export_to_csv()
            self.append_results(f"\n✅ Resultados exportados a CSV: {csv_path}")
            
            # Generar PDF con razones detalladas
            self.update_status("Generando PDF con análisis detallado...", 0.97)
            self.append_results("\n\n📄 Generando reporte PDF con razones de inversión...")
            
            # Usar los códigos correctos de yfinance (en inglés)
            pdf_path = comparative.generate_pdf_report(
                period=self.get_period_code(), 
                interval=self.get_interval_code()
            )
            if pdf_path:
                self.append_results(f"✅ Reporte PDF generado: {pdf_path}")
            
            # ============ FINALIZAR ============
            self.update_status("✅ Análisis comparativo completado", 1.0)
            
            footer = f"""
\n╔══════════════════════════════════════════════════════════════════════════════╗
║  ✅ ANÁLISIS COMPARATIVO COMPLETADO
║  Se analizaron {len(results)} activos exitosamente
║  Archivo CSV guardado en 'outputs/reports/'
╚══════════════════════════════════════════════════════════════════════════════╝
"""
            self.append_results(footer)
            
            messagebox.showinfo("¡Éxito!", 
                              f"Análisis comparativo completado.\n"
                              f"Se analizaron {len(results)} activos.\n"
                              f"Revisa los resultados para ver las mejores oportunidades.")
            
        except Exception as e:
            error_msg = f"\n\n❌ ERROR: {str(e)}\n"
            self.append_results(error_msg)
            self.update_status(f"❌ Error en el análisis comparativo", 0)
            messagebox.showerror("Error", f"Ocurrió un error durante el análisis:\n{str(e)}")
            import traceback
            traceback.print_exc()
        
        finally:
            self.analyzing = False
            self.analyze_button.configure(state="normal")
            self.compare_button.configure(state="normal", text="📊 Comparar TODOS los Activos")
    
    def start_asset_discovery(self):
        """Inicia el proceso de descubrimiento de nuevos activos"""
        if self.analyzing:
            messagebox.showwarning("En proceso", "Ya hay un análisis en curso. Por favor espera.")
            return
        
        # Confirmar acción
        confirm = messagebox.askyesno(
            "Descubrir Nuevos Activos",
            "Este proceso buscará activos emergentes con alto potencial de crecimiento.\n\n"
            "Se analizarán más de 50 activos candidatos.\n"
            "Esto puede tardar varios minutos.\n\n"
            "¿Deseas continuar?"
        )
        
        if not confirm:
            return
        
        # Ejecutar en thread separado
        thread = threading.Thread(target=self.perform_asset_discovery, daemon=True)
        thread.start()
    
    def perform_asset_discovery(self):
        """Ejecuta el descubrimiento de activos en thread separado"""
        try:
            self.analyzing = True
            self.discovery_button.configure(state="disabled", text="🔍 Buscando...")
            self.analyze_button.configure(state="disabled")
            self.compare_button.configure(state="disabled")
            
            self.clear_results()
            self.update_status("Iniciando búsqueda de activos...", 0.05)
            
            header = """
╔══════════════════════════════════════════════════════════════════════════════╗
║           🔍 BÚSQUEDA DE NUEVOS ACTIVOS CON ALTO POTENCIAL
╚══════════════════════════════════════════════════════════════════════════════╝
"""
            self.append_results(header)
            
            # Crear descubridor
            discovery = AssetDiscovery()
            
            # Función callback para progreso
            def progress_callback(message, progress):
                self.update_status(message, progress)
            
            # Ejecutar búsqueda
            self.update_status("Analizando activos candidatos...", 0.1)
            self.append_results("\n🔍 Analizando más de 50 activos candidatos...")
            self.append_results("   Buscando los que tengan score >= 60/100\n")
            
            promising_assets = discovery.discover_promising_assets(
                min_score=60,
                progress_callback=progress_callback
            )
            
            # Generar reporte
            self.update_status("Generando reporte...", 0.85)
            report = discovery.generate_discovery_report()
            self.append_results(report)
            
            # Guardar resultados
            self.update_status("Guardando resultados...", 0.90)
            discovery.save_discovered_assets()
            
            if promising_assets:
                # Preguntar si añadir al sistema
                self.root.after(0, lambda: self._ask_add_assets(discovery))
            
            self.update_status("✅ Búsqueda completada", 1.0)
            
            footer = f"""
\n╔══════════════════════════════════════════════════════════════════════════════╗
║  ✅ BÚSQUEDA DE ACTIVOS COMPLETADA
║  Se encontraron {len(promising_assets)} activos prometedores
║  Resultados guardados en 'src/discovered_assets.json'
╚══════════════════════════════════════════════════════════════════════════════╝
"""
            self.append_results(footer)
            
        except Exception as e:
            error_msg = f"\n\n❌ ERROR: {str(e)}\n"
            self.append_results(error_msg)
            self.update_status(f"❌ Error en la búsqueda", 0)
            messagebox.showerror("Error", f"Ocurrió un error durante la búsqueda:\n{str(e)}")
            import traceback
            traceback.print_exc()
        
        finally:
            self.analyzing = False
            self.discovery_button.configure(state="normal", text="🔍 Descubrir Nuevos Activos")
            self.analyze_button.configure(state="normal")
            self.compare_button.configure(state="normal")
    
    def _ask_add_assets(self, discovery: AssetDiscovery):
        """Pregunta al usuario si desea añadir los activos descubiertos"""
        add = messagebox.askyesno(
            "Añadir Activos",
            f"Se encontraron {len(discovery.discovered_assets)} activos prometedores.\n\n"
            "¿Deseas añadirlos al sistema para futuros análisis comparativos?"
        )
        
        if add:
            try:
                # Obtener activos para añadir
                new_assets = discovery.get_assets_for_addition()
                
                # Añadir al sistema
                added = MarketAnalyzer.add_new_assets(new_assets)
                
                # Guardar configuración
                MarketAnalyzer.save_assets_to_file()
                
                self.append_results(f"\n✅ Se añadieron {added} nuevos activos al sistema")
                self.append_results(f"   Total de activos disponibles: {len(MarketAnalyzer.ASSETS)}\n")
                
                messagebox.showinfo(
                    "Activos Añadidos",
                    f"Se añadieron {added} nuevos activos.\n\n"
                    f"Total de activos: {len(MarketAnalyzer.ASSETS)}\n\n"
                    "Ahora puedes analizarlos en el análisis comparativo."
                )
                
            except Exception as e:
                messagebox.showerror("Error", f"Error añadiendo activos:\n{str(e)}")
    
    def run(self):
        """Inicia la aplicación"""
        self.root.mainloop()


if __name__ == "__main__":
    app = MarketAnalysisApp()
    app.run()
