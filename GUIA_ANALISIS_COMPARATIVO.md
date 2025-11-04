# 📘 Guía de Uso - Análisis Comparativo

## 🎯 Objetivo

El análisis comparativo te permite identificar las mejores oportunidades de inversión entre TODOS los activos disponibles en un solo clic.

## 🚀 Pasos para Ejecutar

### 1. Configuración Inicial

```
Periodo recomendado: 1 mes (para datos suficientes)
Intervalo recomendado: 1 día (para análisis técnico)
```

### 2. Ejecutar Análisis

Haz clic en el botón azul: **"📊 Comparar TODOS los Activos"**

El sistema analizará:
- ✅ 15 activos financieros
- ✅ Datos históricos del periodo seleccionado
- ✅ Patrones técnicos de cada activo
- ✅ Predicciones basadas en IA
- ✅ Score de rentabilidad multi-factorial

**Tiempo estimado**: 3-5 minutos

### 3. Interpretar Resultados

#### 🏆 Top 5 - Mejores Oportunidades

```
🥇 #1 - Apple (AAPL)
   • Precio actual: $225.50
   • Precio objetivo: $245.00
   • Retorno esperado: +8.65%
   • Dirección: Alcista (Confianza: 85.0%)
   • Categoría: 🟢 MUY ALCISTA
   • Score de rentabilidad: 87.0/100
   • Recomendación: 🚀 COMPRA FUERTE
```

**Qué significa:**
- ✅ Apple tiene el mayor potencial de rentabilidad
- ✅ 87/100 score indica alta probabilidad de éxito
- ✅ Confianza del 85% en dirección alcista
- ✅ Retorno esperado del +8.65%

#### ⚠️ Bottom 5 - Activos con Mayor Riesgo

```
#15 - Netflix (NFLX)
   • Categoría: 🔴 MUY BAJISTA
   • Score: 13.0/100
   • Recomendación: 🛑 VENTA FUERTE
```

**Qué significa:**
- ⚠️ Netflix muestra señales bajistas
- ⚠️ Score bajo indica alto riesgo
- ⚠️ Considerar venta o no entrar

## 📊 Entendiendo el Score de Rentabilidad

### Score 75-100: 🟢 MUY ALCISTA
- **Acción**: Compra fuerte
- **Características**: Múltiples patrones alcistas, tendencia clara, RSI favorable
- **Ejemplo**: "Este activo tiene 5 patrones alcistas, RSI en 35 (sobreventa), y tendencia alcista confirmada"

### Score 60-74: 🟢 ALCISTA
- **Acción**: Compra
- **Características**: Balance positivo de señales
- **Ejemplo**: "Más patrones alcistas que bajistas, tendencia positiva"

### Score 45-59: 🟡 NEUTRAL-ALCISTA
- **Acción**: Compra moderada
- **Características**: Ligero sesgo alcista
- **Ejemplo**: "Señales mixtas con leve ventaja alcista"

### Score 35-44: 🟡 NEUTRAL
- **Acción**: Mantener/Observar
- **Características**: Equilibrio entre señales
- **Ejemplo**: "No hay dirección clara, esperar confirmación"

### Score 25-34: 🟠 NEUTRAL-BAJISTA
- **Acción**: Precaución
- **Características**: Ligero sesgo bajista
- **Ejemplo**: "Algunas señales de debilidad"

### Score 15-24: 🔴 BAJISTA
- **Acción**: Considerar venta
- **Características**: Balance negativo
- **Ejemplo**: "Más patrones bajistas que alcistas"

### Score 0-14: 🔴 MUY BAJISTA
- **Acción**: Venta fuerte
- **Características**: Múltiples señales bajistas
- **Ejemplo**: "Tendencia bajista confirmada, RSI sobrecompra"

## 📈 Factores que Afectan el Score

### 1. Predicción y Confianza (±30 puntos)
- Alcista con 80% confianza → +24 puntos
- Bajista con 80% confianza → -24 puntos

### 2. Balance de Patrones (±15 puntos)
- 80% patrones alcistas → +12 puntos
- 80% patrones bajistas → -12 puntos

### 3. RSI (±10 puntos)
- RSI < 30 (sobreventa) → +10 puntos (oportunidad)
- RSI > 70 (sobrecompra) → -10 puntos (riesgo)
- RSI 40-60 (neutral) → +5 puntos (estable)

### 4. Tendencia (±10 puntos)
- Alcista → +10 puntos
- Bajista → -10 puntos
- Lateral → 0 puntos

### 5. Volatilidad (±5 puntos)
- Volatilidad < 2% → +5 puntos (estable)
- Volatilidad > 5% → -5 puntos (arriesgado)

## 💡 Casos de Uso Prácticos

### Caso 1: Construir Portafolio Diversificado
```
1. Ejecutar análisis comparativo
2. Seleccionar top 3 de MUY ALCISTA
3. Seleccionar top 2 de ALCISTA
4. Distribuir capital: 40% en MUY ALCISTA, 30% en ALCISTA, 30% cash
```

### Caso 2: Rebalanceo de Cartera
```
1. Ejecutar análisis comparativo semanal
2. Vender activos que cayeron a BAJISTA
3. Mantener activos NEUTRAL o superiores
4. Comprar nuevos activos MUY ALCISTA
```

### Caso 3: Trading a Corto Plazo
```
1. Usar periodo "1 semana" e intervalo "1 hora"
2. Buscar activos con score > 70
3. Entrar con stop loss del 2%
4. Salir cuando score baje a < 50
```

### Caso 4: Inversión Conservadora
```
1. Filtrar solo activos con score > 60
2. Eliminar activos con volatilidad > 3%
3. Preferir índices y blue chips
4. Mantener largo plazo
```

## 📁 Archivo CSV Exportado

El archivo `Comparativa_Activos_YYYYMMDD_HHMMSS.csv` contiene:

| Columna | Descripción |
|---------|-------------|
| activo | Nombre del activo |
| ticker | Símbolo bursátil |
| categoria | Clasificación (MUY ALCISTA, etc.) |
| recomendacion | Acción sugerida |
| score_rentabilidad | Puntuación 0-100 |
| precio_actual | Precio actual USD |
| precio_objetivo | Precio objetivo estimado |
| retorno_esperado | Retorno esperado % |
| direccion | Alcista/Bajista/Neutral |
| confianza | Nivel de confianza % |
| tendencia | Tendencia técnica |
| rsi | Índice de Fuerza Relativa |
| volatilidad | Volatilidad % |
| patrones_alcistas | Número de patrones alcistas |
| patrones_bajistas | Número de patrones bajistas |
| total_patrones | Total de patrones detectados |

## 🎓 Tips Avanzados

### 1. Combinar con Noticias
- Si un activo tiene score alto Y sentimiento de noticias positivo → Máxima confianza
- Si discrepan → Investigar más antes de actuar

### 2. Correlaciones
- Compara activos relacionados (ej: MSFT vs GOOGL)
- Si todos los tech están bajistas → Señal sectorial

### 3. Timeframes Múltiples
- Ejecuta con 1 semana (tendencia corto plazo)
- Ejecuta con 1 mes (tendencia medio plazo)
- Solo entra si ambos coinciden en dirección

### 4. Confirmación de Patrones
- Score alto + múltiples patrones alcistas = Alta probabilidad
- Score bajo con 1 solo patrón = Baja confianza

### 5. Stop Loss Dinámico
- Score > 75 → Stop loss 3%
- Score 60-74 → Stop loss 2%
- Score < 60 → Stop loss 1%

## ⚠️ Advertencias Importantes

1. **No es predicción del futuro**: Los mercados son impredecibles
2. **Usar gestión de riesgo**: Nunca invertir más del 2% por operación
3. **Diversificar**: No poner todos los huevos en una canasta
4. **Revisar regularmente**: El mercado cambia constantemente
5. **Confirmar con fundamentales**: El análisis técnico es solo una herramienta

## 📞 Preguntas Frecuentes

**P: ¿Con qué frecuencia debo ejecutar el análisis?**
R: Semanalmente para estrategias de medio plazo, diariamente para trading activo.

**P: ¿Qué hago si todos los activos están en BAJISTA?**
R: Mantener cash, esperar mejores condiciones, o buscar activos defensivos.

**P: ¿Puedo confiar 100% en el score?**
R: No. Úsalo como guía junto con tu propio análisis y gestión de riesgo.

**P: ¿Por qué algunos activos fallan en el análisis?**
R: Datos insuficientes o problemas de conexión. Reintenta más tarde.

**P: ¿Qué periodo e intervalo son mejores?**
R: 1 mes / 1 día para swing trading, 1 semana / 1 hora para day trading.

---

**¡Feliz Trading! 📈🚀**
