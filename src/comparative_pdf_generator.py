"""
Generador de reportes PDF comparativos
"""
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.platypus import Table, TableStyle, Image
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from datetime import datetime
import os
from typing import List, Dict
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import yfinance as yf
import pandas as pd
from src.news_analyzer import NewsAnalyzer


class ComparativePDFGenerator:
    """Genera reportes PDF del análisis comparativo"""
    
    VERSION = "2.0_WITH_CHARTS_AND_NEWS"  # Indicador de versión
    
    def __init__(self, output_dir: str = "outputs/reports"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        print(f"[PDF] ComparativePDFGenerator v{self.VERSION} inicializado")
        
    def generate_comparative_pdf(self, results: List[Dict], period: str, interval: str) -> str:
        """
        Genera un PDF con el análisis comparativo completo
        
        Args:
            results: Lista de resultados del análisis
            period: Periodo analizado
            interval: Intervalo usado
            
        Returns:
            Ruta del archivo PDF generado
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"Analisis_Comparativo_{timestamp}.pdf"
        filepath = os.path.join(self.output_dir, filename)
        
        # Crear documento
        doc = SimpleDocTemplate(filepath, pagesize=letter,
                               rightMargin=0.5*inch, leftMargin=0.5*inch,
                               topMargin=0.5*inch, bottomMargin=0.5*inch)
        
        story = []
        styles = getSampleStyleSheet()
        
        # Estilos personalizados
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Title'],
            fontSize=22,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=20,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading1'],
            fontSize=15,
            textColor=colors.HexColor('#2E86AB'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        )
        
        subheading_style = ParagraphStyle(
            'CustomSubHeading',
            parent=styles['Heading2'],
            fontSize=12,
            textColor=colors.HexColor('#555555'),
            spaceAfter=8,
            fontName='Helvetica-Bold'
        )
        
        normal_style = ParagraphStyle(
            'CustomNormal',
            parent=styles['Normal'],
            fontSize=9,
            alignment=TA_JUSTIFY,
            spaceAfter=6
        )
        
        # ============ PORTADA ============
        story.append(Spacer(1, 0.8*inch))
        story.append(Paragraph("📊 ANÁLISIS COMPARATIVO", title_style))
        story.append(Paragraph("DE OPORTUNIDADES DE INVERSIÓN", title_style))
        story.append(Spacer(1, 0.3*inch))
        
        fecha_actual = datetime.now().strftime("%d de %B de %Y - %H:%M")
        story.append(Paragraph(f"Fecha de generación: {fecha_actual}", 
                              ParagraphStyle('DateStyle', parent=normal_style, 
                                           alignment=TA_CENTER, fontSize=10)))
        
        story.append(Spacer(1, 0.3*inch))
        
        # Resumen ejecutivo portada
        total_activos = len(results)
        alcistas = len([r for r in results if 'ALCISTA' in r['categoria'] and 'BAJISTA' not in r['categoria']])
        bajistas = len([r for r in results if 'BAJISTA' in r['categoria']])
        
        resumen_portada = f"""
        <b>Activos Analizados:</b> {total_activos}<br/>
        <b>Periodo:</b> {period} | <b>Intervalo:</b> {interval}<br/>
        <b>Señales Alcistas:</b> {alcistas} | <b>Señales Bajistas:</b> {bajistas}<br/>
        """
        story.append(Paragraph(resumen_portada, 
                              ParagraphStyle('ResumenPortada', parent=normal_style, 
                                           alignment=TA_CENTER, fontSize=11)))
        
        story.append(PageBreak())
        
        # ============ GRÁFICO DE DISTRIBUCIÓN ============
        story.append(Paragraph("DISTRIBUCIÓN DE CATEGORÍAS", heading_style))
        
        # Generar gráfico de distribución
        chart_path = self._generate_distribution_chart(results)
        if os.path.exists(chart_path):
            img = Image(chart_path, width=6.5*inch, height=4*inch)
            story.append(img)
            story.append(Spacer(1, 0.2*inch))
        
        story.append(PageBreak())
        
        # ============ TOP 5 MEJORES OPORTUNIDADES ============
        story.append(Paragraph("🏆 TOP 5 - MEJORES OPORTUNIDADES DE INVERSIÓN", heading_style))
        story.append(Spacer(1, 0.2*inch))
        
        # PRE-GENERAR TODOS LOS GRÁFICOS
        print("\n📊 Pre-generando gráficos para las mejores oportunidades...")
        chart_paths = {}
        for i, result in enumerate(results[:5], 1):
            ticker = result['ticker']
            asset_name = result['activo']
            chart_path = self._generate_price_chart(ticker, asset_name, period=period, interval=interval)
            chart_paths[ticker] = chart_path
            print(f"   {i}. {asset_name}: {'✅ Generado' if chart_path else '❌ Error'}")
        
        print()
        
        for i, result in enumerate(results[:5], 1):
            medal = ["🥇", "🥈", "🥉", "🏅", "🏅"][i-1]
            
            # Título del activo
            activo_title = f"{medal} #{i} - {result['activo']} ({result['ticker']})"
            story.append(Paragraph(activo_title, subheading_style))
            
            # CALCULAR TIEMPO ESTIMADO HASTA RETORNO
            tiempo_retorno = self._calculate_expected_timeframe(result)
            
            # Tabla de datos principales (AMPLIADA)
            rsi_value = f"{result['rsi']:.1f}" if result['rsi'] is not None else "N/A"
            vol_value = f"{result['volatilidad']:.2f}%" if result['volatilidad'] is not None else "N/A"
            
            data_table = [
                ['Métrica', 'Valor'],
                ['Categoría', result['categoria']],
                ['Score de Rentabilidad', f"{result['score_rentabilidad']:.1f}/100"],
                ['Precio Actual', f"${result['precio_actual']:,.2f}"],
                ['Precio Objetivo', f"${result['precio_objetivo']:,.2f}"],
                ['Retorno Esperado', f"{result['retorno_esperado']:+.2f}%"],
                ['⏱️ Tiempo Estimado', tiempo_retorno],  # NUEVO
                ['Dirección', f"{result['direccion']} ({result['confianza']:.0f}% confianza)"],
                ['RSI', rsi_value],
                ['Volatilidad', vol_value],
                ['Patrones', f"{result['patrones_alcistas']}↑ / {result['patrones_bajistas']}↓"]
            ]
            
            table = Table(data_table, colWidths=[2.5*inch, 3.5*inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E86AB')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                # Destacar tiempo estimado
                ('BACKGROUND', (0, 6), (-1, 6), colors.HexColor('#E8F5E9')),
                ('FONTNAME', (0, 6), (-1, 6), 'Helvetica-Bold'),
            ]))
            story.append(table)
            story.append(Spacer(1, 0.15*inch))
            
            # GRÁFICA DE EVOLUCIÓN TEMPORAL
            chart_path = chart_paths.get(result['ticker'])
            
            # Si no hay gráfico pre-generado, intentar generar ahora
            if not chart_path:
                print(f"   ⚠️ Gráfico no pre-generado para {result['activo']}, generando ahora...")
                chart_path = self._generate_price_chart(result['ticker'], result['activo'], 
                                                         period=period, interval=interval)
            
            if chart_path and os.path.exists(chart_path):
                print(f"   ✅ Añadiendo gráfico de {result['activo']} al PDF")
                story.append(Paragraph("📈 GRÁFICO HISTÓRICO DE PRECIO:", 
                                      ParagraphStyle('ChartTitle', parent=subheading_style, 
                                                   fontSize=11, textColor=colors.HexColor('#2E86AB'))))
                story.append(Spacer(1, 0.1*inch))
                
                # Añadir imagen de la gráfica
                try:
                    img = Image(chart_path, width=6*inch, height=3*inch)
                    story.append(img)
                    story.append(Spacer(1, 0.15*inch))
                    print(f"   ✅ Gráfico añadido correctamente")
                except Exception as e:
                    print(f"   ⚠️ Error al añadir imagen al PDF: {e}")
                    # Continuar sin el gráfico
            else:
                print(f"   ℹ️ No se pudo generar gráfico para {result['activo']} (puede no tener datos suficientes)")
                # Añadir un mensaje indicando que no hay gráfico disponible
                story.append(Paragraph("📊 Gráfico no disponible para este activo (datos insuficientes)", 
                                     ParagraphStyle('NoChart', parent=normal_style, 
                                                  fontSize=9, textColor=colors.grey, 
                                                  alignment=TA_CENTER)))
                story.append(Spacer(1, 0.15*inch))
            
            # NOTICIAS CLAVE
            noticias = self._get_key_news(result['activo'], max_news=3)
            if noticias:
                story.append(Paragraph("📰 NOTICIAS CLAVE RECIENTES:", 
                                      ParagraphStyle('NewsTitle', parent=subheading_style, 
                                                   fontSize=11, textColor=colors.HexColor('#FF6B35'))))
                story.append(Spacer(1, 0.1*inch))
                
                for idx, noticia in enumerate(noticias, 1):
                    # Título con enlace
                    titulo_noticia = noticia['titulo']
                    link = noticia['link']
                    
                    if link:
                        news_text = f'<b>{idx}. <link href="{link}" color="blue">{titulo_noticia}</link></b>'
                    else:
                        news_text = f'<b>{idx}. {titulo_noticia}</b>'
                    
                    story.append(Paragraph(news_text, 
                                         ParagraphStyle('NewsItem', parent=normal_style, 
                                                      fontSize=9, leftIndent=10)))
                    
                    # Resumen/descripción
                    descripcion = noticia.get('descripcion', '')
                    if descripcion and len(descripcion) > 15:
                        story.append(Paragraph(f'<i>{descripcion}</i>', 
                                             ParagraphStyle('NewsDesc', parent=normal_style, 
                                                          fontSize=8, leftIndent=15, 
                                                          textColor=colors.HexColor('#555555'))))
                    
                    # Fecha
                    fecha = noticia.get('fecha', 'N/A')
                    story.append(Paragraph(f'📅 {fecha}', 
                                         ParagraphStyle('NewsDate', parent=normal_style, 
                                                      fontSize=7, leftIndent=15, 
                                                      textColor=colors.grey)))
                    story.append(Spacer(1, 0.08*inch))
                
                story.append(Spacer(1, 0.1*inch))
            
            # RAZÓN DE LA RECOMENDACIÓN
            story.append(Paragraph("📋 ANÁLISIS Y RECOMENDACIÓN:", 
                                  ParagraphStyle('RazonTitle', parent=subheading_style, 
                                               fontSize=11, textColor=colors.HexColor('#28a745'))))
            
            razon = self._generate_recommendation_reason(result)
            story.append(Paragraph(razon, normal_style))
            
            story.append(Spacer(1, 0.2*inch))
            
            # Separador
            if i < 5:
                story.append(Paragraph("─" * 80, 
                                     ParagraphStyle('Sep', parent=normal_style, 
                                                  alignment=TA_CENTER, textColor=colors.grey)))
                story.append(Spacer(1, 0.15*inch))
        
        story.append(PageBreak())
        
        # ============ BOTTOM 5 - ADVERTENCIAS ============
        story.append(Paragraph("⚠️ BOTTOM 5 - ACTIVOS DE ALTO RIESGO", heading_style))
        story.append(Spacer(1, 0.2*inch))
        
        for i, result in enumerate(results[-5:][::-1], 1):
            rank = len(results) - 5 + i
            
            # Título del activo
            activo_title = f"⚠️ #{rank} - {result['activo']} ({result['ticker']})"
            story.append(Paragraph(activo_title, subheading_style))
            
            # Tabla de datos principales
            data_table = [
                ['Métrica', 'Valor'],
                ['Categoría', result['categoria']],
                ['Score de Rentabilidad', f"{result['score_rentabilidad']:.1f}/100"],
                ['Precio Actual', f"${result['precio_actual']:,.2f}"],
                ['Retorno Esperado', f"{result['retorno_esperado']:+.2f}%"],
                ['Dirección', f"{result['direccion']} ({result['confianza']:.0f}% confianza)"],
                ['Patrones', f"{result['patrones_alcistas']}↑ / {result['patrones_bajistas']}↓"]
            ]
            
            table = Table(data_table, colWidths=[2.5*inch, 3.5*inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#dc3545')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                ('BACKGROUND', (0, 1), (-1, -1), colors.lightcoral),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                ('FONTSIZE', (0, 1), (-1, -1), 9)
            ]))
            story.append(table)
            story.append(Spacer(1, 0.15*inch))
            
            # GRÁFICA DE EVOLUCIÓN TEMPORAL
            chart_path = self._generate_price_chart(result['ticker'], result['activo'], 
                                                     period=period, interval=interval)
            if chart_path and os.path.exists(chart_path):
                story.append(Paragraph("📉 EVOLUCIÓN TEMPORAL:", 
                                      ParagraphStyle('ChartTitle', parent=subheading_style, 
                                                   fontSize=11, textColor=colors.HexColor('#dc3545'))))
                story.append(Spacer(1, 0.1*inch))
                
                # Añadir imagen de la gráfica
                img = Image(chart_path, width=6*inch, height=3*inch)
                story.append(img)
                story.append(Spacer(1, 0.15*inch))
            
            # RAZÓN DE PRECAUCIÓN
            story.append(Paragraph("⚠️ MOTIVO DE PRECAUCIÓN:", 
                                  ParagraphStyle('PrecaucionTitle', parent=subheading_style, 
                                               fontSize=11, textColor=colors.HexColor('#dc3545'))))
            
            razon = self._generate_warning_reason(result)
            story.append(Paragraph(razon, normal_style))
            
            story.append(Spacer(1, 0.2*inch))
            
            if i < 5:
                story.append(Paragraph("─" * 80, 
                                     ParagraphStyle('Sep', parent=normal_style, 
                                                  alignment=TA_CENTER, textColor=colors.grey)))
                story.append(Spacer(1, 0.15*inch))
        
        story.append(PageBreak())
        
        # ============ RANKING COMPLETO ============
        story.append(Paragraph("📊 RANKING COMPLETO DE ACTIVOS", heading_style))
        story.append(Spacer(1, 0.2*inch))
        
        # Tabla resumen de todos los activos
        ranking_data = [['#', 'Activo', 'Categoría', 'Score', 'Retorno', 'Recomendación']]
        
        for i, r in enumerate(results, 1):
            ranking_data.append([
                str(i),
                f"{r['activo'][:15]}...",
                r['categoria'][:15],
                f"{r['score_rentabilidad']:.0f}",
                f"{r['retorno_esperado']:+.1f}%",
                r['recomendacion'][:15]
            ])
        
        ranking_table = Table(ranking_data, colWidths=[0.4*inch, 1.8*inch, 1.5*inch, 0.8*inch, 0.9*inch, 1.6*inch])
        ranking_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E86AB')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('FONTSIZE', (0, 1), (-1, -1), 7),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
        ]))
        story.append(ranking_table)
        
        story.append(PageBreak())
        
        # ============ RESUMEN Y CONCLUSIONES ============
        story.append(Paragraph("📈 RESUMEN Y CONCLUSIONES", heading_style))
        
        conclusiones = self._generate_conclusions(results)
        story.append(Paragraph(conclusiones, normal_style))
        
        # Pie de página
        story.append(Spacer(1, 0.5*inch))
        footer_text = """
        <i>Este reporte ha sido generado automáticamente mediante análisis técnico cuantitativo. 
        Las recomendaciones se basan en patrones históricos y análisis multi-factorial.
        No constituye asesoramiento financiero profesional. Consulte siempre con un asesor 
        certificado antes de tomar decisiones de inversión. Los resultados pasados no garantizan 
        rendimientos futuros.</i>
        """
        story.append(Paragraph(footer_text, 
                              ParagraphStyle('Footer', parent=normal_style, 
                                           fontSize=7, alignment=TA_CENTER, 
                                           textColor=colors.grey)))
        
        # Construir PDF
        doc.build(story)
        
        print(f"✅ Reporte PDF comparativo generado: {filepath}")
        return filepath
    
    def _generate_recommendation_reason(self, result: Dict) -> str:
        """Genera la razón detallada de por qué se recomienda invertir"""
        
        score = result['score_rentabilidad']
        direccion = result['direccion']
        confianza = result['confianza']
        rsi = result['rsi']
        tendencia = result['tendencia']
        volatilidad = result['volatilidad']
        patrones_alc = result['patrones_alcistas']
        patrones_baj = result['patrones_bajistas']
        retorno = result['retorno_esperado']
        
        razon = f"<b>Recomendación: {result['recomendacion']}</b><br/><br/>"
        
        # Razones positivas
        razones_positivas = []
        
        if score >= 70:
            razones_positivas.append(f"<b>Score excepcional de {score:.0f}/100</b>, indicando alta probabilidad de éxito")
        
        if direccion == 'Alcista' and confianza >= 70:
            razones_positivas.append(f"<b>Predicción alcista con {confianza:.0f}% de confianza</b> basada en análisis de patrones")
        
        if patrones_alc > patrones_baj and patrones_alc >= 3:
            razones_positivas.append(f"<b>Múltiples patrones alcistas detectados</b> ({patrones_alc} alcistas vs {patrones_baj} bajistas)")
        
        if rsi is not None:
            if rsi < 35:
                razones_positivas.append(f"<b>RSI en zona de sobreventa ({rsi:.0f})</b>, sugiere que el activo está infravalorado")
            elif 40 <= rsi <= 60:
                razones_positivas.append(f"<b>RSI en zona neutral ({rsi:.0f})</b>, indicando equilibrio saludable")
        
        if tendencia == 'Alcista':
            razones_positivas.append(f"<b>Tendencia técnica alcista confirmada</b>, momentum positivo")
        
        if volatilidad is not None and volatilidad < 2:
            razones_positivas.append(f"<b>Baja volatilidad ({volatilidad:.1f}%)</b>, menor riesgo de caídas bruscas")
        
        if retorno > 5:
            razones_positivas.append(f"<b>Retorno esperado atractivo de {retorno:+.1f}%</b> en el periodo analizado")
        
        # Construir texto
        if razones_positivas:
            razon += "<b>✅ Factores Favorables:</b><br/>"
            for i, r in enumerate(razones_positivas, 1):
                razon += f"{i}. {r}<br/>"
        
        # Factores a considerar
        factores_considerar = []
        
        if volatilidad is not None and volatilidad > 3:
            factores_considerar.append(f"Alta volatilidad ({volatilidad:.1f}%), usar gestión de riesgo")
        
        if patrones_baj > 0:
            factores_considerar.append(f"Presencia de {patrones_baj} patrón(es) bajista(s), monitorear de cerca")
        
        if rsi is not None and 60 <= rsi <= 70:
            factores_considerar.append(f"RSI acercándose a sobrecompra ({rsi:.0f}), considerar entrada gradual")
        
        if factores_considerar:
            razon += "<br/><b>⚠️ Factores a Considerar:</b><br/>"
            for i, f in enumerate(factores_considerar, 1):
                razon += f"{i}. {f}<br/>"
        
        # Estrategia sugerida
        razon += "<br/><b>💡 Estrategia Sugerida:</b><br/>"
        
        if score >= 75:
            razon += "Entrada con posición significativa (hasta 5% del portafolio). Stop loss al -3%. "
            razon += "Objetivo de beneficio: +10-15%."
        elif score >= 60:
            razon += "Entrada moderada (hasta 3% del portafolio). Stop loss al -2%. "
            razon += "Objetivo de beneficio: +7-10%."
        else:
            razon += "Entrada conservadora (hasta 2% del portafolio). Stop loss al -1.5%. "
            razon += "Revisar semanalmente."
        
        return razon
    
    def _generate_warning_reason(self, result: Dict) -> str:
        """Genera la razón detallada de por qué se recomienda precaución o venta"""
        
        score = result['score_rentabilidad']
        direccion = result['direccion']
        confianza = result['confianza']
        rsi = result['rsi']
        tendencia = result['tendencia']
        volatilidad = result['volatilidad']
        patrones_alc = result['patrones_alcistas']
        patrones_baj = result['patrones_bajistas']
        retorno = result['retorno_esperado']
        
        razon = f"<b>Advertencia: {result['recomendacion']}</b><br/><br/>"
        
        # Señales de alerta
        señales_alerta = []
        
        if score <= 25:
            señales_alerta.append(f"<b>Score crítico de {score:.0f}/100</b>, múltiples indicadores negativos")
        
        if direccion == 'Bajista' and confianza >= 60:
            señales_alerta.append(f"<b>Predicción bajista con {confianza:.0f}% de confianza</b>, alto riesgo de caídas")
        
        if patrones_baj > patrones_alc and patrones_baj >= 3:
            señales_alerta.append(f"<b>Predominio de patrones bajistas</b> ({patrones_baj} bajistas vs {patrones_alc} alcistas)")
        
        if rsi is not None and rsi > 70:
            señales_alerta.append(f"<b>RSI en sobrecompra ({rsi:.0f})</b>, activo sobrevalorado, corrección probable")
        
        if tendencia == 'Bajista':
            señales_alerta.append(f"<b>Tendencia técnica bajista</b>, momentum negativo confirmado")
        
        if volatilidad is not None and volatilidad > 5:
            señales_alerta.append(f"<b>Volatilidad extrema ({volatilidad:.1f}%)</b>, alto riesgo de pérdidas rápidas")
        
        if retorno < -3:
            señales_alerta.append(f"<b>Retorno esperado negativo ({retorno:+.1f}%)</b>, se anticipa caída de precio")
        
        # Construir texto
        if señales_alerta:
            razon += "<b>🚨 Señales de Alerta:</b><br/>"
            for i, s in enumerate(señales_alerta, 1):
                razon += f"{i}. {s}<br/>"
        
        # Recomendación de acción
        razon += "<br/><b>💼 Acción Recomendada:</b><br/>"
        
        if score <= 15:
            razon += "<b>VENTA INMEDIATA</b> si se posee este activo. "
            razon += "Proteger capital y reubicar en activos con mejor perspectiva. "
            razon += "Si está en pérdidas, evaluar corte de pérdidas vs esperar mejora (poco probable a corto plazo)."
        elif score <= 30:
            razon += "<b>REDUCIR EXPOSICIÓN</b> significativamente. "
            razon += "Vender al menos 70% de la posición. "
            razon += "Mantener solo si se cree en recuperación a largo plazo. "
            razon += "No aumentar posición bajo ninguna circunstancia."
        else:
            razon += "<b>MANTENER FUERA</b> del portafolio por ahora. "
            razon += "No entrar en nuevas posiciones. "
            razon += "Esperar mejora de indicadores técnicos antes de considerar. "
            razon += "Revisar en 2-3 semanas."
        
        # Condiciones para reconsiderar
        razon += "<br/><br/><b>✅ Condiciones para Reconsiderar:</b><br/>"
        razon += "• Score supere 50/100<br/>"
        razon += "• Aparezcan 3+ patrones alcistas<br/>"
        razon += "• RSI baje a zona 30-40<br/>"
        razon += "• Tendencia cambie a alcista<br/>"
        
        return razon
    
    def _calculate_expected_timeframe(self, result: Dict) -> str:
        """
        Calcula el tiempo estimado hasta alcanzar el retorno esperado
        
        Args:
            result: Diccionario con los datos del análisis
            
        Returns:
            Texto con el tiempo estimado
        """
        retorno = abs(result['retorno_esperado'])
        volatilidad = result.get('volatilidad', 2.0)
        confianza = result['confianza']
        score = result['score_rentabilidad']
        
        # Lógica de estimación basada en múltiples factores
        if score >= 80 and confianza >= 80:
            # Alta confianza y score: movimiento más rápido esperado
            if retorno >= 10:
                timeframe = "1-2 semanas"
            elif retorno >= 5:
                timeframe = "2-3 semanas"
            else:
                timeframe = "3-4 semanas"
        elif score >= 60 and confianza >= 60:
            # Confianza media: plazos moderados
            if retorno >= 10:
                timeframe = "2-4 semanas"
            elif retorno >= 5:
                timeframe = "1-2 meses"
            else:
                timeframe = "2-3 meses"
        else:
            # Baja confianza: plazos más largos
            if retorno >= 10:
                timeframe = "1-3 meses"
            elif retorno >= 5:
                timeframe = "2-4 meses"
            else:
                timeframe = "3-6 meses"
        
        # Ajustar por volatilidad
        if volatilidad and volatilidad > 4:
            # Alta volatilidad = potencialmente más rápido (pero más riesgoso)
            volatility_note = " (alta volatilidad: puede ser más rápido pero con mayor riesgo)"
        elif volatilidad and volatilidad < 1.5:
            # Baja volatilidad = movimientos más lentos
            volatility_note = " (baja volatilidad: movimiento gradual y estable)"
        else:
            volatility_note = ""
        
        return f"{timeframe}{volatility_note}"
    
    def _get_key_news(self, asset_name: str, max_news: int = 3) -> List[Dict]:
        """
        Obtiene noticias clave relacionadas con el activo
        
        Args:
            asset_name: Nombre del activo
            max_news: Número máximo de noticias a obtener
            
        Returns:
            Lista de diccionarios con noticias
        """
        try:
            print(f"   🔍 Obteniendo noticias para {asset_name}...")
            news_analyzer = NewsAnalyzer(asset_name)
            noticias_raw = news_analyzer.fetch_news(max_news=max_news)
            
            noticias = []
            for noticia in noticias_raw[:max_news]:
                noticias.append({
                    'titulo': noticia.get('titulo', 'Sin título')[:100],
                    'descripcion': noticia.get('descripcion', 'No description available')[:250],
                    'link': noticia.get('link', ''),
                    'fecha': noticia.get('fecha', 'N/A')
                })
            
            print(f"   ✅ Obtenidas {len(noticias)} noticias para {asset_name}")
            return noticias
        except Exception as e:
            print(f"   ⚠️ Error obteniendo noticias para {asset_name}: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def _generate_distribution_chart(self, results: List[Dict]) -> str:
        """Genera gráfico de distribución de categorías"""
        
        # Contar por categoría
        categorias = {}
        for r in results:
            cat = r['categoria']
            categorias[cat] = categorias.get(cat, 0) + 1
        
        # Crear figura
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # Gráfico de barras
        cats = list(categorias.keys())
        counts = list(categorias.values())
        colors_map = {
            '🟢 MUY ALCISTA': '#28a745',
            '🟢 ALCISTA': '#5cb85c',
            '🟡 NEUTRAL-ALCISTA': '#ffc107',
            '🟡 NEUTRAL': '#ffd700',
            '🟠 NEUTRAL-BAJISTA': '#ff8c00',
            '🔴 BAJISTA': '#dc3545',
            '🔴 MUY BAJISTA': '#8b0000'
        }
        colors_list = [colors_map.get(c, '#cccccc') for c in cats]
        
        ax1.barh(cats, counts, color=colors_list, edgecolor='black', linewidth=1.5)
        ax1.set_xlabel('Número de Activos', fontsize=11, fontweight='bold')
        ax1.set_title('Distribución por Categoría', fontsize=13, fontweight='bold')
        ax1.grid(axis='x', alpha=0.3)
        
        # Gráfico circular
        ax2.pie(counts, labels=cats, autopct='%1.0f%%', colors=colors_list,
               startangle=90, textprops={'fontsize': 8})
        ax2.set_title('Proporción de Categorías', fontsize=13, fontweight='bold')
        
        plt.tight_layout()
        
        # Guardar
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        chart_path = os.path.join(self.output_dir, f"distribucion_categorias_{timestamp}.png")
        plt.savefig(chart_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        return chart_path
    
    def _generate_conclusions(self, results: List[Dict]) -> str:
        """Genera conclusiones generales del análisis"""
        
        total = len(results)
        
        # Estadísticas
        alcistas = len([r for r in results if 'ALCISTA' in r['categoria'] and 'BAJISTA' not in r['categoria']])
        bajistas = len([r for r in results if 'BAJISTA' in r['categoria']])
        neutrales = total - alcistas - bajistas
        
        avg_score = sum(r['score_rentabilidad'] for r in results) / total
        avg_retorno = sum(r['retorno_esperado'] for r in results) / total
        
        top_3 = results[:3]
        bottom_3 = results[-3:]
        
        conclusiones = f"""
        <b>Análisis de {total} activos financieros completado.</b><br/><br/>
        
        <b>📊 Panorama General del Mercado:</b><br/>
        • {alcistas} activos ({alcistas/total*100:.0f}%) muestran señales alcistas<br/>
        • {bajistas} activos ({bajistas/total*100:.0f}%) muestran señales bajistas<br/>
        • {neutrales} activos ({neutrales/total*100:.0f}%) en posición neutral<br/><br/>
        
        <b>💡 Score Promedio:</b> {avg_score:.1f}/100<br/>
        <b>📈 Retorno Esperado Promedio:</b> {avg_retorno:+.2f}%<br/><br/>
        
        <b>🎯 Recomendaciones Principales:</b><br/><br/>
        
        <b>PRIORIDAD ALTA - Considerar fuertemente:</b><br/>
        """
        
        for i, r in enumerate(top_3, 1):
            conclusiones += f"{i}. <b>{r['activo']}</b> - Score {r['score_rentabilidad']:.0f}, "
            conclusiones += f"Retorno esperado {r['retorno_esperado']:+.1f}%<br/>"
        
        conclusiones += f"""
        <br/><b>EVITAR o REDUCIR:</b><br/>
        """
        
        for i, r in enumerate(bottom_3, 1):
            conclusiones += f"{i}. <b>{r['activo']}</b> - Score {r['score_rentabilidad']:.0f}, "
            conclusiones += f"Múltiples señales negativas<br/>"
        
        # Recomendación final
        if avg_score > 55:
            sentiment = "optimista"
            action = "Es un buen momento para buscar oportunidades de compra en los activos mejor rankeados."
        elif avg_score > 45:
            sentiment = "neutral"
            action = "Mercado en equilibrio. Ser selectivo y enfocarse solo en los activos con score > 60."
        else:
            sentiment = "cauteloso"
            action = "Prevalece la cautela. Considerar mantener cash hasta que mejoren las condiciones."
        
        conclusiones += f"""
        <br/><br/><b>🔮 Perspectiva General:</b><br/>
        El análisis sugiere un panorama <b>{sentiment}</b> para los activos analizados. 
        {action}<br/><br/>
        
        <b>⚖️ Gestión de Riesgo:</b><br/>
        • No invertir más del 25% del capital en un solo activo<br/>
        • Diversificar entre los 3-5 mejores oportunidades<br/>
        • Usar siempre stop loss (recomendado: 2-3%)<br/>
        • Revisar posiciones semanalmente<br/><br/>
        
        <b>📅 Próximos Pasos:</b><br/>
        1. Ejecutar análisis individual de los top 3 para detalles<br/>
        2. Revisar noticias recientes de los activos seleccionados<br/>
        3. Establecer puntos de entrada y salida<br/>
        4. Configurar alertas de precio<br/>
        5. Repetir análisis comparativo semanalmente
        """
        
        return conclusiones
    
    def _generate_price_chart(self, ticker: str, asset_name: str, period: str = "3mo", interval: str = "1d") -> str:
        """
        Genera gráfica de evolución temporal del precio (sin gaps visuales)
        
        Args:
            ticker: Símbolo del activo
            asset_name: Nombre del activo
            period: Periodo a graficar (1mo, 3mo, 6mo, 1y, 7d, etc.)
            interval: Intervalo de muestreo (1m, 5m, 15m, 1h, 1d, etc.)
            
        Returns:
            Ruta del archivo de imagen generado
        """
        try:
            print(f"   📊 Generando gráfico para {asset_name} ({ticker})...")
            
            # Obtener datos
            stock = yf.Ticker(ticker)
            data = stock.history(period=period, interval=interval)
            
            if data is None or len(data) == 0:
                print(f"   ⚠️ No se pudieron obtener datos para {asset_name}")
                return None
            
            if len(data) < 5:
                print(f"   ⚠️ Datos insuficientes para {asset_name}: {len(data)} registros (mínimo 5)")
                return None
            
            print(f"   📈 Datos obtenidos: {len(data)} registros")
            
            # Crear gráfica
            fig, ax = plt.subplots(figsize=(8, 4))
            
            # Usar índice numérico para evitar gaps visuales en intervalos pequeños
            use_numeric_index = interval in ['1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h']
            
            if use_numeric_index:
                # Gráfica sin gaps (índice numérico)
                x_values = range(len(data))
                ax.plot(x_values, data['Close'].values, color='#2E86AB', linewidth=1.5, label='Precio')
                
                # Media móvil 20 periodos
                if len(data) >= 20:
                    sma_20 = data['Close'].rolling(window=20).mean()
                    ax.plot(x_values, sma_20.values, color='#FFA500', linewidth=1.2, 
                           linestyle='--', label='SMA 20', alpha=0.7)
                
                # Media móvil 50 periodos
                if len(data) >= 50:
                    sma_50 = data['Close'].rolling(window=50).mean()
                    ax.plot(x_values, sma_50.values, color='#DC143C', linewidth=1.2, 
                           linestyle='--', label='SMA 50', alpha=0.7)
                
                # Configurar etiquetas del eje X mostrando fechas reales
                num_labels = min(10, len(data))  # Máximo 10 etiquetas
                step = max(1, len(data) // num_labels)
                tick_positions = list(range(0, len(data), step))
                tick_labels = [data.index[i].strftime('%d/%m %H:%M') if interval in ['1m', '2m', '5m', '15m', '30m'] 
                              else data.index[i].strftime('%d/%m/%y') 
                              for i in tick_positions]
                ax.set_xticks(tick_positions)
                ax.set_xticklabels(tick_labels, rotation=45, ha='right')
                ax.set_xlabel('Tiempo (solo datos disponibles)', fontsize=11)
                
            else:
                # Gráfica tradicional con fechas (para intervalos diarios)
                ax.plot(data.index, data['Close'], color='#2E86AB', linewidth=2, label='Precio')
                
                # Media móvil 20 días
                if len(data) >= 20:
                    sma_20 = data['Close'].rolling(window=20).mean()
                    ax.plot(data.index, sma_20, color='#FFA500', linewidth=1.5, 
                           linestyle='--', label='SMA 20', alpha=0.7)
                
                # Media móvil 50 días
                if len(data) >= 50:
                    sma_50 = data['Close'].rolling(window=50).mean()
                    ax.plot(data.index, sma_50, color='#DC143C', linewidth=1.5, 
                           linestyle='--', label='SMA 50', alpha=0.7)
                
                plt.xticks(rotation=45, ha='right')
                ax.set_xlabel('Fecha', fontsize=11)
            
            # Formato común
            ax.set_title(f'Evolución de {asset_name} - {period} ({interval})', 
                        fontsize=14, fontweight='bold', pad=15)
            ax.set_ylabel('Precio ($)', fontsize=11)
            ax.grid(True, alpha=0.3, linestyle=':', linewidth=0.7)
            ax.legend(loc='best', fontsize=10)
            
            # Formato del eje Y con formato de moneda
            from matplotlib.ticker import FuncFormatter
            def currency_formatter(x, p):
                return f'${x:,.0f}' if x >= 100 else f'${x:.2f}'
            ax.yaxis.set_major_formatter(FuncFormatter(currency_formatter))
            
            # Ajustar diseño
            plt.tight_layout()
            
            # Asegurar que el directorio existe
            os.makedirs(self.output_dir, exist_ok=True)
            
            # Guardar
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            chart_path = os.path.join(self.output_dir, f"chart_{ticker}_{timestamp}.png")
            plt.savefig(chart_path, dpi=150, bbox_inches='tight', facecolor='white')
            plt.close()
            
            print(f"   ✅ Gráfico guardado: {chart_path}")
            
            return chart_path
            
        except Exception as e:
            print(f"   ⚠️ Error generando gráfica para {asset_name}: {e}")
            import traceback
            traceback.print_exc()
            return None
