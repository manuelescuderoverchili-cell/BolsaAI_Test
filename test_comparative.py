"""
Test del analizador comparativo
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from comparative_analyzer import ComparativeAnalyzer

print("🔍 Iniciando análisis comparativo de TODOS los activos...")
print("⚠️ Esto puede tardar varios minutos...\n")

# Crear analizador
comparative = ComparativeAnalyzer()

# Callback de progreso
def show_progress(message, progress):
    print(f"[{progress*100:.0f}%] {message}")

# Analizar todos los activos (periodo corto para test rápido)
results = comparative.analyze_all_assets(
    period="7d",  # Solo 7 días para test rápido
    interval="1d",
    progress_callback=show_progress
)

print(f"\n✅ Análisis completado: {len(results)} activos analizados\n")

# Generar reporte
report = comparative.generate_comparative_report()
print(report)

# Exportar a CSV
csv_path = comparative.export_to_csv()
print(f"\n✅ CSV generado: {csv_path}")

# Generar PDF con razones detalladas
print("\n📄 Generando PDF con análisis detallado...")
pdf_path = comparative.generate_pdf_report(period="1 semana", interval="1 día")
if pdf_path:
    print(f"✅ PDF comparativo generado: {pdf_path}")

# Mostrar top 3
print("\n" + "="*80)
print("🏆 TOP 3 MEJORES OPORTUNIDADES:")
print("="*80)
for i, r in enumerate(results[:3], 1):
    print(f"\n{i}. {r['activo']} - {r['categoria']}")
    print(f"   Score: {r['score_rentabilidad']:.1f}/100")
    print(f"   Recomendación: {r['recomendacion']}")
    print(f"   Retorno esperado: {r['retorno_esperado']:+.2f}%")
