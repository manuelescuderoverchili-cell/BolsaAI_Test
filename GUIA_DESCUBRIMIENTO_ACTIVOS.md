# 🔍 GUÍA DE DESCUBRIMIENTO DE ACTIVOS

## Descripción General

El módulo de **Descubrimiento de Activos** es una funcionalidad avanzada que busca automáticamente nuevos activos con alto potencial de crecimiento en el mercado. Utiliza un sistema de puntuación (0-100) basado en múltiples factores técnicos para identificar las mejores oportunidades.

## ¿Cómo Funciona?

### 1. Catálogo de Candidatos

El sistema analiza más de **65 activos candidatos** de diferentes categorías:

- **Criptomonedas emergentes**: Solana, Cardano, Polkadot, Avalanche, Chainlink, Polygon
- **Tecnología emergente**: Palantir, Snowflake, CrowdStrike, Cloudflare, Datadog, MongoDB, Unity, Roblox
- **IA y Semiconductores**: AMD, Intel, Qualcomm, Arm Holdings, Broadcom
- **Fintech**: Block (Square), PayPal, Coinbase, Robinhood
- **Energía renovable**: First Solar, Enphase Energy, SunPower, Plug Power
- **Biotecnología**: Moderna, BioNTech, Illumina, CRISPR Therapeutics
- **E-commerce**: Shopify, Etsy, MercadoLibre
- **Vehículos eléctricos**: Rivian, Lucid, NIO, Li Auto
- **Gaming y entretenimiento**: Sea Limited, DraftKings
- **Cloud y SaaS**: Zoom, DocuSign, Twilio, Okta

### 2. Sistema de Puntuación (0-100)

Cada activo es evaluado en base a 5 criterios principales:

#### A) Crecimiento Reciente (30 puntos)
- **30 puntos**: Crecimiento > 10% en 30 días
- **20 puntos**: Crecimiento > 5% en 30 días
- **10 puntos**: Crecimiento > 0% en 30 días

#### B) Crecimiento a Medio Plazo (25 puntos)
- **25 puntos**: Crecimiento > 20% en 90 días
- **15 puntos**: Crecimiento > 10% en 90 días
- **5 puntos**: Crecimiento > 0% en 90 días

#### C) Momentum y RSI (20 puntos)
- **20 puntos**: RSI entre 30-70 Y tendencia alcista
- **10 puntos**: Solo tendencia alcista

#### D) Volumen Creciente (15 puntos)
- **15 puntos**: Aumento de volumen > 20%
- **7 puntos**: Aumento de volumen > 0%

#### E) Volatilidad Controlada (10 puntos)
- **10 puntos**: Volatilidad < 3%
- **5 puntos**: Volatilidad < 5%

### 3. Criterio de Selección

Por defecto, solo los activos con **score ≥ 60/100** son considerados "prometedores" y recomendados para análisis adicional.

## Cómo Usar la Función

### Opción 1: Desde la Interfaz Gráfica

1. Abre la aplicación ejecutando `python main.py`
2. Haz clic en el botón **"🔍 Descubrir Nuevos Activos"**
3. Confirma que deseas iniciar el análisis (puede tardar varios minutos)
4. Espera a que se complete el análisis
5. Revisa los resultados en la pantalla
6. Si encuentras activos interesantes, se te preguntará si deseas añadirlos al sistema
7. Si aceptas, los activos se añadirán automáticamente para futuros análisis comparativos

### Opción 2: Desde Script

```python
from src.asset_discovery import AssetDiscovery
from src.market_analyzer import MarketAnalyzer

# Crear descubridor
discovery = AssetDiscovery()

# Buscar activos prometedores (score >= 60)
promising_assets = discovery.discover_promising_assets(min_score=60)

# Generar reporte
report = discovery.generate_discovery_report()
print(report)

# Guardar resultados
discovery.save_discovered_assets()

# Añadir al sistema
new_assets = discovery.get_assets_for_addition()
MarketAnalyzer.add_new_assets(new_assets)
MarketAnalyzer.save_assets_to_file()
```

## Resultados Generados

### 1. Reporte en Pantalla

Muestra los activos descubiertos con:
- Precio actual
- Score de potencial (0-100)
- Crecimiento en diferentes periodos (30d, 90d, 6m)
- Volatilidad
- RSI actual
- Tendencia (alcista/no alcista)
- Aumento de volumen

### 2. Archivo JSON (`src/discovered_assets.json`)

Contiene todos los datos de los activos descubiertos en formato JSON para análisis posterior.

### 3. Archivo de Configuración (`src/assets_config.json`)

Si decides añadir los activos al sistema, se actualiza este archivo con la lista completa de activos disponibles.

## Interpretación de Resultados

### Scores de Potencial

- **90-100**: 🌟 EXCEPCIONAL - Oportunidad extraordinaria
- **80-89**: 🚀 MUY ALTO - Excelente oportunidad
- **70-79**: ✅ ALTO - Buena oportunidad
- **60-69**: 💡 MODERADO - Oportunidad interesante
- **50-59**: ⚡ BAJO - Considerar con precaución
- **< 50**: ❌ MUY BAJO - No recomendado

### Factores a Considerar

**Crecimiento Sostenido**:
- Si el activo tiene crecimiento positivo en todos los periodos (30d, 90d, 6m), es señal de momentum sostenido

**Volatilidad**:
- Baja volatilidad (< 3%) = Menor riesgo
- Alta volatilidad (> 5%) = Mayor riesgo pero potencialmente mayor retorno

**RSI**:
- RSI < 30: Sobreventa (posible rebote)
- RSI 30-70: Zona neutral (saludable)
- RSI > 70: Sobrecompra (posible corrección)

**Tendencia**:
- Tendencia alcista confirmada = El precio está por encima de las medias móviles
- Sin tendencia alcista = Movimiento lateral o bajista

**Volumen**:
- Aumento de volumen = Mayor interés institucional
- Disminución de volumen = Posible falta de interés

## Mejores Prácticas

1. **Ejecuta la búsqueda semanalmente** para encontrar nuevas oportunidades

2. **No inviertas solo por el score**: El score es una guía, pero debes hacer tu propio análisis

3. **Verifica noticias recientes**: Antes de invertir, busca noticias sobre el activo

4. **Usa el análisis individual**: Una vez descubiertos, añádelos al sistema y ejecuta análisis individuales detallados

5. **Diversifica**: No pongas todo tu capital en un solo activo descubierto

6. **Establece stop loss**: Especialmente en activos con alta volatilidad

## Limitaciones

- El análisis se basa solo en datos técnicos (precio, volumen), no en fundamentales
- El rendimiento pasado no garantiza resultados futuros
- Algunos activos pueden tener datos limitados
- La volatilidad puede cambiar rápidamente

## Preguntas Frecuentes

**¿Cuánto tiempo tarda el análisis?**
- Depende de la conexión a internet, pero normalmente 5-10 minutos para todos los candidatos

**¿Puedo añadir mis propios activos candidatos?**
- Sí, edita `src/asset_discovery.py` y añade tickers al diccionario `CANDIDATE_TICKERS`

**¿Los activos descubiertos se añaden automáticamente?**
- No, se te pregunta si deseas añadirlos después del análisis

**¿Puedo ejecutar el descubrimiento con un score mínimo diferente?**
- Sí, en el código puedes cambiar el parámetro `min_score`

**¿Qué pasa con los activos que ya están en el sistema?**
- Se detectan como duplicados y no se vuelven a añadir

## Ejemplo de Resultado Real

```
🥇 #1 - AMD (AMD)
   • Precio actual: $254.51
   • Score de potencial: 80/100
   • Crecimiento 30 días: +58.20%
   • Crecimiento 90 días: +79.36%
   • Crecimiento 6 meses: +153.02%
   • Volatilidad: 3.63%
   • RSI: 59.9
   • Tendencia: 📈 Alcista
   • Aumento de volumen: -15.8%
```

**Interpretación**: AMD muestra un score de 80/100 con crecimiento excepcional en todos los periodos (+153% en 6 meses). RSI saludable en 59.9, tendencia alcista confirmada, volatilidad moderada. A pesar de la disminución de volumen reciente (-15.8%), es una excelente oportunidad según los criterios técnicos.

## Actualizaciones Futuras

Funcionalidades planeadas:
- Análisis de fundamentales (P/E, market cap, etc.)
- Integración con noticias y sentiment analysis
- Machine learning para predicción de scores
- Alertas automáticas cuando aparecen nuevos activos prometedores
- Análisis de correlación con índices principales
