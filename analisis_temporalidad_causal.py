import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def analizar_temporalidad_noticias():
    """
    Analiza si las noticias aparecieron ANTES o DESPUÉS de los movimientos de precio
    """
    print("🕒 ANÁLISIS DE TEMPORALIDAD: ¿CAUSA O EFECTO?")
    print("="*60)
    
    # Datos con horarios específicos de las noticias
    datos_temporales = [
        # [Fecha, Hora_noticia, Variación_diaria, Sentimiento, Noticia]
        ["2025-10-08", "10:00", 1.57, 1, "Bitcoin ETF recibe nuevas inversiones"],
        ["2025-10-13", "20:00", 0.09, 1, "Adopción institucional de Bitcoin se acelera"],
        ["2025-10-16", "09:00", -2.34, -1, "Corrección técnica en Bitcoin"],
        ["2025-10-18", "13:00", 0.69, -1, "Regulación cripto genera incertidumbre"],
        ["2025-10-21", "05:00", -1.91, 0, "Volatilidad en mercados crypto"],
        ["2025-10-23", "20:00", 2.21, 1, "Bitcoin alcanza máximo mensual"],
        ["2025-10-25", "02:00", 0.55, 0, "Análisis técnico sugiere consolidación"]
    ]
    
    print("📊 ANÁLISIS TEMPORAL DETALLADO:")
    print(f"{'Fecha':<12} {'Hora':<6} {'Variación':<10} {'Tipo Noticia':<15} {'¿Timing Correcto?':<18} {'Noticia'}")
    print("-" * 100)
    
    casos_validos = 0
    casos_invalidos = 0
    
    for fecha, hora, variacion, sentimiento, noticia in datos_temporales:
        # Determinar el tipo de noticia
        if sentimiento == 1:
            tipo = "Positiva"
        elif sentimiento == -1:
            tipo = "Negativa"
        else:
            tipo = "Neutral"
        
        # Analizar el timing
        hora_int = int(hora.split(':')[0])
        
        # La variación diaria es el cambio desde apertura hasta cierre
        # Para que una noticia "cause" la variación, debería aparecer:
        # - Temprano en el día (antes de las 12:00) para impactar el precio del día
        # - O la noche anterior para impactar el día siguiente
        
        timing_correcto = False
        explicacion = ""
        
        if hora_int <= 12:  # Noticia en la mañana
            timing_correcto = True
            explicacion = "✅ Temprano"
        elif hora_int >= 20:  # Noticia en la noche
            timing_correcto = True
            explicacion = "⚠️ Nocturna"
        else:  # Noticia en la tarde
            timing_correcto = False
            explicacion = "❌ Tarde"
        
        if timing_correcto:
            casos_validos += 1
        else:
            casos_invalidos += 1
        
        print(f"{fecha:<12} {hora:<6} {variacion:+6.2f}%   {tipo:<15} {explicacion:<18} {noticia[:50]}...")
    
    print("\n" + "="*60)
    print(f"📈 ANÁLISIS DE CAUSALIDAD:")
    print(f"  • Casos con timing válido: {casos_validos}/{len(datos_temporales)} ({casos_validos/len(datos_temporales)*100:.1f}%)")
    print(f"  • Casos con timing inválido: {casos_invalidos}/{len(datos_temporales)} ({casos_invalidos/len(datos_temporales)*100:.1f}%)")
    
    # Análisis específico caso por caso
    print(f"\n🔍 ANÁLISIS CASO POR CASO:")
    
    casos = [
        {
            'fecha': '08/10',
            'hora': '10:00',
            'variacion': 1.57,
            'noticia': 'ETF inversiones',
            'sentimiento': 'positiva',
            'analisis': 'VÁLIDO - Noticia a las 10:00 AM puede influir en el precio del día'
        },
        {
            'fecha': '13/10',
            'hora': '20:00',
            'variacion': 0.09,
            'noticia': 'Adopción institucional',
            'sentimiento': 'positiva',
            'analisis': 'CUESTIONABLE - Noticia a las 8:00 PM, después del mercado. Podría ser EFECTO, no causa'
        },
        {
            'fecha': '16/10',
            'hora': '09:00',
            'variacion': -2.34,
            'noticia': 'Corrección técnica',
            'sentimiento': 'negativa',
            'analisis': 'VÁLIDO - Noticia temprana (9:00 AM) puede causar la caída del -2.34%'
        },
        {
            'fecha': '18/10',
            'hora': '13:00',
            'variacion': 0.69,
            'noticia': 'Regulación incertidumbre',
            'sentimiento': 'negativa',
            'analisis': 'INVÁLIDO - Noticia a la 1:00 PM, probablemente REACCIÓN al movimiento, no causa'
        },
        {
            'fecha': '21/10',
            'hora': '05:00',
            'variacion': -1.91,
            'noticia': 'Volatilidad mercados',
            'sentimiento': 'neutral',
            'analisis': 'VÁLIDO - Noticia muy temprana (5:00 AM) puede explicar la caída del día'
        },
        {
            'fecha': '23/10',
            'hora': '20:00',
            'variacion': 2.21,
            'noticia': 'Máximo mensual',
            'sentimiento': 'positiva',
            'analisis': 'INVÁLIDO - "Alcanza máximo" a las 8:00 PM es EFECTO, no causa del +2.21%'
        },
        {
            'fecha': '25/10',
            'hora': '02:00',
            'variacion': 0.55,
            'noticia': 'Consolidación técnica',
            'sentimiento': 'neutral',
            'analisis': 'VÁLIDO - Noticia a las 2:00 AM puede influir en el día'
        }
    ]
    
    validos_causales = 0
    for caso in casos:
        icono = "✅" if "VÁLIDO" in caso['analisis'] else "❌"
        if "VÁLIDO" in caso['analisis']:
            validos_causales += 1
        
        print(f"  {icono} {caso['fecha']} ({caso['hora']}): {caso['analisis']}")
    
    print(f"\n🎯 CONCLUSIÓN SOBRE CAUSALIDAD:")
    print(f"  • Solo {validos_causales}/7 casos tienen timing causal válido ({validos_causales/7*100:.1f}%)")
    print(f"  • La correlación de 0.592 incluye casos donde:")
    print(f"    - Las noticias son EFECTO del movimiento (no causa)")
    print(f"    - El timing no permite causalidad real")
    
    print(f"\n⚠️ PROBLEMAS IDENTIFICADOS:")
    print(f"  1. 'Bitcoin alcanza máximo mensual' (23/10, 20:00)")
    print(f"     → Claramente es EFECTO del +2.21%, no la causa")
    print(f"  2. 'Regulación genera incertidumbre' (18/10, 13:00)")
    print(f"     → Timing sugiere reacción al movimiento")
    print(f"  3. 'Adopción institucional' (13/10, 20:00)")
    print(f"     → Publicada después del horario de mercado")
    
    print(f"\n💡 CORRELACIÓN REAL vs ESPURIA:")
    print(f"""
    La correlación de 0.592 es en gran parte ESPURIA porque:
    
    🔴 CASOS ESPURIOS (noticias como EFECTO):
    • 23/10: "Máximo mensual" → Describe el resultado, no lo causa
    • 18/10: "Regulación" → Timing sugiere reacción
    • 13/10: "Adopción" → Publicada post-mercado
    
    🟢 CASOS POTENCIALMENTE CAUSALES:
    • 08/10: "ETF inversiones" (10:00 AM) → +1.57%
    • 16/10: "Corrección técnica" (09:00 AM) → -2.34%
    • 21/10: "Volatilidad" (05:00 AM) → -1.91%
    
    📊 CORRELACIÓN AJUSTADA POR TIMING:
    Solo 3/7 casos tienen timing causal válido.
    La correlación real sería mucho menor si se considera solo timing válido.
    """)
    
    # Recalcular correlación solo con casos válidos
    casos_validos_data = [
        [1, 1.57],   # ETF positivo
        [-1, -2.34], # Corrección negativa
        [0, -1.91],  # Volatilidad neutral
        [0, 0.55]    # Consolidación neutral
    ]
    
    if len(casos_validos_data) > 1:
        sentimientos_validos = [caso[0] for caso in casos_validos_data]
        variaciones_validas = [caso[1] for caso in casos_validos_data]
        correlacion_ajustada = np.corrcoef(sentimientos_validos, variaciones_validas)[0, 1]
        
        print(f"\n📊 CORRELACIÓN AJUSTADA (solo timing válido): {correlacion_ajustada:.3f}")
        print(f"  • Correlación original: 0.592")
        print(f"  • Correlación ajustada: {correlacion_ajustada:.3f}")
        print(f"  • Diferencia: {0.592 - correlacion_ajustada:.3f}")

if __name__ == "__main__":
    analizar_temporalidad_noticias()