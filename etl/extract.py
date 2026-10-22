import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Función matemática para generar probabilidades realistas
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def generar_datos_crudos(num_registros=15000):
    print("📥 [EXTRACT] Generando datos crudos (V0 - Inmutable) con Distribución Sigmoide...")
    np.random.seed(42)
    random.seed(42)

    tiendas = ['Jinotepe', 'Diriamba', 'San Marcos', 'Masatepe', 'Managua Sur']
    canales = ['Tienda', 'Web', 'WhatsApp', 'Mayorista']
    familias = ['Abarrotes', 'Lácteos', 'Higiene', 'Bebidas', 'Congelados']
    promociones = ['Sin promoción', '2x1', '2X1', 'Descuento', 'DESCUENTO', 'Combo', 'COMBO', 'Temporada']
    abc_list = ['A', 'B', 'C']
    sistemas = ['POS', 'WMS', 'Compras', 'E-commerce']

    fecha_inicio = datetime(2024, 7, 1)
    fechas_semanales = [fecha_inicio + timedelta(weeks=i) for i in range(104)]

    data = []
    for i in range(1, num_registros + 1):
        inicio_sem = random.choice(fechas_semanales)
        tienda = random.choice(tiendas)
        familia = random.choice(familias)
        promocion = random.choice(promociones)
        clasificacion_abc = random.choice(abc_list)
        
        # Inyectamos nulos para Auditoría
        canal = random.choice(canales) if random.random() > 0.05 else None 
        
        # Variables base realistas
        inv_inicial = int(np.random.normal(150, 50))
        inv_inicial = max(10, inv_inicial)

        if promocion in ['2x1', '2X1', 'Temporada', 'Combo', 'COMBO']:
            ventas = int(np.random.normal(130, 30))
        else:
            ventas = int(np.random.normal(70, 20))
            
        # Inyectamos valores fuera de rango para Auditoría
        if random.random() < 0.04:
            ventas = random.choice([-10, 300, 500]) 
        else:
            ventas = max(5, min(240, ventas))

        if familia in ['Lácteos', 'Congelados'] and tienda in ['Jinotepe', 'Managua Sur']:
            dias_retraso = int(np.random.normal(6, 2))
        else:
            dias_retraso = int(np.random.normal(2, 1))
        dias_retraso = max(0, min(18, dias_retraso))
        
        dias_cobertura = random.randint(0, 35)

        # ========================================================
        # GENERACIÓN DE TARGETS CON SIGMOIDE Y RUIDO GAUSSIANO
        # ========================================================
        
# 1. TARGET 1: Quiebre de Stock (KPI 1)
        score_q = -3.2 # Ajuste leve de anclaje
        if canal in ['Web', 'WhatsApp']: score_q += 1.4
        if promocion in ['2x1', '2X1', 'Temporada']: score_q += 1.4
        if dias_retraso > 4: score_q += 1.8
        if ventas > (inv_inicial * 0.8): score_q += 2.2
        
        # CAMBIO CLAVE: Reducimos la dispersión del ruido de 1.0 a 0.6 para afilar la precisión
        prob_q = sigmoid(score_q + np.random.normal(0, 0.6)) 
        quiebre = 1 if random.random() < prob_q else 0
        if random.random() < 0.03: quiebre = None
        
        prob_q = sigmoid(score_q + np.random.normal(0, 1.0)) 
        quiebre = 1 if random.random() < prob_q else 0
        if random.random() < 0.03: quiebre = None 

        # 2. TARGET 2: Retraso Crítico (KPI 4) - Ajustado a ~20%
        score_r = -3.0
        if familia in ['Lácteos', 'Congelados']: score_r += 2.0
        if tienda in ['Jinotepe', 'Managua Sur']: score_r += 1.5
        if ventas > 100: score_r += 1.0
        
        prob_r = sigmoid(score_r + np.random.normal(0, 1.0))
        retraso_critico = 1 if random.random() < prob_r else 0

        # 3. TARGET 3: Riesgo de Estancamiento / Sobreinventario (KPI 2) - Ajustado a ~15%
        score_est = -3.0
        if clasificacion_abc == 'C': score_est += 2.0
        if promocion in ['Sin promoción']: score_est += 1.5
        if inv_inicial > 200: score_est += 1.5
        if familia == 'Higiene': score_est += 1.0
        
        prob_est = sigmoid(score_est + np.random.normal(0, 1.0))
        estancamiento = 1 if random.random() < prob_est else 0

        # 4. TARGET 4: Alta Rotación (KPI 9) - Ajustado a ~25%
        score_rot = -3.0
        if familia in ['Abarrotes', 'Bebidas']: score_rot += 1.5
        if canal in ['Web', 'Mayorista']: score_rot += 1.5
        if promocion in ['Descuento', 'DESCUENTO', 'Combo', 'COMBO']: score_rot += 2.0
        
        prob_rot = sigmoid(score_rot + np.random.normal(0, 1.0))
        alta_rotacion = 1 if random.random() < prob_rot else 0

        data.append({
            'id_producto_tienda_semana': f"REG-{i:05d}",
            'inicio_semana': inicio_sem.strftime('%Y-%m-%d'),
            'tienda': tienda,
            'canal_venta': canal,
            'familia_producto': familia,
            'tipo_promocion': promocion,
            'ventas_unidades': ventas,
            'dias_cobertura': dias_cobertura,
            'inventario_inicial': inv_inicial,
            'dias_retraso_proveedor': dias_retraso,
            'clasificacion_abc': clasificacion_abc,
            'sistema_origen': random.choice(sistemas),
            'quiebre_stock': quiebre,
            'target_retraso_critico': retraso_critico,
            'target_estancamiento': estancamiento,
            'target_alta_rotacion': alta_rotacion
        })

    return pd.DataFrame(data)