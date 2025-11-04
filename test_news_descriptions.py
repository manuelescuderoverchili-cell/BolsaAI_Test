"""
Test específico para verificar extracción de descripciones de noticias
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.news_analyzer import NewsAnalyzer

print("=" * 70)
print("TEST: Extracción de descripciones de noticias")
print("=" * 70)

# Probar con Bitcoin
news_analyzer = NewsAnalyzer("Bitcoin")
noticias = news_analyzer.fetch_news(max_news=10)

print(f"\n✅ Se obtuvieron {len(noticias)} noticias")

if noticias:
    print("\n" + "=" * 70)
    print("ANÁLISIS DE DESCRIPCIONES:")
    print("=" * 70)
    
    con_descripcion = 0
    sin_descripcion = 0
    
    for i, noticia in enumerate(noticias, 1):
        titulo = noticia.get('titulo', 'Sin título')
        descripcion = noticia.get('descripcion', '')
        
        print(f"\n📰 Noticia #{i}")
        print(f"Título: {titulo[:80]}...")
        
        if descripcion and len(descripcion) > 10 and descripcion != titulo:
            print(f"✅ TIENE descripción ({len(descripcion)} chars):")
            print(f"   {descripcion[:150]}...")
            con_descripcion += 1
        else:
            print(f"❌ SIN descripción válida (len={len(descripcion)})")
            sin_descripcion += 1
    
    print("\n" + "=" * 70)
    print("RESUMEN:")
    print("=" * 70)
    print(f"✅ Noticias CON descripción: {con_descripcion}/{len(noticias)} ({con_descripcion/len(noticias)*100:.1f}%)")
    print(f"❌ Noticias SIN descripción: {sin_descripcion}/{len(noticias)} ({sin_descripcion/len(noticias)*100:.1f}%)")
    
    if con_descripcion == 0:
        print("\n⚠️ PROBLEMA: Ninguna noticia tiene descripción válida")
        print("   Esto puede deberse a:")
        print("   - Fuentes RSS que no incluyen el campo 'summary' o 'description'")
        print("   - Problemas con la limpieza de HTML")
        print("   - Campos vacíos en las fuentes")
    elif con_descripcion < len(noticias) * 0.5:
        print("\n⚠️ ADVERTENCIA: Menos del 50% de noticias tienen descripción")
    else:
        print("\n✅ CORRECTO: La mayoría de noticias tienen descripción")
else:
    print("❌ No se encontraron noticias")
