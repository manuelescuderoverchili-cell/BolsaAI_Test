# 📊 LIMITACIONES DE INTERVALOS Y AJUSTE AUTOMÁTICO

## Problema Identificado

Al usar intervalos de muestreo de poco tiempo (como 1 minuto, 5 minutos, etc.) con periodos largos (1 año, 6 meses), **yfinance** tiene restricciones internas que limitan la cantidad de datos que puede retornar. Esto causaba que las gráficas no mostraran todo el periodo solicitado.

## Solución Implementada

Se ha añadido un **sistema de ajuste automático** que adapta el periodo según el intervalo seleccionado para obtener la máxima cantidad de datos posibles dentro de las restricciones de yfinance.

## Restricciones de yfinance

### Intervalos Intraday de Alta Frecuencia (1m, 2m, 5m)
- **Máximo**: 7 días de datos
- **Uso recomendado**: Análisis intraday, day trading, scalping
- **Ejemplo**: Si seleccionas "1 año" con intervalo "1 minuto", el sistema ajustará automáticamente a "7 días"

### Intervalos Intraday de Media Frecuencia (15m, 30m)
- **Máximo**: 60 días de datos
- **Uso recomendado**: Swing trading, análisis de patrones de corto-medio plazo
- **Ejemplo**: Si seleccionas "6 meses" con intervalo "15 minutos", el sistema ajustará automáticamente a "60 días"

### Intervalos Horarios (60m, 90m, 1h)
- **Máximo**: 730 días (2 años)
- **Uso recomendado**: Análisis de medio plazo, patrones semanales
- **Ejemplo**: Si seleccionas "5 años" con intervalo "1 hora", el sistema ajustará automáticamente a "730 días"

### Intervalos Diarios o Mayores (1d, 5d, 1wk, 1mo)
- **Sin restricción importante**
- **Uso recomendado**: Análisis de largo plazo, inversión, tendencias macro
- **Ejemplo**: Puedes solicitar "5 años" con intervalo "1 día" sin problemas

## Tabla de Compatibilidad

| Intervalo | Periodo Máximo | Puntos de Datos Típicos | Uso Ideal |
|-----------|---------------|------------------------|-----------|
| 1 minuto | 7 días | ~7,000 | Day trading |
| 5 minutos | 7 días | ~2,000 | Scalping/Intraday |
| 15 minutos | 60 días | ~5,700 | Swing trading |
| 30 minutos | 60 días | ~2,800 | Swing trading |
| 1 hora | 730 días (2 años) | ~17,500 | Trading medio plazo |
| 1 día | Ilimitado | Variable | Inversión largo plazo |
| 1 semana | Ilimitado | Variable | Análisis macro |

## Cómo Funciona el Ajuste Automático

### 1. Detección de Conflicto
El sistema detecta cuando la combinación periodo/intervalo excede los límites de yfinance:

```python
# Usuario selecciona: "1 año" + "1 minuto"
# Sistema detecta: intervalo 1m tiene límite de 7 días
```

### 2. Ajuste Inteligente
Ajusta automáticamente el periodo al máximo permitido:

```python
# Sistema ajusta: periodo "1 año" → "7 días"
# Muestra advertencia: "⚠️ Periodo ajustado de '1y' a '7d'"
```

### 3. Información al Usuario
Proporciona feedback claro sobre el ajuste:
- Mensaje en consola con el ajuste realizado
- Información de datos obtenidos (cantidad, rango temporal)
- Advertencia visual en la interfaz gráfica

## Advertencias en la Interfaz

La interfaz ahora muestra **advertencias dinámicas** según el intervalo seleccionado:

```
Intervalo: 1 minuto
⚠️ Intervalo de 1m: Máximo 7 días de datos disponibles

Intervalo: 5 minutos  
⚠️ Intervalo de 5m: Máximo 7 días de datos disponibles

Intervalo: 15 minutos
⚠️ Intervalo de 15m: Máximo 60 días de datos disponibles

Intervalo: 1 hora
⚠️ Intervalo de 1h: Máximo 730 días de datos disponibles

Intervalo: 1 día
(Sin advertencia - sin restricción)
```

## Ejemplos de Uso

### Caso 1: Trading Intraday
```
Objetivo: Analizar Bitcoin para day trading
Selección: 
  - Activo: Bitcoin
  - Periodo: 5 días
  - Intervalo: 1 minuto
Resultado: ✅ OK - Obtiene ~5,000 puntos de datos
```

### Caso 2: Swing Trading
```
Objetivo: Analizar Tesla para swing trading
Selección:
  - Activo: Tesla
  - Periodo: 1 mes
  - Intervalo: 15 minutos
Resultado: ✅ OK - Obtiene ~2,800 puntos de datos
```

### Caso 3: Análisis de Medio Plazo
```
Objetivo: Analizar Apple para posición de semanas
Selección:
  - Activo: Apple
  - Periodo: 1 año
  - Intervalo: 1 hora
Resultado: ✅ OK - Obtiene ~8,700 puntos de datos
```

### Caso 4: Inversión Largo Plazo
```
Objetivo: Analizar Ethereum para hold
Selección:
  - Activo: Ethereum
  - Periodo: 5 años
  - Intervalo: 1 día
Resultado: ✅ OK - Obtiene ~1,800 puntos de datos
```

### Caso 5: Ajuste Automático
```
Objetivo: Usuario novato selecciona combinación inválida
Selección:
  - Activo: Microsoft
  - Periodo: 1 año ⚠️
  - Intervalo: 1 minuto ⚠️
Sistema: 
  - Ajusta automáticamente a: 7 días
  - Muestra advertencia
  - Obtiene datos máximos posibles (~7,000 puntos)
Resultado: ✅ Funciona sin error, con datos útiles
```

## Resultados de la Prueba

Ejecutando `test_interval_limits.py`:

```
✅ 1 año + 1m → Ajustado a 7d (7,402 puntos)
✅ 3 meses + 5m → Ajustado a 7d (1,938 puntos)
✅ 6 meses + 15m → Ajustado a 60d (5,734 puntos)
✅ 1 año + 1h → Sin ajuste (8,760 puntos)
✅ 5 años + 1h → Ajustado a 730d (17,513 puntos)
✅ 1 mes + 1d → Sin ajuste (32 puntos)
✅ 5 días + 1m → Sin ajuste (5,086 puntos)
```

## Recomendaciones de Uso

### Para Day Trading (operaciones en el día)
- **Intervalo**: 1m o 5m
- **Periodo**: 1-5 días
- **Patrones**: Soportes/resistencias intraday

### Para Swing Trading (varios días/semanas)
- **Intervalo**: 15m o 1h
- **Periodo**: 1-3 meses
- **Patrones**: Doble techo/suelo, banderas

### Para Position Trading (semanas/meses)
- **Intervalo**: 1h o 1d
- **Periodo**: 6 meses - 1 año
- **Patrones**: Triángulos, canales, hombro-cabeza-hombro

### Para Inversión Largo Plazo (años)
- **Intervalo**: 1d o 1wk
- **Periodo**: 1-5 años
- **Patrones**: Tendencias macro, ciclos de mercado

## Código Implementado

### Método de Ajuste Automático

```python
def _adjust_period_for_interval(self, period: str, interval: str) -> str:
    """Ajusta el periodo según restricciones de yfinance"""
    
    if interval in ['1m', '2m', '5m']:
        # Máximo 7 días
        max_days_map = {
            '5y': '7d', '2y': '7d', '1y': '7d',
            '6mo': '7d', '3mo': '7d', '1mo': '7d',
            '5d': '5d', '1d': '1d'
        }
        return max_days_map.get(period, '7d')
    
    elif interval in ['15m', '30m']:
        # Máximo 60 días
        ...
    
    elif interval in ['60m', '90m', '1h']:
        # Máximo 730 días
        ...
    
    return period  # Sin restricción
```

### Advertencias en la GUI

```python
def update_data_warning(self):
    """Actualiza advertencia según intervalo"""
    warnings = {
        "1 minuto": "⚠️ Máximo 7 días de datos",
        "5 minutos": "⚠️ Máximo 7 días de datos",
        "15 minutos": "⚠️ Máximo 60 días de datos",
        "1 hora": "⚠️ Máximo 730 días de datos",
        "1 día": "",
        "1 semana": ""
    }
    self.warning_label.configure(text=warnings.get(interval, ""))
```

## Beneficios

1. **No más errores**: El usuario nunca verá un error por combinación inválida
2. **Máximos datos**: Siempre obtiene la mayor cantidad de datos posibles
3. **Transparencia**: Sabe exactamente qué ajustes se hicieron
4. **Usabilidad**: No necesita conocer las restricciones técnicas
5. **Flexibilidad**: Puede experimentar sin miedo a romper nada

## Limitaciones Conocidas

- Los ajustes son conservadores para garantizar funcionamiento
- En algunos casos, yfinance puede retornar menos datos de los esperados (fines de semana, festivos)
- Los intervalos muy pequeños (1m) pueden tener gaps en horas no de mercado
- Las criptomonedas tienen datos 24/7, las acciones solo horario de mercado

---

**Última actualización**: 04/11/2025  
**Versión**: 3.0
