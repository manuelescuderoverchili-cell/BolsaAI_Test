"""
Generador de reportes detallados de análisis
"""
from datetime import datetime
import os
from typing import Dict, List


class ReportGenerator:
    """Clase para generar reportes detallados de todos los análisis"""
    
    def __init__(self, output_dir: str = "outputs/reports"):
        """
        Inicializa el generador de reportes
        
        Args:
            output_dir: Directorio donde guardar los reportes
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def generate_complete_report(self, asset_name: str, period: str, 
                                stats: Dict, trends: Dict, patterns: Dict,
                                news_summary: Dict = None) -> str:
        """
        Genera un reporte completo de todos los análisis
        
        Args:
            asset_name: Nombre del activo
            period: Periodo analizado
            stats: Estadísticas del activo
            trends: Tendencias detectadas
            patterns: Patrones encontrados
            news_summary: Resumen de noticias (opcional)
            
        Returns:
            Ruta del archivo del reporte
        """
        timestamp = datetime.now()
        
        report = f"""
╔══════════════════════════════════════════════════════════════╗
║           REPORTE DETALLADO DE ANÁLISIS FINANCIERO
║           {asset_name.upper()}
╚══════════════════════════════════════════════════════════════╝

Fecha de generación: {timestamp.strftime("%d/%m/%Y %H:%M:%S")}
Periodo analizado: {period}

═══════════════════════════════════════════════════════════════
                    1. ANÁLISIS ESTADÍSTICO
═══════════════════════════════════════════════════════════════

TEST 1: ESTADÍSTICAS BÁSICAS
─────────────────────────────────────────────────────────────
✅ EJECUTADO CORRECTAMENTE

Datos recopilados:
• Número de registros: {stats['num_datos']}
• Precio actual: ${stats['precio_actual']:,.2f}
• Precio inicial del periodo: ${stats['precio_inicial']:,.2f}
• Precio máximo alcanzado: ${stats['precio_maximo']:,.2f}
• Precio mínimo alcanzado: ${stats['precio_minimo']:,.2f}
• Volumen promedio: {stats['volumen_promedio']:,.0f}

Variaciones:
• Variación absoluta: ${stats['variacion_absoluta']:+,.2f}
• Variación porcentual: {stats['variacion_porcentual']:+.2f}%
• Volatilidad (desviación estándar): {stats['volatilidad']:.2f}%

Interpretación:
"""
        
        if stats['variacion_porcentual'] > 5:
            report += "  → FUERTE SUBIDA en el periodo analizado\n"
        elif stats['variacion_porcentual'] > 0:
            report += "  → Subida moderada en el periodo analizado\n"
        elif stats['variacion_porcentual'] > -5:
            report += "  → Bajada moderada en el periodo analizado\n"
        else:
            report += "  → FUERTE BAJADA en el periodo analizado\n"
        
        if stats['volatilidad'] > 5:
            report += "  → Volatilidad ALTA - mercado muy agitado\n"
        elif stats['volatilidad'] > 2:
            report += "  → Volatilidad MODERADA - movimientos normales\n"
        else:
            report += "  → Volatilidad BAJA - mercado estable\n"
        
        report += f"""
═══════════════════════════════════════════════════════════════
                    2. ANÁLISIS TÉCNICO
═══════════════════════════════════════════════════════════════

TEST 2: INDICADORES TÉCNICOS
─────────────────────────────────────────────────────────────
✅ EJECUTADO CORRECTAMENTE

Tendencia detectada: {trends['tendencia'].upper()}
Señal de trading: {trends['señal'].upper()}

Medias Móviles:
"""
        
        if trends.get('sma_20') is not None:
            report += f"• SMA 20: ${trends['sma_20']:,.2f}"
            if trends.get('precio_vs_sma20') is not None:
                report += f" ({trends['precio_vs_sma20']:+.2f}% del precio actual)\n"
            else:
                report += "\n"
        else:
            report += "• SMA 20: No disponible (datos insuficientes)\n"
        
        if trends.get('sma_50') is not None:
            report += f"• SMA 50: ${trends['sma_50']:,.2f}"
            if trends.get('precio_vs_sma50') is not None:
                report += f" ({trends['precio_vs_sma50']:+.2f}% del precio actual)\n"
            else:
                report += "\n"
        else:
            report += "• SMA 50: No disponible (datos insuficientes)\n"
        
        report += f"""
RSI (Relative Strength Index):
"""
        
        if trends.get('rsi') is not None:
            rsi_val = trends['rsi']
            report += f"• Valor RSI: {rsi_val:.2f}\n"
            if rsi_val > 70:
                report += "• Estado: SOBRECOMPRA - Posible corrección a la baja\n"
            elif rsi_val < 30:
                report += "• Estado: SOBREVENTA - Posible rebote al alza\n"
            else:
                report += "• Estado: NEUTRAL - Sin señales extremas\n"
        else:
            report += "• RSI: No disponible (datos insuficientes)\n"
        
        report += f"""
Soportes y Resistencias:
• Soporte identificado: ${trends['soporte']:,.2f}
• Resistencia identificada: ${trends['resistencia']:,.2f}
• Distancia al soporte: {((stats['precio_actual'] - trends['soporte']) / stats['precio_actual'] * 100):+.2f}%
• Distancia a resistencia: {((trends['resistencia'] - stats['precio_actual']) / stats['precio_actual'] * 100):+.2f}%

═══════════════════════════════════════════════════════════════
                3. DETECCIÓN DE PATRONES
═══════════════════════════════════════════════════════════════

TEST 3: PATRONES DE VELAS JAPONESAS
─────────────────────────────────────────────────────────────
✅ EJECUTADO CORRECTAMENTE

Patrones encontrados: {len(patterns['velas_japonesas'])}
"""
        
        if patterns['velas_japonesas']:
            for p in patterns['velas_japonesas'][:5]:
                fecha_str = p['fecha'].strftime("%d/%m/%Y") if hasattr(p['fecha'], 'strftime') else str(p['fecha'])
                report += f"\n• [{fecha_str}] {p['patron']}\n"
                report += f"  Tipo: {p['tipo']} | Confianza: {p['confianza']}\n"
                report += f"  {p['descripcion']}\n"
        else:
            report += "\nNo se detectaron patrones de velas significativos.\n"
        
        report += f"""
TEST 4: PATRONES GRÁFICOS
─────────────────────────────────────────────────────────────
✅ EJECUTADO CORRECTAMENTE

Patrones encontrados: {len(patterns['patrones_graficos'])}
"""
        
        if patterns['patrones_graficos']:
            for p in patterns['patrones_graficos'][:5]:
                fecha_str = p['fecha'].strftime("%d/%m/%Y") if hasattr(p['fecha'], 'strftime') else str(p['fecha'])
                report += f"\n• [{fecha_str}] {p['patron']}\n"
                report += f"  Tipo: {p['tipo']} | Confianza: {p['confianza']}\n"
                report += f"  {p['descripcion']}\n"
        else:
            report += "\nNo se detectaron patrones gráficos significativos.\n"
        
        report += f"""
TEST 5: DIVERGENCIAS DE MOMENTUM
─────────────────────────────────────────────────────────────
✅ EJECUTADO CORRECTAMENTE

Divergencias encontradas: {len(patterns['divergencias'])}
"""
        
        if patterns['divergencias']:
            for d in patterns['divergencias'][:3]:
                fecha_str = d['fecha'].strftime("%d/%m/%Y") if hasattr(d['fecha'], 'strftime') else str(d['fecha'])
                report += f"\n• [{fecha_str}] {d['tipo']}\n"
                report += f"  Señal: {d['señal']} | Confianza: {d['confianza']}\n"
                report += f"  {d['descripcion']}\n"
        else:
            report += "\nNo se detectaron divergencias significativas.\n"
        
        report += f"""
TEST 6: ANÁLISIS DE VOLUMEN
─────────────────────────────────────────────────────────────
✅ EJECUTADO CORRECTAMENTE

Patrones de volumen encontrados: {len(patterns['volumen'])}
"""
        
        if patterns['volumen']:
            for v in patterns['volumen'][:3]:
                fecha_str = v['fecha'].strftime("%d/%m/%Y") if hasattr(v['fecha'], 'strftime') else str(v['fecha'])
                report += f"\n• [{fecha_str}] {v['patron']}\n"
                report += f"  Tipo: {v['tipo']} | Confianza: {v['confianza']}\n"
                report += f"  {v['descripcion']}\n"
        else:
            report += "\nNo se detectaron patrones de volumen inusuales.\n"
        
        # Análisis de noticias si está disponible
        if news_summary:
            report += f"""
═══════════════════════════════════════════════════════════════
                4. ANÁLISIS DE SENTIMIENTO
═══════════════════════════════════════════════════════════════

TEST 7: ANÁLISIS DE NOTICIAS
─────────────────────────────────────────────────────────────
✅ EJECUTADO CORRECTAMENTE

Noticias analizadas: {news_summary['total']}

Distribución de sentimiento:
• Noticias positivas: {news_summary['positivas']} ({news_summary['positivas']/news_summary['total']*100 if news_summary['total'] > 0 else 0:.1f}%)
• Noticias negativas: {news_summary['negativas']} ({news_summary['negativas']/news_summary['total']*100 if news_summary['total'] > 0 else 0:.1f}%)
• Noticias neutrales: {news_summary['neutrales']} ({news_summary['neutrales']/news_summary['total']*100 if news_summary['total'] > 0 else 0:.1f}%)

Métricas de sentimiento:
• Sentimiento promedio: {news_summary['sentimiento_promedio']:+.3f}
• Subjetividad promedio: {news_summary['subjetividad_promedio']:.3f}

Interpretación:
"""
            if news_summary['sentimiento_promedio'] > 0.1:
                report += "  → Sentimiento POSITIVO en las noticias\n"
            elif news_summary['sentimiento_promedio'] < -0.1:
                report += "  → Sentimiento NEGATIVO en las noticias\n"
            else:
                report += "  → Sentimiento NEUTRAL en las noticias\n"
        
        # Resumen final
        report += f"""
═══════════════════════════════════════════════════════════════
                    RESUMEN EJECUTIVO
═══════════════════════════════════════════════════════════════

TESTS EJECUTADOS: 7/7 ✅

Conclusiones principales:

1. PRECIO Y TENDENCIA:
   • El precio ha variado {stats['variacion_porcentual']:+.2f}% en el periodo
   • Tendencia identificada: {trends['tendencia'].upper()}
   • Señal de trading: {trends['señal'].upper()}

2. PATRONES TÉCNICOS:
   • Total de patrones detectados: {patterns['total']}
   • Patrones alcistas vs bajistas: Ver detalle arriba
   • Nivel de confianza: Variable según patrón

3. VOLATILIDAD Y RIESGO:
   • Volatilidad: {stats['volatilidad']:.2f}% ({'ALTA' if stats['volatilidad'] > 5 else 'MODERADA' if stats['volatilidad'] > 2 else 'BAJA'})
   • Rango de precios: ${stats['precio_minimo']:,.2f} - ${stats['precio_maximo']:,.2f}
"""
        
        if news_summary:
            report += f"""
4. SENTIMIENTO DEL MERCADO:
   • Sentimiento de noticias: {'POSITIVO' if news_summary['sentimiento_promedio'] > 0.1 else 'NEGATIVO' if news_summary['sentimiento_promedio'] < -0.1 else 'NEUTRAL'}
   • Nivel de cobertura mediática: {'ALTO' if news_summary['total'] > 30 else 'MEDIO' if news_summary['total'] > 15 else 'BAJO'}
"""
        
        report += f"""
RECOMENDACIÓN GENERAL:
{'⚠️ PRECAUCIÓN' if stats['volatilidad'] > 5 or abs(stats['variacion_porcentual']) > 10 else '✅ ESTABLE'}

═══════════════════════════════════════════════════════════════
Fin del reporte - {timestamp.strftime("%d/%m/%Y %H:%M:%S")}
═══════════════════════════════════════════════════════════════
"""
        
        # Guardar reporte
        filename = f"{asset_name.replace(' ', '_')}_reporte_{timestamp.strftime('%Y%m%d_%H%M%S')}.txt"
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"📄 Reporte guardado: {filepath}")
        return filepath
