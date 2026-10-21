import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def generar_datos_crudos(num_registros=15000):
    print("📥 [EXTRACT] Generando datos crudos (V0 - Inmutable)...")
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
        
        # Inyectamos nulos para Auditoría
        canal = random.choice(canales) if random.random() > 0.05 else None 
        
        # Inyectamos valores fuera de rango para Auditoría
        if random.random() < 0.04:
            ventas = random.choice([-10, 300, 500]) 
        else:
            ventas = int(np.random.normal(loc=120, scale=40))
            ventas = max(5, min(240, ventas))

        dias_retraso = random.randint(0, 18)
        dias_cobertura = random.randint(0, 35)
        inv_inicial = random.randint(0, 420)

        # ========================================================
        # LA MATEMÁTICA PARA MINERÍA (Ajuste fino al 39.4%)
        # ========================================================
        
        # 1. TARGET 1: Quiebre de Stock (Ajustado matemáticamente)
        prob_quiebre = 0.05 # Base 5%
        
        # Sumamos probabilidad (Pesos ajustados para promediar ~39.4% global)
        if canal in ['Web', 'WhatsApp']: prob_quiebre += 0.20
        if promocion in ['2x1', '2X1', 'Temporada']: prob_quiebre += 0.20
        if dias_retraso > 4: prob_quiebre += 0.15
        if tienda in ['Managua Sur', 'Jinotepe']: prob_quiebre += 0.15
        
        prob_quiebre = min(0.95, prob_quiebre) # Tope máximo
        
        # Generamos el quiebre basado en la probabilidad real
        if random.random() < 0.03:
            quiebre = None # 3% nulos para Auditoría
        else:
            quiebre = 1 if random.random() < prob_quiebre else 0

        # 2. TARGET 2: Retraso Crítico
        retraso_critico = 1 if dias_retraso > 4 else 0
            
        # 3. TARGET 3: Falso Quiebre
        falso_quiebre = 1 if (canal in ['Web', 'WhatsApp'] and inv_inicial > 100 and quiebre == 1) else 0
        
        # 4. TARGET 4: Pico de Demanda
        pico_demanda = 1 if (promocion in ['2x1', '2X1', 'Temporada'] and ventas > 150) else 0

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
            'clasificacion_abc': random.choice(abc_list),
            'sistema_origen': random.choice(sistemas),
            'quiebre_stock': quiebre,
            'target_retraso_critico': retraso_critico,
            'target_falso_quiebre': falso_quiebre,
            'target_pico_demanda': pico_demanda
        })

    return pd.DataFrame(data)