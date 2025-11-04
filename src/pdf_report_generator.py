"""
Generador de reportes PDF con gráficos embebidos
"""
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak
from reportlab.platypus import Table, TableStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from datetime import datetime
import os
from typing import Dict, List


class PDFReportGenerator:
    """Clase para generar reportes PDF con gráficos y análisis"""
    
    def __init__(self, output_dir: str = "outputs/reports"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
    def generate_complete_pdf_report(self, asset_name: str, analysis_results: Dict,
                                     graph_paths: List[str]) -> str:
        """
        Genera un reporte PDF completo con gráficos embebidos
        
        Args:
            asset_name: Nombre del activo
            analysis_results: Resultados del análisis
            graph_paths: Lista de rutas a los gráficos generados
            
        Returns:
            Ruta del archivo PDF generado
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"Reporte_{asset_name.replace(' ', '_')}_{timestamp}.pdf"
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
            fontSize=24,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading1'],
            fontSize=16,
            textColor=colors.HexColor('#2E86AB'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        )
        
        subheading_style = ParagraphStyle(
            'CustomSubHeading',
            parent=styles['Heading2'],
            fontSize=13,
            textColor=colors.HexColor('#555555'),
            spaceAfter=8,
            fontName='Helvetica-Bold'
        )
        
        normal_style = ParagraphStyle(
            'CustomNormal',
            parent=styles['Normal'],
            fontSize=10,
            alignment=TA_JUSTIFY,
            spaceAfter=8
        )
        
        # ============ PORTADA ============
        story.append(Spacer(1, 1*inch))
        story.append(Paragraph(f"📊 REPORTE DE ANÁLISIS FINANCIERO", title_style))
        story.append(Spacer(1, 0.3*inch))
        story.append(Paragraph(f"<b>{asset_name}</b>", 
                              ParagraphStyle('AssetTitle', parent=title_style, fontSize=20)))
        story.append(Spacer(1, 0.5*inch))
        
        fecha_actual = datetime.now().strftime("%d de %B de %Y - %H:%M")
        story.append(Paragraph(f"Fecha de generación: {fecha_actual}", 
                              ParagraphStyle('DateStyle', parent=normal_style, 
                                           alignment=TA_CENTER, fontSize=11)))
        
        story.append(Spacer(1, 0.5*inch))
        
        # Resumen ejecutivo
        story.append(Paragraph("RESUMEN EJECUTIVO", heading_style))
        
        predicciones = analysis_results.get('predicciones', {})
        if predicciones:
            direccion = predicciones.get('direccion_probable', 'N/A')
            confianza = predicciones.get('confianza', 0)
            
            resumen_color = '#28a745' if direccion == 'Alcista' else '#dc3545' if direccion == 'Bajista' else '#ffc107'
            
            resumen_text = f"""
            <b>Dirección Probable:</b> <font color="{resumen_color}">{direccion}</font><br/>
            <b>Nivel de Confianza:</b> {confianza:.1f}%<br/>
            <b>Patrones Detectados:</b> {len(analysis_results.get('patrones', {}).get('todos', []))}<br/>
            <b>Noticias Analizadas:</b> {len(analysis_results.get('noticias', []))}
            """
            story.append(Paragraph(resumen_text, normal_style))
        
        story.append(PageBreak())
        
        # ============ GRÁFICOS ============
        story.append(Paragraph("ANÁLISIS GRÁFICO", heading_style))
        
        for i, graph_path in enumerate(graph_paths):
            if os.path.exists(graph_path):
                try:
                    # Ajustar tamaño de imagen
                    img = Image(graph_path, width=7*inch, height=4.5*inch)
                    story.append(img)
                    story.append(Spacer(1, 0.3*inch))
                    
                    if i < len(graph_paths) - 1:  # No romper página en el último gráfico
                        story.append(PageBreak())
                except Exception as e:
                    print(f"⚠️ Error al incluir gráfico {graph_path}: {e}")
        
        story.append(PageBreak())
        
        # ============ ANÁLISIS TÉCNICO ============
        story.append(Paragraph("ANÁLISIS TÉCNICO DETALLADO", heading_style))
        
        market_data = analysis_results.get('market_data', {})
        if market_data:
            story.append(Paragraph("Indicadores Técnicos", subheading_style))
            
            stats = market_data.get('statistics', {})
            
            # Función auxiliar para formatear valores que pueden ser None
            def format_price(val):
                return f"${val:.2f}" if val and val > 0 else "N/A"
            
            def format_percent(val):
                return f"{val:.2f}%" if val and val > 0 else "N/A"
            
            def format_number(val):
                return f"{val:.2f}" if val and val > 0 else "N/A"
            
            indicators_data = [
                ['Indicador', 'Valor'],
                ['Precio Actual', format_price(stats.get('current_price', 0))],
                ['Media 20 días', format_price(stats.get('sma_20'))],
                ['Media 50 días', format_price(stats.get('sma_50'))],
                ['RSI', format_number(stats.get('rsi'))],
                ['Volatilidad', format_percent(stats.get('volatility'))],
                ['Tendencia', stats.get('trend', 'N/A')]
            ]
            
            indicators_table = Table(indicators_data, colWidths=[3*inch, 3*inch])
            indicators_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E86AB')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(indicators_table)
            story.append(Spacer(1, 0.3*inch))
        
        # ============ PATRONES DETECTADOS ============
        story.append(Paragraph("PATRONES TÉCNICOS IDENTIFICADOS", heading_style))
        
        patrones = analysis_results.get('patrones', {})
        patrones_todos = patrones.get('todos', [])
        
        if patrones_todos:
            story.append(Paragraph(f"Total de patrones detectados: {len(patrones_todos)}", subheading_style))
            
            # Agrupar por tipo
            alcistas = [p for p in patrones_todos if p.get('tipo') == 'Alcista' or p.get('señal') == 'Alcista']
            bajistas = [p for p in patrones_todos if p.get('tipo') == 'Bajista' or p.get('señal') == 'Bajista']
            
            patron_summary = f"""
            <b>📈 Patrones Alcistas:</b> {len(alcistas)}<br/>
            <b>📉 Patrones Bajistas:</b> {len(bajistas)}<br/>
            <b>➡️ Patrones Neutrales:</b> {len(patrones_todos) - len(alcistas) - len(bajistas)}
            """
            story.append(Paragraph(patron_summary, normal_style))
            story.append(Spacer(1, 0.2*inch))
            
            # Tabla de patrones recientes (top 10)
            story.append(Paragraph("Patrones Más Recientes:", subheading_style))
            
            patrones_recientes = sorted(patrones_todos, 
                                       key=lambda x: x['fecha'], reverse=True)[:10]
            
            patron_data = [['Fecha', 'Patrón', 'Tipo', 'Señal']]
            for p in patrones_recientes:
                fecha_str = p['fecha'].strftime('%d/%m/%Y') if hasattr(p['fecha'], 'strftime') else str(p['fecha'])
                patron_nombre = p.get('patron', p.get('tipo', 'N/A'))
                tipo = p.get('tipo', p.get('señal', 'Neutral'))
                fuerza = p.get('fuerza', p.get('intensidad', 'N/A'))
                
                patron_data.append([fecha_str, patron_nombre, tipo, str(fuerza)])
            
            patrones_table = Table(patron_data, colWidths=[1.5*inch, 2.5*inch, 1.5*inch, 1.5*inch])
            patrones_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E86AB')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
                ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
            ]))
            
            story.append(patrones_table)
        
        story.append(PageBreak())
        
        # ============ PREDICCIONES ============
        story.append(Paragraph("PREDICCIONES Y ESCENARIOS", heading_style))
        
        if predicciones:
            story.append(Paragraph("Proyección de Precio", subheading_style))
            
            rango = predicciones.get('rango_precio_estimado', {})
            pred_text = f"""
            <b>Precio Objetivo:</b> ${rango.get('objetivo', 0):.2f}<br/>
            <b>Rango Mínimo:</b> ${rango.get('minimo', 0):.2f}<br/>
            <b>Rango Máximo:</b> ${rango.get('maximo', 0):.2f}<br/>
            <b>Confianza:</b> {predicciones.get('confianza', 0):.1f}%
            """
            story.append(Paragraph(pred_text, normal_style))
            story.append(Spacer(1, 0.2*inch))
            
            # Escenarios
            escenarios = predicciones.get('escenarios', [])
            if escenarios:
                story.append(Paragraph("Escenarios Posibles:", subheading_style))
                
                escenarios_data = [['Escenario', 'Precio Objetivo', 'Probabilidad', 'Descripción']]
                for esc in escenarios:
                    descripcion = esc.get('descripcion', esc.get('fundamento', 'N/A'))
                    escenarios_data.append([
                        esc['nombre'],
                        f"${esc['precio_objetivo']:.2f}",
                        f"{esc['probabilidad']:.0f}%",
                        descripcion[:50] + "..." if len(descripcion) > 50 else descripcion
                    ])
                
                escenarios_table = Table(escenarios_data, colWidths=[1.5*inch, 1.5*inch, 1.2*inch, 2.8*inch])
                escenarios_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#28a745')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, -1), 8),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.lightgreen),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.black)
                ]))
                
                story.append(escenarios_table)
        
        story.append(PageBreak())
        
        # ============ ANÁLISIS DE NOTICIAS ============
        story.append(Paragraph("ANÁLISIS DE SENTIMIENTO DE NOTICIAS", heading_style))
        
        noticias = analysis_results.get('noticias', [])
        if noticias:
            story.append(Paragraph(f"Total de noticias analizadas: {len(noticias)}", subheading_style))
            
            # Calcular sentimiento promedio
            sentimientos = []
            for n in noticias:
                sent = n.get('sentimiento', 0)
                # Si sentimiento es un diccionario, extraer polaridad; si no, usar directamente
                if isinstance(sent, dict):
                    sentimientos.append(sent.get('polaridad', 0))
                else:
                    sentimientos.append(sent if isinstance(sent, (int, float)) else 0)
            
            sent_promedio = sum(sentimientos) / len(sentimientos) if sentimientos else 0
            
            sent_text = f"""
            <b>Sentimiento Promedio:</b> {sent_promedio:.3f}<br/>
            <b>Interpretación:</b> {'Positivo' if sent_promedio > 0.1 else 'Negativo' if sent_promedio < -0.1 else 'Neutral'}
            """
            story.append(Paragraph(sent_text, normal_style))
            story.append(Spacer(1, 0.2*inch))
            
            # Identificar noticias de alto impacto (sentimiento extremo = mayor impacto)
            noticias_con_impacto = []
            for noticia in noticias:
                sent = noticia.get('sentimiento', 0)
                if isinstance(sent, dict):
                    polaridad = sent.get('polaridad', 0)
                else:
                    polaridad = sent if isinstance(sent, (int, float)) else 0
                
                # Calcular impacto: abs(polaridad) + subjetividad
                subjetividad = noticia.get('subjetividad', 0)
                impacto = abs(polaridad) + (subjetividad * 0.3)  # Peso 30% a subjetividad
                
                noticias_con_impacto.append({
                    **noticia,
                    'polaridad_calc': polaridad,
                    'impacto': impacto
                })
            
            # Ordenar por impacto (mayor primero)
            noticias_con_impacto.sort(key=lambda x: x['impacto'], reverse=True)
            
            # Noticias de ALTO IMPACTO (top 5 por impacto)
            story.append(Paragraph("🔥 NOTICIAS DE ALTO IMPACTO:", subheading_style))
            story.append(Spacer(1, 0.1*inch))
            
            for i, noticia in enumerate(noticias_con_impacto[:5], 1):
                titulo = noticia.get('titulo', 'Sin título')
                fecha = noticia.get('fecha', 'Fecha desconocida')
                if isinstance(fecha, datetime):
                    fecha = fecha.strftime('%d/%m/%Y %H:%M')
                fuente = noticia.get('fuente', 'Fuente desconocida')
                link = noticia.get('link', '')
                polaridad = noticia.get('polaridad_calc', 0)
                impacto = noticia.get('impacto', 0)
                descripcion = noticia.get('descripcion', '')
                
                # Emoji según sentimiento
                if polaridad > 0.2:
                    sent_emoji = '🚀'
                    sent_label = 'MUY POSITIVO'
                    color = '#28a745'
                elif polaridad > 0.05:
                    sent_emoji = '😊'
                    sent_label = 'POSITIVO'
                    color = '#5cb85c'
                elif polaridad < -0.2:
                    sent_emoji = '⚠️'
                    sent_label = 'MUY NEGATIVO'
                    color = '#dc3545'
                elif polaridad < -0.05:
                    sent_emoji = '😟'
                    sent_label = 'NEGATIVO'
                    color = '#ff6b6b'
                else:
                    sent_emoji = '😐'
                    sent_label = 'NEUTRAL'
                    color = '#6c757d'
                
                # Traducir y resumir descripción al español (3-4 líneas máximo)
                descripcion_resumen = self._resumir_descripcion(descripcion, titulo)
                
                # Crear texto con hipervínculo y descripción
                if link:
                    noticia_text = f"""
                    <b>{sent_emoji} #{i} - {titulo}</b><br/>
                    <font color="{color}"><b>Impacto: {impacto:.3f} | Sentimiento: {sent_label} ({polaridad:.3f})</b></font><br/>
                    <i>📰 {fuente} | 📅 {fecha}</i><br/>
                    <br/>
                    <b>📝 Resumen:</b><br/>
                    <i>{descripcion_resumen}</i><br/>
                    <br/>
                    <b><a href="{link}" color="blue">🔗 Leer noticia completa</a></b>
                    """
                else:
                    noticia_text = f"""
                    <b>{sent_emoji} #{i} - {titulo}</b><br/>
                    <font color="{color}"><b>Impacto: {impacto:.3f} | Sentimiento: {sent_label} ({polaridad:.3f})</b></font><br/>
                    <i>📰 {fuente} | 📅 {fecha}</i><br/>
                    <br/>
                    <b>📝 Resumen:</b><br/>
                    <i>{descripcion_resumen}</i><br/>
                    <br/>
                    <i>(Sin enlace disponible)</i>
                    """
                
                story.append(Paragraph(noticia_text, normal_style))
                story.append(Spacer(1, 0.25*inch))
            
            # Separador
            story.append(Spacer(1, 0.2*inch))
            story.append(Paragraph("─" * 80, 
                                 ParagraphStyle('Sep', parent=normal_style, 
                                              alignment=TA_CENTER, textColor=colors.grey)))
            story.append(Spacer(1, 0.2*inch))
            
            # Noticias recientes (resto, ordenadas por fecha)
            otras_noticias = noticias_con_impacto[5:]
            if otras_noticias:
                story.append(Paragraph("📰 OTRAS NOTICIAS RECIENTES:", subheading_style))
                story.append(Spacer(1, 0.1*inch))
                
                for noticia in otras_noticias[:10]:  # Mostrar hasta 10 más
                    titulo = noticia.get('titulo', 'Sin título')
                    fecha = noticia.get('fecha', 'Fecha desconocida')
                    if isinstance(fecha, datetime):
                        fecha = fecha.strftime('%d/%m/%Y %H:%M')
                    fuente = noticia.get('fuente', 'Fuente desconocida')
                    link = noticia.get('link', '')
                    polaridad = noticia.get('polaridad_calc', 0)
                    
                    sent_emoji = '😊' if polaridad > 0.05 else '😟' if polaridad < -0.05 else '😐'
                    
                    if link:
                        noticia_text = f"""
                        <b>{sent_emoji} {titulo}</b><br/>
                        <i>{fuente} | {fecha}</i> | 
                        <a href="{link}" color="blue">🔗 Ver noticia</a>
                        """
                    else:
                        noticia_text = f"""
                        <b>{sent_emoji} {titulo}</b><br/>
                        <i>{fuente} | {fecha}</i>
                        """
                    
                    story.append(Paragraph(noticia_text, normal_style))
                    story.append(Spacer(1, 0.12*inch))
        
        story.append(PageBreak())
        
        # ============ CONCLUSIONES ============
        story.append(Paragraph("CONCLUSIONES Y RECOMENDACIONES", heading_style))
        
        conclusion_text = self._generate_conclusions(analysis_results)
        story.append(Paragraph(conclusion_text, normal_style))
        
        # Pie de página
        story.append(Spacer(1, 0.5*inch))
        footer_text = """
        <i>Este reporte ha sido generado automáticamente mediante análisis técnico y de sentimiento. 
        No constituye asesoramiento financiero. Consulte siempre con un profesional antes de tomar 
        decisiones de inversión.</i>
        """
        story.append(Paragraph(footer_text, 
                              ParagraphStyle('Footer', parent=normal_style, 
                                           fontSize=8, alignment=TA_CENTER, 
                                           textColor=colors.grey)))
        
        # Construir PDF
        doc.build(story)
        
        print(f"✅ Reporte PDF generado: {filepath}")
        return filepath
    
    def _resumir_descripcion(self, descripcion: str, titulo: str = "", max_chars: int = 350) -> str:
        """
        Resume y limpia la descripción de una noticia (mantiene idioma original)
        
        Args:
            descripcion: Texto original de la descripción
            titulo: Título de la noticia (usado como fallback)
            max_chars: Número máximo de caracteres
            
        Returns:
            Descripción resumida y limpia
        """
        # Si no hay descripción o es muy corta, generar una breve a partir del título
        if not descripcion or len(descripcion) < 20:
            if titulo:
                return f"Related news: {titulo}"
            else:
                return "News content available at the link."
        
        # Limpiar HTML si existe
        from html import unescape
        descripcion = unescape(descripcion)
        
        # Eliminar tags HTML básicos
        import re
        descripcion = re.sub(r'<[^>]+>', '', descripcion)  # Eliminar todos los tags HTML
        
        # Limpiar espacios múltiples
        descripcion = re.sub(r'\s+', ' ', descripcion).strip()
        
        # Truncar
        if len(descripcion) > max_chars:
            truncated = descripcion[:max_chars]
            last_period = truncated.rfind('.')
            
            if last_period > max_chars * 0.7:
                descripcion = truncated[:last_period + 1]
            else:
                last_space = truncated.rfind(' ')
                if last_space > 0:
                    descripcion = truncated[:last_space] + '...'
                else:
                    descripcion = truncated + '...'
        
        return descripcion
    
    def _traducir_texto(self, texto: str) -> str:
        """
        Traduce texto al español usando traducción simple de términos comunes
        
        Args:
            texto: Texto a traducir
            
        Returns:
            Texto en español
        """
        if not texto or len(texto.strip()) < 3:
            return texto
        
        # Detectar si ya está en español
        palabras_esp = ['el', 'la', 'de', 'que', 'en', 'y', 'a', 'los', 'del', 'se', 'las', 'por', 'un', 'una', 'con', 'no', 'su', 'para', 'es', 'al']
        palabras_texto = texto.lower().split()[:20]
        palabras_esp_encontradas = sum(1 for p in palabras_texto if p in palabras_esp)
        
        if palabras_esp_encontradas > len(palabras_texto) * 0.3:
            return texto  # Ya está en español
        
        # Diccionario de traducción para términos financieros y comunes
        traducciones = {
            # Términos financieros
            'price': 'precio',
            'prices': 'precios',
            'market': 'mercado',
            'markets': 'mercados',
            'stock': 'acción',
            'stocks': 'acciones',
            'trading': 'comercio',
            'trade': 'comerciar',
            'trader': 'comerciante',
            'traders': 'comerciantes',
            'volume': 'volumen',
            'cryptocurrency': 'criptomoneda',
            'cryptocurrencies': 'criptomonedas',
            'crypto': 'cripto',
            'bitcoin': 'Bitcoin',
            'btc': 'BTC',
            'ethereum': 'Ethereum',
            'eth': 'ETH',
            'blockchain': 'blockchain',
            'investment': 'inversión',
            'investments': 'inversiones',
            'investor': 'inversor',
            'investors': 'inversores',
            'rally': 'repunte',
            'surge': 'aumento',
            'plunge': 'caída',
            'plunges': 'cae',
            'crash': 'colapso',
            'crashes': 'colapsa',
            'bull': 'alcista',
            'bear': 'bajista',
            'profit': 'beneficio',
            'profits': 'beneficios',
            'loss': 'pérdida',
            'losses': 'pérdidas',
            'gain': 'ganancia',
            'gains': 'ganancias',
            'decline': 'descenso',
            'declines': 'desciende',
            'rise': 'subida',
            'rises': 'sube',
            'fall': 'caída',
            'falls': 'cae',
            'falling': 'cayendo',
            'rising': 'subiendo',
            
            # Verbos comunes
            'reaches': 'alcanza',
            'reach': 'alcanzar',
            'reached': 'alcanzó',
            'hits': 'golpea',
            'hit': 'golpear',
            'breaks': 'rompe',
            'break': 'romper',
            'broke': 'rompió',
            'announces': 'anuncia',
            'announce': 'anunciar',
            'announced': 'anunció',
            'reports': 'reporta',
            'report': 'informe',
            'reported': 'reportó',
            'says': 'dice',
            'say': 'decir',
            'said': 'dijo',
            'shows': 'muestra',
            'show': 'mostrar',
            'showed': 'mostró',
            'reveals': 'revela',
            'reveal': 'revelar',
            'revealed': 'reveló',
            'outlines': 'esboza',
            'outline': 'esbozar',
            'outlined': 'esbozó',
            'fails': 'falla',
            'fail': 'fallar',
            'failed': 'falló',
            'can': 'puede',
            'could': 'podría',
            'will': 'va',
            'would': 'haría',
            'may': 'puede',
            'might': 'podría',
            
            # Palabras comunes
            'new': 'nuevo',
            'old': 'viejo',
            'high': 'alto',
            'higher': 'más alto',
            'highest': 'más alto',
            'low': 'bajo',
            'lower': 'más bajo',
            'lowest': 'más bajo',
            'record': 'récord',
            'records': 'récords',
            'analysis': 'análisis',
            'data': 'datos',
            'news': 'noticias',
            'article': 'artículo',
            'articles': 'artículos',
            'related': 'relacionado',
            'available': 'disponible',
            'content': 'contenido',
            'link': 'enlace',
            'links': 'enlaces',
            'ways': 'formas',
            'way': 'forma',
            'toward': 'hacia',
            'towards': 'hacia',
            'over': 'sobre',
            'under': 'bajo',
            'with': 'con',
            'without': 'sin',
            'about': 'sobre',
            'after': 'después',
            'before': 'antes',
            'during': 'durante',
            'through': 'a través',
            'against': 'contra',
            'between': 'entre',
            'among': 'entre',
            'into': 'en',
            'from': 'desde',
            'by': 'por',
            'at': 'en',
            'on': 'en',
            'in': 'en',
            'as': 'como',
            'morning': 'mañana',
            'afternoon': 'tarde',
            'evening': 'noche',
            'night': 'noche',
            'day': 'día',
            'week': 'semana',
            'month': 'mes',
            'year': 'año',
            
            # Organizaciones y términos específicos
            'ceo': 'director ejecutivo',
            'nasdaq': 'Nasdaq',
            'sanctions': 'sanciones',
            'bankers': 'banqueros',
            'banker': 'banquero',
            'laundering': 'lavado',
            'tied': 'vinculado',
            'cyberattacks': 'ciberataques',
            'cyberattack': 'ciberataque',
            'north': 'norte',
            'korean': 'coreano',
            'finance': 'finanzas',
            'financial': 'financiero',
            'fix': 'arreglar',
            'fixes': 'arregla',
            'fixed': 'arregló',
            'bounce': 'rebote',
            'bounces': 'rebota',
            'bounced': 'rebotó',
            'careens': 'se precipita'
        }
        
        # Traducir palabra por palabra preservando puntuación
        palabras = texto.split()
        palabras_traducidas = []
        
        for palabra in palabras:
            # Separar puntuación
            palabra_limpia = palabra.lower().strip('.,;:!?¿¡"\'()[]{}')
            puntuacion = palabra[len(palabra_limpia):] if palabra_limpia else ''
            
            # Traducir si existe en el diccionario
            if palabra_limpia in traducciones:
                # Mantener capitalización original
                if palabra[0].isupper() and len(palabra) > 0:
                    palabra_traducida = traducciones[palabra_limpia].capitalize()
                else:
                    palabra_traducida = traducciones[palabra_limpia]
                palabras_traducidas.append(palabra_traducida + puntuacion)
            else:
                palabras_traducidas.append(palabra)
        
        return ' '.join(palabras_traducidas)
    
    def _generate_conclusions(self, analysis_results: Dict) -> str:
        """Genera conclusiones basadas en el análisis"""
        
        predicciones = analysis_results.get('predicciones', {})
        direccion = predicciones.get('direccion_probable', 'Neutral')
        confianza = predicciones.get('confianza', 0)
        
        patrones = analysis_results.get('patrones', {})
        num_patrones = len(patrones.get('todos', []))
        
        noticias = analysis_results.get('noticias', [])
        
        # Calcular sentimiento de noticias (manejar dict o float)
        sentimientos_list = []
        for n in noticias:
            sent = n.get('sentimiento', 0)
            if isinstance(sent, dict):
                sentimientos_list.append(sent.get('polaridad', 0))
            else:
                sentimientos_list.append(sent if isinstance(sent, (int, float)) else 0)
        
        sentimiento_noticias = sum(sentimientos_list) / len(sentimientos_list) if sentimientos_list else 0
        
        conclusion = f"""
        Basándose en el análisis técnico realizado, se han identificado <b>{num_patrones} patrones</b> 
        en el comportamiento del activo. La dirección probable del mercado es <b>{direccion}</b> 
        con un nivel de confianza del <b>{confianza:.1f}%</b>.
        <br/><br/>
        El análisis de sentimiento de noticias muestra una tendencia <b>{'positiva' if sentimiento_noticias > 0.1 else 'negativa' if sentimiento_noticias < -0.1 else 'neutral'}</b>, 
        con un valor promedio de {sentimiento_noticias:.3f}.
        <br/><br/>
        <b>Recomendación:</b> 
        """
        
        if direccion == 'Alcista' and confianza > 60:
            conclusion += """Se observan señales alcistas con alta confianza. Considere posiciones 
            largas con gestión de riesgo apropiada."""
        elif direccion == 'Bajista' and confianza > 60:
            conclusion += """Se observan señales bajistas con alta confianza. Considere reducir 
            exposición o posiciones cortas con gestión de riesgo."""
        else:
            conclusion += """El mercado muestra señales mixtas. Se recomienda precaución y esperar 
            confirmación de tendencia antes de tomar posiciones significativas."""
        
        return conclusion
