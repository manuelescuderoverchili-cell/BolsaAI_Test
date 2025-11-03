import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def analizar_correlacion_detallada():
    """
    Análisis detallado para mostrar exactamente dónde está la correlación
    """
    print("🔍 ANÁLISIS DETALLADO DE LA CORRELACIÓN MENSUAL")
    print("="*60)
    
    # Datos específicos de los días con noticias
    datos_correlacion = [
        # [Fecha, Sentimiento (1=pos, 0=neu, -1=neg), Variación_diaria, Precio, Noticia]
        ["2025-10-08", 1, 1.57, 123354.87, "Bitcoin ETF recibe nuevas inversiones"],
        ["2025-10-13", 1, 0.09, 115271.08, "Adopción institucional de Bitcoin se acelera"],
        ["2025-10-16", -1, -2.34, 108186.04, "Corrección técnica en Bitcoin"],
        ["2025-10-18", -1, 0.69, 107198.27, "Regulación cripto genera incertidumbre"],
        ["2025-10-21", 0, -1.91, 108476.89, "Volatilidad en mercados crypto"],
        ["2025-10-23", 1, 2.21, 110069.73, "Bitcoin alcanza máximo mensual"],
        ["2025-10-25", 0, 0.55, 111641.73, "Análisis técnico sugiere consolidación"]
    ]
    
    # Crear DataFrame
    df = pd.DataFrame(datos_correlacion, columns=['Fecha', 'Sentimiento', 'Variacion_%', 'Precio', 'Noticia'])
    
    print("📊 DATOS PUNTO POR PUNTO:")
    print(df.to_string(index=False))
    
    # Calcular correlación
    correlacion = np.corrcoef(df['Sentimiento'], df['Variacion_%'])[0, 1]
    print(f"\n🔗 Correlación calculada: {correlacion:.3f}")
    
    # Análisis por sentimiento
    print(f"\n📈 ANÁLISIS POR SENTIMIENTO:")
    
    positivas = df[df['Sentimiento'] == 1]
    negativas = df[df['Sentimiento'] == -1]
    neutrales = df[df['Sentimiento'] == 0]
    
    print(f"NOTICIAS POSITIVAS ({len(positivas)} casos):")
    for _, row in positivas.iterrows():
        print(f"  • {row['Fecha']}: {row['Variacion_%']:+.2f}% - {row['Noticia']}")
    if not positivas.empty:
        print(f"  → Promedio variación: {positivas['Variacion_%'].mean():+.2f}%")
    
    print(f"\nNOTICIAS NEGATIVAS ({len(negativas)} casos):")
    for _, row in negativas.iterrows():
        print(f"  • {row['Fecha']}: {row['Variacion_%']:+.2f}% - {row['Noticia']}")
    if not negativas.empty:
        print(f"  → Promedio variación: {negativas['Variacion_%'].mean():+.2f}%")
    
    print(f"\nNOTICIAS NEUTRALES ({len(neutrales)} casos):")
    for _, row in neutrales.iterrows():
        print(f"  • {row['Fecha']}: {row['Variacion_%']:+.2f}% - {row['Noticia']}")
    if not neutrales.empty:
        print(f"  → Promedio variación: {neutrales['Variacion_%'].mean():+.2f}%")
    
    # Verificar la correlación
    print(f"\n🎯 ¿DÓNDE ESTÁ LA CORRELACIÓN?")
    
    print(f"\n✅ CASOS QUE APOYAN LA CORRELACIÓN:")
    casos_coherentes = 0
    casos_totales = len(df)
    
    for _, row in df.iterrows():
        sent = row['Sentimiento']
        var = row['Variacion_%']
        
        if (sent > 0 and var > 0) or (sent < 0 and var < 0):
            casos_coherentes += 1
            direccion = "📈 Positiva → Subida" if sent > 0 else "📉 Negativa → Bajada"
            print(f"  • {row['Fecha']}: {direccion} ({var:+.2f}%)")
    
    print(f"\n⚠️ CASOS QUE VAN CONTRA LA CORRELACIÓN:")
    for _, row in df.iterrows():
        sent = row['Sentimiento']
        var = row['Variacion_%']
        
        if (sent > 0 and var < 0) or (sent < 0 and var > 0):
            direccion = "📈→📉 Positiva pero Bajada" if sent > 0 else "📉→📈 Negativa pero Subida"
            print(f"  • {row['Fecha']}: {direccion} ({var:+.2f}%)")
    
    print(f"\n📊 RESUMEN:")
    print(f"  • Casos coherentes: {casos_coherentes}/{casos_totales} ({casos_coherentes/casos_totales*100:.1f}%)")
    print(f"  • Correlación: {correlacion:.3f}")
    
    # Crear gráfico específico
    plt.figure(figsize=(12, 8))
    
    # Subplot 1: Scatter plot
    plt.subplot(2, 1, 1)
    colors = ['red' if s == -1 else 'gray' if s == 0 else 'green' for s in df['Sentimiento']]
    plt.scatter(df['Sentimiento'], df['Variacion_%'], c=colors, s=100, alpha=0.7)
    
    # Añadir línea de tendencia
    z = np.polyfit(df['Sentimiento'], df['Variacion_%'], 1)
    p = np.poly1d(z)
    x_line = np.linspace(-1, 1, 100)
    plt.plot(x_line, p(x_line), "r--", alpha=0.8, linewidth=2)
    
    plt.xlabel('Sentimiento (-1: Negativo, 0: Neutral, 1: Positivo)')
    plt.ylabel('Variación Diaria (%)')
    plt.title(f'Correlación Sentimiento vs Precio (r = {correlacion:.3f})')
    plt.grid(True, alpha=0.3)
    plt.axhline(y=0, color='black', linestyle='-', alpha=0.3)
    plt.axvline(x=0, color='black', linestyle='-', alpha=0.3)
    
    # Anotar puntos
    for i, row in df.iterrows():
        plt.annotate(f"{row['Fecha'][8:10]}/{row['Fecha'][5:7]}", 
                    (row['Sentimiento'], row['Variacion_%']),
                    xytext=(5, 5), textcoords='offset points', fontsize=8)
    
    # Subplot 2: Barras por fecha
    plt.subplot(2, 1, 2)
    fechas_cortas = [fecha[8:10] + "/" + fecha[5:7] for fecha in df['Fecha']]
    
    # Crear barras de variación coloreadas por sentimiento
    bars = plt.bar(range(len(df)), df['Variacion_%'], 
                   color=['red' if s == -1 else 'gray' if s == 0 else 'green' for s in df['Sentimiento']],
                   alpha=0.7)
    
    plt.xlabel('Fecha (DD/MM)')
    plt.ylabel('Variación Diaria (%)')
    plt.title('Variación Diaria por Fecha (Color = Sentimiento)')
    plt.xticks(range(len(df)), fechas_cortas, rotation=45)
    plt.grid(True, alpha=0.3)
    plt.axhline(y=0, color='black', linestyle='-', alpha=0.3)
    
    # Añadir leyenda
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor='green', alpha=0.7, label='Positivo'),
                      Patch(facecolor='gray', alpha=0.7, label='Neutral'),
                      Patch(facecolor='red', alpha=0.7, label='Negativo')]
    plt.legend(handles=legend_elements)
    
    plt.tight_layout()
    plt.savefig('correlacion_detallada_analisis.png', dpi=300, bbox_inches='tight')
    print(f"\n💾 Gráfico guardado: correlacion_detallada_analisis.png")
    plt.show()
    
    # Conclusión sobre por qué hay correlación
    print(f"\n🎯 ¿POR QUÉ HAY CORRELACIÓN DE 0.592?")
    print(f"""
    La correlación existe porque:
    
    1. 📈 NOTICIAS POSITIVAS → SUBIDAS:
       • 08/10: ETF inversiones → +1.57%
       • 23/10: Máximo mensual → +2.21%
       (2 de 3 noticias positivas tuvieron subidas)
    
    2. 📉 NOTICIAS NEGATIVAS → COMPORTAMIENTO MIXTO:
       • 16/10: Corrección técnica → -2.34% ✓
       • 18/10: Regulación → +0.69% ✗ (contraditorio)
    
    3. 📊 NOTICIAS NEUTRALES → VARIACIÓN MENOR:
       • Promedio de variación más contenido
    
    4. 🔍 PATRÓN IDENTIFICADO:
       • Las noticias positivas tienden a coincidir con días alcistas
       • Las noticias negativas son más mixtas
       • Esto genera una correlación moderada-fuerte (0.592)
    
    IMPORTANTE: Esta correlación está basada en datos simulados
    para demostrar la metodología. En un análisis real con noticias 
    reales de feeds RSS, los resultados serían diferentes.
    """)

if __name__ == "__main__":
    analizar_correlacion_detallada()