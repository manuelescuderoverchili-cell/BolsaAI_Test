# 📰 HIPERVÍNCULOS A NOTICIAS EN REPORTES PDF

## Descripción

Los reportes PDF de análisis individual ahora incluyen **hipervínculos clickeables** a las noticias más relevantes, permitiendo acceso directo a las fuentes originales para profundizar en el contexto del activo analizado.

## Características

### 🔥 Sección de Noticias de Alto Impacto

Las noticias se clasifican por **score de impacto** calculado mediante:

```
Impacto = |Sentimiento| + (Subjetividad × 0.3)
```

- **|Sentimiento|**: Valor absoluto de la polaridad (-1 a +1)
- **Subjetividad**: Nivel de opinión vs hechos objetivos (0 a 1)

Las **Top 5 noticias de mayor impacto** se muestran destacadas con:

#### Clasificación por Sentimiento

| Emoji | Label | Polaridad | Color | Significado |
|-------|-------|-----------|-------|-------------|
| 🚀 | MUY POSITIVO | > 0.2 | Verde oscuro | Noticias muy favorables |
| 😊 | POSITIVO | 0.05 a 0.2 | Verde claro | Noticias favorables |
| 😐 | NEUTRAL | -0.05 a 0.05 | Gris | Noticias neutrales |
| 😟 | NEGATIVO | -0.2 a -0.05 | Naranja | Noticias desfavorables |
| ⚠️ | MUY NEGATIVO | < -0.2 | Rojo | Noticias muy desfavorables |

#### Información Mostrada

Para cada noticia de alto impacto:
- **Título de la noticia**
- **Score de impacto** (calculado)
- **Clasificación de sentimiento** (con emoji y color)
- **Fuente** y **fecha de publicación**
- **🔗 Hipervínculo clickeable** para leer la noticia completa

### 📰 Otras Noticias Recientes

Después de las noticias de alto impacto, se muestran hasta **10 noticias adicionales** ordenadas por fecha, también con hipervínculos.

## Ejemplo de Visualización en PDF

```
🔥 NOTICIAS DE ALTO IMPACTO:

🚀 #1 - Bitcoin alcanza nuevo máximo histórico tras aprobación de ETF
Impacto: 0.856 | Sentimiento: MUY POSITIVO (0.723)
📰 CoinDesk | 📅 04/11/2025 14:30
🔗 Leer noticia completa [CLICKEABLE]

⚠️ #2 - Reguladores advierten sobre riesgos en criptomonedas
Impacto: 0.745 | Sentimiento: MUY NEGATIVO (-0.612)
📰 CoinTelegraph | 📅 04/11/2025 12:15
🔗 Leer noticia completa [CLICKEABLE]

😊 #3 - Grandes instituciones aumentan posiciones en Bitcoin
Impacto: 0.523 | Sentimiento: POSITIVO (0.145)
📰 CoinDesk | 📅 04/11/2025 10:45
🔗 Leer noticia completa [CLICKEABLE]
```

## Cómo Funciona

### 1. Recopilación de Noticias

El sistema busca noticias de múltiples fuentes RSS:
- CoinDesk
- CoinTelegraph
- (Otras fuentes según el activo)

### 2. Análisis de Sentimiento

Cada noticia se analiza con:
- **Polaridad**: -1 (muy negativo) a +1 (muy positivo)
- **Subjetividad**: 0 (objetivo) a 1 (muy subjetivo)

### 3. Cálculo de Impacto

```python
impacto = abs(polaridad) + (subjetividad * 0.3)
```

Las noticias con sentimientos extremos (muy positivos o muy negativos) y alta subjetividad tienen mayor impacto.

### 4. Ordenamiento

- **Alto impacto**: Top 5 ordenadas por score de impacto
- **Otras noticias**: Hasta 10 más, ordenadas por fecha

### 5. Generación de Hipervínculos

Los enlaces se generan como hipervínculos HTML en el PDF:
```html
<a href="https://..." color="blue">🔗 Leer noticia completa</a>
```

## Uso

### Desde la Interfaz Gráfica

1. Selecciona un activo
2. Haz clic en "🚀 Iniciar Análisis Completo"
3. Espera a que se complete el análisis
4. Se generará automáticamente un PDF
5. Abre el PDF y navega a la sección "ANÁLISIS DE SENTIMIENTO DE NOTICIAS"
6. Haz clic en los enlaces 🔗 para abrir las noticias en tu navegador

### Desde Código

```python
from src.market_analyzer import MarketAnalyzer
from src.news_analyzer import NewsAnalyzer
from src.pdf_report_generator import PDFReportGenerator

# Analizar activo
market_analyzer = MarketAnalyzer("Bitcoin")
data = market_analyzer.get_data(period="1mo", interval="1d")
stats = market_analyzer.calculate_statistics()

# Obtener noticias
news_analyzer = NewsAnalyzer("Bitcoin")
news_analyzer.fetch_news(max_news=20)

# Preparar datos
analysis_results = {
    'asset_name': "Bitcoin",
    'noticias': news_analyzer.noticias,
    'stats': stats,
    # ... otros datos
}

# Generar PDF
pdf_generator = PDFReportGenerator()
pdf_path = pdf_generator.generate_complete_pdf_report(
    "Bitcoin", 
    analysis_results, 
    graph_paths
)
```

## Beneficios

### 🎯 Contexto Inmediato
Acceso directo a las fuentes para entender el contexto completo

### 📊 Priorización Inteligente
Las noticias más importantes aparecen primero basadas en impacto

### ⚡ Ahorro de Tiempo
No necesitas buscar manualmente las noticias relevantes

### 🔍 Análisis Profundo
Combina análisis técnico con contexto fundamental desde las noticias

### 📈 Mejor Toma de Decisiones
Información completa (técnica + fundamental) en un solo documento

## Limitaciones

- Los hipervínculos solo funcionan si el PDF se abre en un lector compatible (Adobe Reader, navegadores modernos)
- Algunos lectores de PDF básicos pueden no soportar enlaces clickeables
- Las noticias dependen de la disponibilidad de fuentes RSS
- El análisis de sentimiento es automático y puede no captar toda la complejidad

## Solución de Problemas

### Los enlaces no son clickeables

**Problema**: Los enlaces aparecen como texto normal
**Solución**: Abre el PDF con Adobe Acrobat Reader, Chrome, Edge o Firefox

### No aparecen noticias en el PDF

**Problema**: La sección de noticias está vacía
**Solución**: 
1. Verifica tu conexión a internet
2. Comprueba que las fuentes RSS estén disponibles
3. Intenta con otro activo más popular (Bitcoin, Ethereum)

### Errores de "Sin enlace disponible"

**Problema**: Algunas noticias no tienen hipervínculo
**Solución**: Normal, no todas las fuentes RSS proporcionan enlaces. El sistema lo maneja mostrando el aviso.

## Ejemplos Reales

### Caso 1: Análisis de Bitcoin

```
🔥 NOTICIAS DE ALTO IMPACTO:

🚀 #1 - Bitcoin ETF Approval Sends Price to New Heights
Impacto: 0.892 | Sentimiento: MUY POSITIVO (0.756)
📰 CoinDesk | 📅 04/11/2025 15:22
🔗 Leer noticia completa

😟 #2 - SEC Investigates Major Exchange for Regulatory Violations  
Impacto: 0.734 | Sentimiento: NEGATIVO (-0.618)
📰 CoinTelegraph | 📅 04/11/2025 13:45
🔗 Leer noticia completa

😊 #3 - Institutional Adoption Grows with Major Bank Partnership
Impacto: 0.654 | Sentimiento: POSITIVO (0.487)
📰 CoinDesk | 📅 04/11/2025 11:30
🔗 Leer noticia completa
```

### Caso 2: Análisis de Apple

```
🔥 NOTICIAS DE ALTO IMPACTO:

🚀 #1 - Apple Reports Record-Breaking Quarter
Impacto: 0.823 | Sentimiento: MUY POSITIVO (0.689)
📰 Reuters | 📅 04/11/2025 16:00
🔗 Leer noticia completa

😊 #2 - New iPhone Launch Exceeds Expectations
Impacto: 0.612 | Sentimiento: POSITIVO (0.423)
📰 Bloomberg | 📅 04/11/2025 14:30
🔗 Leer noticia completa
```

## Mejoras Futuras

- Integración con más fuentes de noticias
- Análisis de sentimiento más sofisticado con IA
- Resúmenes automáticos de noticias largas
- Clasificación por categorías (regulación, adopción, tecnología, etc.)
- Vista previa de noticias en el propio PDF
- Alertas de noticias de alto impacto en tiempo real

## Soporte

Para reportar problemas o sugerir mejoras, contacta con el equipo de desarrollo.

---

**Fecha de actualización**: 04/11/2025
**Versión**: 2.0
