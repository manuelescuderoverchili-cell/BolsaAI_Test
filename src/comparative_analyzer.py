"""
Analizador comparativo de múltiples activos
Analiza todos los activos disponibles y los clasifica por rentabilidad
"""
import pandas as pd
from datetime import datetime
from typing import Dict, List
import os

from market_analyzer import MarketAnalyzer
from pattern_analyzer import TechnicalPatternAnalyzer
from predictive_analyzer import PredictiveAnalyzer
from comparative_pdf_generator import ComparativePDFGenerator

print(f"[INFO] comparative_analyzer.py cargado")
print(f"[INFO] ComparativePDFGenerator version: {getattr(ComparativePDFGenerator, 'VERSION', 'UNKNOWN')}")


class ComparativeAnalyzer:
    """Analiza múltiples activos y los compara"""
    
    def __init__(self):
        self.results = []
        
    def analyze_all_assets(self, period: str = "1mo", interval: str = "1d", 
                          progress_callback=None) -> List[Dict]:
        """
        Analiza todos los activos disponibles
        
        Args:
            period: Periodo de análisis
            interval: Intervalo de datos
            progress_callback: Función para reportar progreso
            
        Returns:
            Lista de resultados ordenados por rentabilidad
        """
        self.results = []
        assets = list(MarketAnalyzer.ASSETS.keys())
        total = len(assets)
        
        for idx, asset_name in enumerate(assets):
            try:
                if progress_callback:
                    progress_callback(f"Analizando {asset_name}...", (idx + 1) / total)
                
                # Analizar el activo
                result = self._analyze_single_asset(asset_name, period, interval)
                if result:
                    self.results.append(result)
                    
            except Exception as e:
                print(f"[ERROR] Error analizando {asset_name}: {e}")
                continue
        
        # Ordenar por score de rentabilidad
        self.results.sort(key=lambda x: x['score_rentabilidad'], reverse=True)
        
        return self.results
    
    def _analyze_single_asset(self, asset_name: str, period: str, interval: str) -> Dict:
        """
        Analiza un activo individual
        
        Args:
            asset_name: Nombre del activo
            period: Periodo
            interval: Intervalo
            
        Returns:
            Diccionario con resultados del análisis
        """
        # Obtener datos
        analyzer = MarketAnalyzer(asset_name)
        data = analyzer.get_data(period=period, interval=interval)
        
        if len(data) < 5:
            return None
        
        # Estadísticas básicas
        stats = analyzer.calculate_statistics()
        trends = analyzer.detect_trends()
        
        # Análisis de patrones
        pattern_analyzer = TechnicalPatternAnalyzer(data)
        patterns = pattern_analyzer.analyze_all_patterns()
        
        # Predicciones
        predictive_analyzer = PredictiveAnalyzer(data, patterns)
        prediction_report, predictions = predictive_analyzer.generate_prediction_report()
        
        # Calcular score de rentabilidad
        score = self._calculate_rentability_score(stats, trends, patterns, predictions)
        
        # Categorizar
        categoria = self._categorize_asset(predictions, score)
        
        # Calcular retorno esperado
        precio_actual = stats.get('precio_actual', 0)
        rango_precio = predictions.get('rango_precio_estimado', {})
        precio_objetivo = rango_precio.get('objetivo', precio_actual)
        retorno_esperado = ((precio_objetivo - precio_actual) / precio_actual * 100) if precio_actual > 0 else 0
        
        result = {
            'activo': asset_name,
            'ticker': MarketAnalyzer.ASSETS[asset_name],
            'precio_actual': precio_actual,
            'precio_objetivo': precio_objetivo,
            'retorno_esperado': retorno_esperado,
            'direccion': predictions['direccion_probable'],
            'confianza': predictions['confianza'],
            'tendencia': trends.get('tendencia', 'N/A'),
            'volatilidad': stats.get('volatilidad', 0),
            'rsi': trends.get('rsi', 50),
            'patrones_alcistas': len([p for p in patterns.get('todos', []) 
                                     if p.get('tipo') == 'Alcista' or p.get('señal') == 'Alcista']),
            'patrones_bajistas': len([p for p in patterns.get('todos', []) 
                                     if p.get('tipo') == 'Bajista' or p.get('señal') == 'Bajista']),
            'total_patrones': len(patterns.get('todos', [])),
            'score_rentabilidad': score,
            'categoria': categoria,
            'recomendacion': self._generate_recommendation(predictions, score, retorno_esperado)
        }
        
        return result
    
    def _calculate_rentability_score(self, stats: Dict, trends: Dict, patterns: Dict, 
                                     predictions: Dict) -> float:
        """
        Calcula un score de rentabilidad (0-100)
        
        Args:
            stats: Estadísticas del mercado
            trends: Tendencias técnicas
            patterns: Patrones detectados
            predictions: Predicciones
            
        Returns:
            Score de rentabilidad
        """
        score = 50.0  # Score base neutral
        
        # Factor 1: Dirección y confianza de la predicción (±30 puntos)
        direccion = predictions.get('direccion_probable', 'Neutral')
        confianza = predictions.get('confianza', 0)
        
        if direccion == 'Alcista':
            score += (confianza / 100) * 30
        elif direccion == 'Bajista':
            score -= (confianza / 100) * 30
        
        # Factor 2: Balance de patrones (±15 puntos)
        todos_patrones = patterns.get('todos', [])
        if todos_patrones:
            alcistas = len([p for p in todos_patrones if p.get('tipo') == 'Alcista' or p.get('señal') == 'Alcista'])
            bajistas = len([p for p in todos_patrones if p.get('tipo') == 'Bajista' or p.get('señal') == 'Bajista'])
            total = len(todos_patrones)
            
            if total > 0:
                ratio_alcista = alcistas / total
                score += (ratio_alcista - 0.5) * 30  # De -15 a +15
        
        # Factor 3: RSI (±10 puntos)
        rsi = trends.get('rsi', 50)
        if rsi:
            if rsi < 30:  # Sobreventa (oportunidad)
                score += 10
            elif rsi > 70:  # Sobrecompra (riesgo)
                score -= 10
            elif 40 <= rsi <= 60:  # Zona neutral
                score += 5
        
        # Factor 4: Tendencia (±10 puntos)
        tendencia = trends.get('tendencia', 'lateral')
        if tendencia and tendencia.lower() == 'alcista':
            score += 10
        elif tendencia and tendencia.lower() == 'bajista':
            score -= 10
        
        # Factor 5: Volatilidad (±5 puntos, menos volatilidad = más estable)
        volatilidad = stats.get('volatilidad', 0)
        if volatilidad:
            if volatilidad < 2:
                score += 5
            elif volatilidad > 5:
                score -= 5
        
        # Limitar score entre 0 y 100
        score = max(0, min(100, score))
        
        return round(score, 2)
    
    def _categorize_asset(self, predictions: Dict, score: float) -> str:
        """
        Categoriza el activo según su potencial
        
        Args:
            predictions: Predicciones
            score: Score de rentabilidad
            
        Returns:
            Categoría del activo
        """
        if score >= 75:
            return "🟢 MUY ALCISTA"
        elif score >= 60:
            return "🟢 ALCISTA"
        elif score >= 45:
            return "🟡 NEUTRAL-ALCISTA"
        elif score >= 35:
            return "🟡 NEUTRAL"
        elif score >= 25:
            return "🟠 NEUTRAL-BAJISTA"
        elif score >= 15:
            return "🔴 BAJISTA"
        else:
            return "🔴 MUY BAJISTA"
    
    def _generate_recommendation(self, predictions: Dict, score: float, 
                                retorno_esperado: float) -> str:
        """
        Genera una recomendación de inversión
        
        Args:
            predictions: Predicciones
            score: Score de rentabilidad
            retorno_esperado: Retorno esperado en %
            
        Returns:
            Recomendación
        """
        confianza = predictions.get('confianza', 0)
        
        if score >= 70 and confianza >= 60:
            return "🚀 COMPRA FUERTE"
        elif score >= 60 and confianza >= 50:
            return "✅ COMPRA"
        elif score >= 50:
            return "👍 COMPRA MODERADA"
        elif score >= 40:
            return "⚖️ MANTENER/OBSERVAR"
        elif score >= 30:
            return "⚠️ PRECAUCIÓN"
        elif score >= 20:
            return "📉 CONSIDERAR VENTA"
        else:
            return "🛑 VENTA FUERTE"
    
    def generate_comparative_report(self) -> str:
        """
        Genera un reporte comparativo de todos los activos
        
        Returns:
            String con el reporte
        """
        if not self.results:
            return "No hay resultados para mostrar"
        
        report = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    ANÁLISIS COMPARATIVO DE ACTIVOS
║                    {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}
╚══════════════════════════════════════════════════════════════════════════════╝

📊 Total de activos analizados: {len(self.results)}

═══════════════════════════════════════════════════════════════════════════════
                        🏆 RANKING DE OPORTUNIDADES
═══════════════════════════════════════════════════════════════════════════════

"""
        
        # Top 5 mejores oportunidades
        report += "🥇 TOP 5 - MEJORES OPORTUNIDADES DE INVERSIÓN:\n\n"
        
        for i, result in enumerate(self.results[:5], 1):
            medal = ["🥇", "🥈", "🥉", "🏅", "🏅"][i-1]
            report += f"{medal} #{i} - {result['activo']} ({result['ticker']})\n"
            report += f"   • Precio actual: ${result['precio_actual']:,.2f}\n"
            report += f"   • Precio objetivo: ${result['precio_objetivo']:,.2f}\n"
            report += f"   • Retorno esperado: {result['retorno_esperado']:+.2f}%\n"
            report += f"   • Dirección: {result['direccion']} (Confianza: {result['confianza']:.1f}%)\n"
            report += f"   • Categoría: {result['categoria']}\n"
            report += f"   • Score de rentabilidad: {result['score_rentabilidad']:.1f}/100\n"
            report += f"   • Recomendación: {result['recomendacion']}\n"
            
            rsi_str = f"{result['rsi']:.1f}" if result['rsi'] is not None else "N/A"
            vol_str = f"{result['volatilidad']:.2f}" if result['volatilidad'] is not None else "N/A"
            report += f"   • RSI: {rsi_str} | Volatilidad: {vol_str}%\n"
            report += f"   • Patrones: {result['patrones_alcistas']}↑ / {result['patrones_bajistas']}↓\n\n"
        
        # Bottom 5 (advertencias)
        report += "\n⚠️ BOTTOM 5 - ACTIVOS CON MAYOR RIESGO:\n\n"
        
        for i, result in enumerate(self.results[-5:][::-1], 1):
            report += f"#{len(self.results)-5+i} - {result['activo']} ({result['ticker']})\n"
            report += f"   • Precio actual: ${result['precio_actual']:,.2f}\n"
            report += f"   • Retorno esperado: {result['retorno_esperado']:+.2f}%\n"
            report += f"   • Categoría: {result['categoria']}\n"
            report += f"   • Score: {result['score_rentabilidad']:.1f}/100\n"
            report += f"   • Recomendación: {result['recomendacion']}\n\n"
        
        # Resumen por categorías
        report += "\n═══════════════════════════════════════════════════════════════════════════════\n"
        report += "                        📑 RESUMEN POR CATEGORÍAS\n"
        report += "═══════════════════════════════════════════════════════════════════════════════\n\n"
        
        categorias = {}
        for result in self.results:
            cat = result['categoria']
            if cat not in categorias:
                categorias[cat] = []
            categorias[cat].append(result['activo'])
        
        for cat, activos in sorted(categorias.items(), reverse=True):
            report += f"{cat}: {len(activos)} activos\n"
            report += f"   {', '.join(activos)}\n\n"
        
        # Estadísticas generales
        report += "\n═══════════════════════════════════════════════════════════════════════════════\n"
        report += "                        📈 ESTADÍSTICAS GENERALES\n"
        report += "═══════════════════════════════════════════════════════════════════════════════\n\n"
        
        alcistas = len([r for r in self.results if r['direccion'] == 'Alcista'])
        bajistas = len([r for r in self.results if r['direccion'] == 'Bajista'])
        neutrales = len(self.results) - alcistas - bajistas
        
        avg_retorno = sum(r['retorno_esperado'] for r in self.results) / len(self.results)
        avg_confianza = sum(r['confianza'] for r in self.results) / len(self.results)
        avg_score = sum(r['score_rentabilidad'] for r in self.results) / len(self.results)
        
        report += f"📊 Distribución de señales:\n"
        report += f"   • Alcistas: {alcistas} ({alcistas/len(self.results)*100:.1f}%)\n"
        report += f"   • Bajistas: {bajistas} ({bajistas/len(self.results)*100:.1f}%)\n"
        report += f"   • Neutrales: {neutrales} ({neutrales/len(self.results)*100:.1f}%)\n\n"
        
        report += f"💰 Promedios:\n"
        report += f"   • Retorno esperado promedio: {avg_retorno:+.2f}%\n"
        report += f"   • Confianza promedio: {avg_confianza:.1f}%\n"
        report += f"   • Score promedio: {avg_score:.1f}/100\n\n"
        
        report += f"🎯 Recomendaciones:\n"
        compra_fuerte = len([r for r in self.results if '🚀' in r['recomendacion']])
        compra = len([r for r in self.results if '✅' in r['recomendacion'] or '👍' in r['recomendacion']])
        venta = len([r for r in self.results if '📉' in r['recomendacion'] or '🛑' in r['recomendacion']])
        
        report += f"   • Compra fuerte: {compra_fuerte} activos\n"
        report += f"   • Compra/Compra moderada: {compra} activos\n"
        report += f"   • Venta/Precaución: {venta} activos\n"
        
        report += "\n═══════════════════════════════════════════════════════════════════════════════\n"
        
        return report
    
    def export_to_csv(self, filepath: str = None) -> str:
        """
        Exporta los resultados a CSV
        
        Args:
            filepath: Ruta del archivo (opcional)
            
        Returns:
            Ruta del archivo generado
        """
        if not self.results:
            return None
        
        if not filepath:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = f"outputs/reports/Comparativa_Activos_{timestamp}.csv"
        
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        # Convertir a DataFrame
        df = pd.DataFrame(self.results)
        
        # Ordenar columnas
        columns = ['activo', 'ticker', 'categoria', 'recomendacion', 'score_rentabilidad',
                  'precio_actual', 'precio_objetivo', 'retorno_esperado', 'direccion', 
                  'confianza', 'tendencia', 'rsi', 'volatilidad', 'patrones_alcistas',
                  'patrones_bajistas', 'total_patrones']
        
        df = df[columns]
        df.to_csv(filepath, index=False, encoding='utf-8-sig')
        
        print(f"[OK] Resultados exportados a CSV: {filepath}")
        return filepath
    
    def generate_pdf_report(self, period: str = "1mo", interval: str = "1d") -> str:
        """
        Genera un reporte PDF comparativo con razones detalladas
        
        Args:
            period: Periodo analizado
            interval: Intervalo usado
            
        Returns:
            Ruta del archivo PDF generado
        """
        if not self.results:
            print("[WARNING] No hay resultados para generar PDF")
            return None
        
        # Recargar el módulo para asegurar que se use la última versión
        import importlib
        import comparative_pdf_generator
        importlib.reload(comparative_pdf_generator)
        
        from comparative_pdf_generator import ComparativePDFGenerator
        print(f"[PDF] Usando ComparativePDFGenerator version: {getattr(ComparativePDFGenerator, 'VERSION', 'UNKNOWN')}")
        
        pdf_generator = ComparativePDFGenerator()
        pdf_path = pdf_generator.generate_comparative_pdf(self.results, period, interval)
        
        return pdf_path
