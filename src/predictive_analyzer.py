"""
Analizador predictivo basado en patrones técnicos detectados
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
from datetime import datetime, timedelta


class PredictiveAnalyzer:
    """Clase para realizar predicciones basadas en patrones históricos"""
    
    def __init__(self, data: pd.DataFrame, patterns: Dict):
        """
        Inicializa el analizador predictivo
        
        Args:
            data: DataFrame con datos históricos
            patterns: Diccionario con patrones detectados
        """
        self.data = data.copy()
        self.patterns = patterns
        self.predictions = []
        
    def analyze_pattern_effectiveness(self) -> Dict:
        """
        Analiza la efectividad de los patrones detectados para predecir movimientos
        
        Returns:
            Diccionario con análisis de efectividad
        """
        effectiveness = {
            'patrones_alcistas_acertados': 0,
            'patrones_bajistas_acertados': 0,
            'patrones_totales': 0,
            'precision_alcista': 0,
            'precision_bajista': 0,
            'casos_analizados': []
        }
        
        all_patterns = self.patterns.get('todos', [])
        
        for pattern in all_patterns:
            # Solo analizar patrones que no sean del último día
            fecha_patron = pattern['fecha']
            
            # Buscar el índice del patrón en los datos
            try:
                idx = self.data.index.get_loc(fecha_patron)
                
                # Si no es el último registro, podemos verificar qué pasó después
                if idx < len(self.data) - 1:
                    precio_patron = self.data['Close'].iloc[idx]
                    
                    # Mirar los próximos 5 días (o lo que haya disponible)
                    dias_futuros = min(5, len(self.data) - idx - 1)
                    precio_futuro = self.data['Close'].iloc[idx + dias_futuros]
                    
                    cambio_porcentual = ((precio_futuro - precio_patron) / precio_patron) * 100
                    
                    tipo_patron = pattern.get('tipo', pattern.get('señal', 'Neutral'))
                    
                    # Verificar si la predicción fue correcta
                    if tipo_patron == 'Alcista' and cambio_porcentual > 0:
                        effectiveness['patrones_alcistas_acertados'] += 1
                        acierto = True
                    elif tipo_patron == 'Bajista' and cambio_porcentual < 0:
                        effectiveness['patrones_bajistas_acertados'] += 1
                        acierto = True
                    else:
                        acierto = False
                    
                    effectiveness['patrones_totales'] += 1
                    
                    effectiveness['casos_analizados'].append({
                        'patron': pattern.get('patron', pattern.get('tipo')),
                        'fecha': fecha_patron,
                        'tipo_esperado': tipo_patron,
                        'cambio_real': cambio_porcentual,
                        'acierto': acierto,
                        'dias_analisis': dias_futuros
                    })
                    
            except (KeyError, ValueError):
                continue
        
        # Calcular precisión
        if effectiveness['patrones_totales'] > 0:
            total_acertados = (effectiveness['patrones_alcistas_acertados'] + 
                             effectiveness['patrones_bajistas_acertados'])
            effectiveness['precision_general'] = (total_acertados / effectiveness['patrones_totales']) * 100
        else:
            effectiveness['precision_general'] = 0
        
        return effectiveness
    
    def predict_next_movements(self) -> Dict:
        """
        Predice movimientos futuros basándose en patrones recientes
        
        Returns:
            Diccionario con predicciones
        """
        predictions = {
            'direccion_probable': 'Neutral',
            'confianza': 0,
            'rango_precio_estimado': {},
            'escenarios': [],
            'patrones_activos': []
        }
        
        # Analizar los patrones más recientes (últimos 5 días)
        recent_patterns = []
        fecha_limite = self.data.index[-1] - timedelta(days=5)
        
        for pattern in self.patterns.get('todos', []):
            if pattern['fecha'] >= fecha_limite:
                recent_patterns.append(pattern)
        
        # Establecer valores por defecto basados en precio actual
        precio_actual = self.data['Close'].iloc[-1]
        volatilidad = self.data['Close'].pct_change().std() * 100
        
        if not recent_patterns:
            # Sin patrones recientes, asumir neutral
            predictions['direccion_probable'] = 'Neutral/Lateral'
            predictions['confianza'] = 50
            predictions['rango_precio_estimado'] = {
                'minimo': precio_actual * (1 - volatilidad/100),
                'maximo': precio_actual * (1 + volatilidad/100),
                'objetivo': precio_actual
            }
            predictions['escenarios'] = [
                {
                    'nombre': 'Optimista',
                    'probabilidad': 30,
                    'precio_objetivo': predictions['rango_precio_estimado']['maximo'],
                    'descripcion': 'El mercado se mueve favorablemente sin señales claras',
                    'fundamento': 'Movimiento favorable sin patrones detectados'
                },
                {
                    'nombre': 'Base',
                    'probabilidad': 50,
                    'precio_objetivo': predictions['rango_precio_estimado']['objetivo'],
                    'descripcion': 'El mercado se mantiene estable',
                    'fundamento': 'Precio se mantiene estable sin señales claras'
                },
                {
                    'nombre': 'Pesimista',
                    'probabilidad': 30,
                    'precio_objetivo': predictions['rango_precio_estimado']['minimo'],
                    'descripcion': 'El mercado se mueve desfavorablemente sin señales claras',
                    'fundamento': 'Movimiento desfavorable sin patrones detectados'
                }
            ]
            return predictions
        
        # Contar señales alcistas y bajistas
        señales_alcistas = 0
        señales_bajistas = 0
        peso_total_alcista = 0
        peso_total_bajista = 0
        
        pesos_confianza = {
            'Muy Alta': 3,
            'Alta': 2,
            'Media': 1,
            'Baja': 0.5
        }
        
        for pattern in recent_patterns:
            tipo = pattern.get('tipo', pattern.get('señal', 'Neutral'))
            confianza = pattern.get('confianza', 'Media')
            peso = pesos_confianza.get(confianza, 1)
            
            if tipo == 'Alcista':
                señales_alcistas += 1
                peso_total_alcista += peso
                predictions['patrones_activos'].append({
                    'patron': pattern.get('patron', pattern.get('tipo')),
                    'tipo': 'Alcista',
                    'peso': peso
                })
            elif tipo == 'Bajista':
                señales_bajistas += 1
                peso_total_bajista += peso
                predictions['patrones_activos'].append({
                    'patron': pattern.get('patron', pattern.get('tipo')),
                    'tipo': 'Bajista',
                    'peso': peso
                })
        
        # Determinar dirección probable
        if peso_total_alcista > peso_total_bajista * 1.5:
            predictions['direccion_probable'] = 'Alcista'
            predictions['confianza'] = min(90, (peso_total_alcista / (peso_total_alcista + peso_total_bajista)) * 100)
        elif peso_total_bajista > peso_total_alcista * 1.5:
            predictions['direccion_probable'] = 'Bajista'
            predictions['confianza'] = min(90, (peso_total_bajista / (peso_total_alcista + peso_total_bajista)) * 100)
        else:
            predictions['direccion_probable'] = 'Neutral/Lateral'
            predictions['confianza'] = 50
        
        # Rango de precio ya calculado arriba, reutilizarlo si no hay patrones
        # pero actualizar basándose en la dirección si hay patrones
        if recent_patterns:
            # Estimar rango de precio para los próximos días basado en patrones
            if predictions['direccion_probable'] == 'Alcista':
                predictions['rango_precio_estimado'] = {
                    'minimo': precio_actual * (1 - volatilidad/100),
                    'maximo': precio_actual * (1 + volatilidad*1.5/100),
                    'objetivo': precio_actual * (1 + volatilidad/100)
                }
            elif predictions['direccion_probable'] == 'Bajista':
                predictions['rango_precio_estimado'] = {
                    'minimo': precio_actual * (1 - volatilidad*1.5/100),
                    'maximo': precio_actual * (1 + volatilidad/100),
                    'objetivo': precio_actual * (1 - volatilidad/100)
                }
            else:
                predictions['rango_precio_estimado'] = {
                    'minimo': precio_actual * (1 - volatilidad/100),
                    'maximo': precio_actual * (1 + volatilidad/100),
                    'objetivo': precio_actual
                }
        
        # Generar escenarios
        predictions['escenarios'] = [
            {
                'nombre': 'Optimista',
                'probabilidad': predictions['confianza'] if predictions['direccion_probable'] == 'Alcista' else 30,
                'precio_objetivo': predictions['rango_precio_estimado']['maximo'],
                'descripcion': 'Los patrones alcistas se confirman y el precio sube',
                'fundamento': 'Los patrones alcistas se confirman y el precio sube'
            },
            {
                'nombre': 'Base',
                'probabilidad': 50,
                'precio_objetivo': predictions['rango_precio_estimado']['objetivo'],
                'descripcion': 'El mercado se mueve según las tendencias detectadas',
                'fundamento': 'El mercado se mueve según las tendencias detectadas'
            },
            {
                'nombre': 'Pesimista',
                'probabilidad': predictions['confianza'] if predictions['direccion_probable'] == 'Bajista' else 30,
                'precio_objetivo': predictions['rango_precio_estimado']['minimo'],
                'descripcion': 'Los patrones bajistas se confirman y el precio cae',
                'fundamento': 'Los patrones bajistas se confirman y el precio cae'
            }
        ]
        
        return predictions
    
    def generate_prediction_report(self) -> str:
        """
        Genera un reporte de predicciones
        
        Returns:
            String con el reporte
        """
        effectiveness = self.analyze_pattern_effectiveness()
        predictions = self.predict_next_movements()
        
        report = """
╔══════════════════════════════════════════════════════════════╗
║           ANÁLISIS PREDICTIVO BASADO EN PATRONES
╚══════════════════════════════════════════════════════════════╝

📊 EFECTIVIDAD HISTÓRICA DE PATRONES:
"""
        
        if effectiveness['patrones_totales'] > 0:
            report += f"""
   • Patrones analizados: {effectiveness['patrones_totales']}
   • Patrones alcistas acertados: {effectiveness['patrones_alcistas_acertados']}
   • Patrones bajistas acertados: {effectiveness['patrones_bajistas_acertados']}
   • Precisión general: {effectiveness['precision_general']:.1f}%

   📈 Casos de éxito recientes:
"""
            for caso in effectiveness['casos_analizados'][:5]:
                if caso['acierto']:
                    emoji = "✅"
                    fecha_str = caso['fecha'].strftime("%d/%m/%Y") if hasattr(caso['fecha'], 'strftime') else str(caso['fecha'])
                    report += f"   {emoji} {caso['patron']} ({fecha_str}) → Cambio real: {caso['cambio_real']:+.2f}%\n"
        else:
            report += "\n   ℹ️ Insuficientes datos históricos para validar patrones\n"
        
        report += f"""
🔮 PREDICCIÓN PARA LOS PRÓXIMOS DÍAS:

   Dirección probable: {predictions['direccion_probable'].upper()}
   Nivel de confianza: {predictions['confianza']:.1f}%

   💰 Rango de precio estimado:
   • Mínimo: ${predictions['rango_precio_estimado']['minimo']:,.2f}
   • Objetivo: ${predictions['rango_precio_estimado']['objetivo']:,.2f}
   • Máximo: ${predictions['rango_precio_estimado']['maximo']:,.2f}

   📋 Patrones activos considerados:
"""
        
        for p in predictions['patrones_activos'][:5]:
            emoji = "📈" if p['tipo'] == 'Alcista' else "📉"
            report += f"   {emoji} {p['patron']} (Peso: {p['peso']})\n"
        
        report += "\n   📊 ESCENARIOS POSIBLES:\n\n"
        
        for escenario in predictions['escenarios']:
            report += f"   {escenario['nombre']}:\n"
            report += f"   • Probabilidad: {escenario['probabilidad']:.0f}%\n"
            report += f"   • Precio objetivo: ${escenario['precio_objetivo']:,.2f}\n"
            report += f"   • {escenario['descripcion']}\n\n"
        
        return report, predictions
