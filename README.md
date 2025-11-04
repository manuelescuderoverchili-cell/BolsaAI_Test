# 📊 Market Analyzer - Análisis de Mercados Financieros

Una aplicación moderna con interfaz gráfica para analizar activos financieros en tiempo real, incluyendo análisis técnico, detección de tendencias y análisis de sentimiento de noticias.

## 🎯 Características

- ✅ **Interfaz gráfica moderna** con CustomTkinter (tema oscuro)
- ✅ **Múltiples activos** soportados: Bitcoin, Ethereum, Tesla, Apple, Microsoft, Amazon, Google, NVIDIA, Meta, Netflix, índices bursátiles, oro y plata
- ✅ **Análisis técnico completo**: medias móviles (SMA 20/50), RSI, soportes/resistencias
- ✅ **Detección de tendencias** y patrones de mercado
- ✅ **Análisis de sentimiento** de noticias en tiempo real
- ✅ **Gráficos profesionales**: evolución de precios, volumen, retornos, velas japonesas
- ✅ **Periodos flexibles**: desde 1 día hasta 5 años
- ✅ **Múltiples intervalos**: desde 1 minuto hasta 1 semana
- ✅ **Exportación automática** de gráficos en alta calidad

## 📁 Estructura del Proyecto

```
# 📊 BolsaAI - Análisis Inteligente de Mercados Financieros

Sistema avanzado de análisis técnico, predictivo y comparativo de activos financieros con interfaz gráfica.

## 🚀 Características Principales

### 1. Análisis Individual de Activos
- **Análisis técnico completo**: SMA, RSI, soportes, resistencias
- **Detección de patrones**: 15+ patrones de velas y gráficos
- **Análisis de noticias**: Sentimiento de 50+ noticias por activo
- **Predicciones**: Escenarios optimista/base/pesimista con rangos de precio
- **Reportes PDF**: Gráficos profesionales con patrones marcados

### 2. 🆕 Análisis Comparativo de TODOS los Activos
- **Análisis masivo**: Compara los 15 activos disponibles simultáneamente
- **Ranking inteligente**: Ordena por potencial de rentabilidad
- **Score de rentabilidad**: Puntuación 0-100 basada en múltiples factores
- **Categorización**: Desde "MUY ALCISTA" hasta "MUY BAJISTA"
- **Recomendaciones**: Compra Fuerte, Compra, Mantener, Venta, etc.
- **Exportación CSV**: Resultados tabulados para análisis posterior

## 📈 Activos Disponibles

### Criptomonedas
- Bitcoin (BTC-USD)
- Ethereum (ETH-USD)

### Acciones Tecnológicas
- Tesla (TSLA)
- Apple (AAPL)
- Microsoft (MSFT)
- Amazon (AMZN)
- Google/Alphabet (GOOGL)
- NVIDIA (NVDA)
- Meta/Facebook (META)
- Netflix (NFLX)

### Índices
- S&P 500 (^GSPC)
- Dow Jones (^DJI)
- NASDAQ (^IXIC)

### Metales Preciosos
- Oro (GC=F)
- Plata (SI=F)

## 🎯 Cómo Usar el Análisis Comparativo

1. **Abrir la aplicación**: Ejecuta `python main.py`
2. **Configurar periodo**: Selecciona el periodo (1 mes recomendado)
3. **Hacer clic en "📊 Comparar TODOS los Activos"**
4. **Esperar el análisis**: Tardará 3-5 minutos
5. **Revisar resultados**:
   - Top 5 mejores oportunidades
   - Bottom 5 activos con mayor riesgo
   - Estadísticas generales
   - CSV exportado en `outputs/reports/`

## 📊 Sistema de Puntuación

El **Score de Rentabilidad (0-100)** se calcula con:

- **Dirección y Confianza** (±30 pts): Predicción alcista/bajista
- **Balance de Patrones** (±15 pts): Ratio patrones alcistas vs bajistas
- **RSI** (±10 pts): Sobreventa (+), Sobrecompra (-)
- **Tendencia** (±10 pts): Alcista (+), Bajista (-)
- **Volatilidad** (±5 pts): Baja volatilidad (+)

## 🏆 Categorías de Activos

| Score | Categoría | Emoji | Acción Sugerida |
|-------|-----------|-------|-----------------|
| 75-100 | MUY ALCISTA | 🟢 | Compra Fuerte |
| 60-74 | ALCISTA | 🟢 | Compra |
| 45-59 | NEUTRAL-ALCISTA | 🟡 | Compra Moderada |
| 35-44 | NEUTRAL | 🟡 | Mantener/Observar |
| 25-34 | NEUTRAL-BAJISTA | 🟠 | Precaución |
| 15-24 | BAJISTA | 🔴 | Considerar Venta |
| 0-14 | MUY BAJISTA | 🔴 | Venta Fuerte |

## 🔧 Instalación y Ejecución

```bash
# Activar entorno virtual
.\venv\Scripts\Activate.ps1

# Ejecutar aplicación
python main.py
```

## ⚠️ Disclaimer

Este software es solo para fines educativos y de análisis. No constituye asesoramiento financiero. Consulte siempre con un profesional antes de tomar decisiones de inversión.

│
├── main.py                      # Aplicación principal con interfaz gráfica
├── requirements.txt             # Dependencias del proyecto
├── README.md                    # Este archivo
├── .gitignore                   # Archivos ignorados por git
│
├── src/                         # Módulos del proyecto
│   ├── __init__.py
│   ├── market_analyzer.py       # Análisis de mercados
│   ├── news_analyzer.py         # Análisis de noticias
│   └── visualizer.py            # Generación de gráficos
│
├── outputs/                     # Archivos generados
│   ├── graphs/                  # Gráficos PNG
│   └── reports/                 # Reportes de texto
│
├── data/                        # Datos temporales
│
└── venv/                        # Entorno virtual Python
```

## 🚀 Instalación

### 1. Clonar el repositorio (si aplica)
```bash
git clone <tu-repositorio>
cd BolsaAI_Test
```

### 2. Crear entorno virtual (ya creado)
El entorno virtual ya está configurado en la carpeta `venv/`

### 3. Instalar dependencias
```powershell
.\venv\Scripts\python.exe -m pip install -r requirements.txt
```

## 💻 Uso

### Ejecutar la aplicación
```powershell
.\venv\Scripts\python.exe main.py
```

### Pasos para analizar un activo:

1. **Seleccionar el activo** del menú desplegable (Bitcoin, Tesla, etc.)
2. **Elegir el periodo** de tiempo (1 día, 1 mes, 1 año, etc.)
3. **Seleccionar el intervalo** de datos (1 minuto, 1 hora, 1 día, etc.)
4. **Marcar las opciones** deseadas:
   - ✅ Incluir análisis de noticias
   - ✅ Guardar gráficos
5. **Hacer clic** en "🚀 Iniciar Análisis"
6. **Esperar** a que se complete el análisis
7. **Revisar** los resultados en el panel derecho
8. **Encontrar** los gráficos en la carpeta `outputs/graphs/`

## 📊 Tipos de Análisis

### 1. Análisis Técnico
- Precio actual, máximo, mínimo
- Variación absoluta y porcentual
- Volatilidad del mercado
- Medias móviles simples (SMA 20 y 50)
- RSI (Relative Strength Index)
- Soportes y resistencias
- Detección de tendencias (alcista/bajista)

### 2. Análisis de Noticias
- Búsqueda automática de noticias relevantes
- Análisis de sentimiento (positivo/negativo/neutral)
- Distribución de sentimientos
- Evolución temporal del sentimiento
- Fuentes múltiples de noticias especializadas

### 3. Visualizaciones
- Gráfico de evolución de precios con medias móviles
- Gráfico de volumen de transacciones
- Gráfico de retornos diarios
- Gráfico de velas japonesas (candlestick)
- Gráfico de análisis de sentimiento de noticias
- Distribución de polaridad de noticias

## 🎨 Activos Disponibles

### Criptomonedas
- Bitcoin (BTC-USD)
- Ethereum (ETH-USD)

### Tecnología
- Tesla (TSLA)
- Apple (AAPL)
- Microsoft (MSFT)
- Amazon (AMZN)
- Google (GOOGL)
- NVIDIA (NVDA)
- Meta (META)
- Netflix (NFLX)

### Índices
- S&P 500 (^GSPC)
- Dow Jones (^DJI)
- NASDAQ (^IXIC)

### Materias Primas
- Oro (GC=F)
- Plata (SI=F)

## 📦 Dependencias Principales

- **yfinance**: Obtención de datos financieros
- **customtkinter**: Interfaz gráfica moderna
- **matplotlib**: Generación de gráficos
- **pandas**: Manipulación de datos
- **numpy**: Cálculos numéricos
- **textblob**: Análisis de sentimiento
- **seaborn**: Visualizaciones estadísticas
- **feedparser**: Lectura de feeds RSS
- **beautifulsoup4**: Web scraping

## 🔧 Configuración Avanzada

### Añadir nuevos activos
Edita el diccionario `ASSETS` en `src/market_analyzer.py`:

```python
ASSETS = {
    'Tu Activo': 'TICKER-SYMBOL',
    # ... otros activos
}
```

### Añadir fuentes de noticias
Edita el método `_get_news_sources()` en `src/news_analyzer.py`

## 📝 Ejemplos de Salida

### Análisis de Bitcoin
```
╔══════════════════════════════════════════════════════════════╗
║         ANÁLISIS COMPLETO: BITCOIN
╚══════════════════════════════════════════════════════════════╝

📊 ESTADÍSTICAS BÁSICAS:
   • Precio Actual: $67,234.50
   • Variación: +2.45% ($1,608.23)
   • Volatilidad: 3.21%
   • RSI: 62.34 (NEUTRAL)

📈 ANÁLISIS TÉCNICO:
   • Tendencia Actual: ALCISTA
   • Señal: COMPRA (ALCISTA)
   
📰 ANÁLISIS DE NOTICIAS:
   • Total: 18 noticias
   • Sentimiento promedio: +0.234 (POSITIVO)
```

## 🐛 Solución de Problemas

### La aplicación no inicia
```powershell
# Verificar que el entorno virtual está activado
.\venv\Scripts\python.exe --version

# Reinstalar dependencias
.\venv\Scripts\python.exe -m pip install -r requirements.txt
```

### No se muestran gráficos
- Verifica que la carpeta `outputs/graphs/` existe
- Verifica que tienes permisos de escritura

### Error al obtener noticias
- Verifica tu conexión a internet
- Algunas fuentes RSS pueden estar temporalmente no disponibles

## 👨‍💻 Desarrollo

### Ejecutar en modo desarrollo
```powershell
.\venv\Scripts\python.exe main.py
```

### Ejecutar tests (si existen)
```powershell
.\venv\Scripts\python.exe -m pytest
```

## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:
1. Haz fork del proyecto
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

## 📧 Contacto

Para preguntas o sugerencias, abre un issue en el repositorio.

---

**Desarrollado con ❤️ usando Python y CustomTkinter**
