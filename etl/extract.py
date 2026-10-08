import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def generar_datos_crudos(num_registros=15000):
    print("📥 [EXTRACT] Generando datos crudos")
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
        canal = random.choice(canales) if random.random() > 0.03 else None
        promocion = random.choice(promociones)
        
        ventas = int(np.random.normal(loc=120, scale=50))
        dias_retraso = random.randint(0, 18)
        dias_cobertura = random.randint(0, 35)
        inv_inicial = random.randint(0, 420)
        
        # ==========================================
        # LÓGICA CALIBRADA PARA ACERCARSE AL 39.4%
        # ==========================================
        prob_quiebre = 0.05  # Probabilidad base muy baja (5%)
        
        # Sumamos pesos solo si se cumplen las condiciones de riesgo
        if canal in ['Web', 'WhatsApp']: prob_quiebre += 0.15
        if promocion in ['2x1', '2X1', 'Temporada']: prob_quiebre += 0.18
        if tienda in ['Managua Sur', 'Jinotepe']: prob_quiebre += 0.12
        if dias_retraso > 4: prob_quiebre += 0.15
            
        # POL-CAL-01: Inyección de nulos (datos no consolidados)
        if random.random() < 0.03:
            quiebre = None
        else:
            # Determinamos el quiebre basados en la probabilidad calculada
            quiebre = 1 if random.random() < prob_quiebre else 0

        data.append({
            'id_producto_tienda_semana': f"REG-{i:05d}",
            'inicio_semana': inicio_sem.strftime('%Y-%m-%d'),
            'tienda': tienda,
            'canal_venta': canal,
            'familia_producto': random.choice(familias),
            'tipo_promocion': promocion,
            'ventas_unidades': ventas,
            'dias_cobertura': dias_cobertura,
            'inventario_inicial': inv_inicial,
            'dias_retraso_proveedor': dias_retraso,
            'clasificacion_abc': random.choice(abc_list),
            'sistema_origen': random.choice(sistemas),
            'quiebre_stock': quiebre
        })

    return pd.DataFrame(data)