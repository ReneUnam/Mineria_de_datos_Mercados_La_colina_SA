import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-np.clip(x, -20, 20)))

def generar_datos_crudos(num_registros=15000):
    print(f"📥 [EXTRACT] Generando {num_registros:,} registros con Fricción Operativa Realista (PDF)...")
    np.random.seed(42)
    random.seed(42)

    # 1. Proporciones marginales reales del PDF (Informes 2, 3 y 4)
    canales = ['WhatsApp', 'Web', 'Tienda', 'Mayorista']
    p_canales = [0.302, 0.299, 0.211, 0.188]

    promociones = ['Descuento', '2x1', 'Temporada', 'Sin promoción', 'Combo']
    p_promociones = [0.231, 0.222, 0.208, 0.181, 0.158]

    tiendas = ['Managua Sur', 'Jinotepe', 'Diriamba', 'San Marcos', 'Masatepe']
    p_tiendas = [0.217, 0.206, 0.200, 0.194, 0.183]

    familias = ['Abarrotes', 'Lácteos', 'Higiene', 'Bebidas', 'Congelados']
    abc_list = ['A', 'B', 'C']
    sistemas = ['POS', 'WMS', 'Compras', 'E-commerce']

    fecha_inicio = datetime(2024, 7, 1)
    fechas_semanales = [fecha_inicio + timedelta(weeks=i) for i in range(104)]

    data = []
    for i in range(1, num_registros + 1):
        inicio_sem = random.choice(fechas_semanales)
        sistema_origen = random.choice(sistemas)
        clasificacion_abc = random.choice(abc_list)
        familia = random.choice(familias)

        canal = np.random.choice(canales, p=p_canales)
        promo_base = np.random.choice(promociones, p=p_promociones)
        tienda = np.random.choice(tiendas, p=p_tiendas)

        # ----------------------------------------------------
        # Variables operativas continuas con distribución realista
        # ----------------------------------------------------
        # Ventas (Promociones masivas generan picos de demanda según Informe 3)
        if promo_base in ['2x1', 'Temporada']:
            ventas_base = int(np.random.normal(140, 30))
        elif promo_base == 'Sin promoción':
            ventas_base = int(np.random.normal(90, 25))
        else:
            ventas_base = int(np.random.normal(115, 25))
        ventas = int(np.clip(ventas_base, 5, 240))

        # Inventario inicial en tienda
        inv_inicial = int(np.clip(np.random.normal(165, 55), 20, 420))

        # Días de demora de proveedores (Lácteos y Congelados sufren más según Hallazgo 5)
        if familia in ['Lácteos', 'Congelados'] and tienda in ['Managua Sur', 'Jinotepe']:
            dias_retraso = int(np.clip(np.random.normal(9.5, 3.5), 0, 18))
        else:
            dias_retraso = int(np.clip(np.random.normal(5.0, 3.0), 0, 18))

        # Días de cobertura
        consumo_diario = max(ventas / 7.0, 1.0)
        cobertura_teorica = inv_inicial / consumo_diario
        dias_cobertura = int(np.clip(cobertura_teorica + np.random.normal(0, 2.0), 0, 35))

        # =================================================================
        # ÍNDICE DE FRICCIÓN OPERATIVA DEL CASO DE ESTUDIO 
        # =================================================================
        friccion = 0

        # 1. Tensión de inventario físico
        ratio = ventas / max(inv_inicial, 1)
        if ratio >= 1.0:
            friccion += 35
        elif ratio >= 0.75:
            friccion += 20
        elif ratio < 0.40:
            friccion -= 25

        # 2. Logística de Entrada: Retraso de proveedor (Hallazgo 5)
        if dias_retraso > 4:
            friccion += 25
        else:
            friccion -= 15  # WMS repuso a tiempo de noche

        # 3. Canales Digitales y Mayorista (Informe 2: WhatsApp 43% y Mayorista 52%)
        if canal == 'Mayorista':
            friccion += 20
        elif canal == 'WhatsApp':
            friccion += 15
        elif canal == 'Tienda':
            friccion -= 10  # Tienda física es el canal más seguro (31%)

        # 4. Asfixia por Promoción (Informe 3: Temporada 50% y 2x1 42%)
        if promo_base == 'Temporada':
            friccion += 20
        elif promo_base == '2x1':
            friccion += 12
        elif promo_base == 'Descuento':
            friccion -= 10

        # 5. Cuello de botella geográfico (Informe 4 / Hallazgo 4: Managua Sur y Jinotepe)
        if tienda in ['Managua Sur', 'Jinotepe']:
            friccion += 10

        # 6. Criticidad ABC (Hallazgo 9: Productos A rotan y quiebran; C se estancan)
        if clasificacion_abc == 'A':
            friccion += 10
        elif clasificacion_abc == 'C':
            friccion -= 20

        # =================================================================
        # MAPEO A PROBABILIDADES CALIBRADAS (Tasa global objetivo: ~39.3%)
        # =================================================================
        if friccion >= 50:
            prob_quiebre = 0.85  # Alto riesgo: 20% se salvan por traslados nocturnos
        elif friccion >= 28:
            prob_quiebre = 0.50  # Riesgo medio
        elif friccion >= 5:
            prob_quiebre = 0.14  # Riesgo bajo
        else:
            prob_quiebre = 0.03  # Muy seguro: 3% merma/rotura accidental

        quiebre_real = 1 if random.random() < prob_quiebre else 0

        # =================================================================
        # TARGETS SECUNDARIOS PARA LOS OTROS 3 NOTEBOOKS (Calibrados)
        # =================================================================
        
        # Retraso Crítico (KPI 4): Compras (~22% base)
        score_ret = -2.60
        if familia in ['Lácteos', 'Congelados']: score_ret += 1.80       # Fricción de refrigeración
        if tienda in ['Managua Sur', 'Jinotepe']: score_ret += 1.20       # Cuello de botella en ruta
        if sistema_origen in ['Compras', 'E-commerce']: score_ret += 1.00 # Hallazgo 10: Compras en Excel genera desfase
        if ventas > 120: score_ret += 1.00                               # Pedidos de gran volumen
        
        retraso_critico = 1 if random.random() < sigmoid(score_ret) else 0

        #Preferencia de Canal Digital (Comportamiento Humano / Omnicanal - ~35% base)
        # Factores: Urbanismo (tráfico), conveniencia de carga pesada y compras de impulso (FOMO)
        score_dig = -1.50
        if tienda == 'Managua Sur': score_dig += 1.80                      # Tráfico urbano y bancarización digital
        if promo_base in ['2x1', '2X1', 'Temporada']: score_dig += 1.40     # Ansiedad por apartar la oferta (FOMO)
        if familia in ['Abarrotes', 'Bebidas']: score_dig += 1.10          # Productos pesados (conveniencia de delivery)
        if ventas > 130: score_dig += 0.90                                 # Compras de gran volumen familiar
        if tienda in ['Diriamba', 'Masatepe']: score_dig -= 1.20           # Hábito arraigado de compra presencial
        preferencia_digital = 1 if random.random() < sigmoid(score_dig) else 0

        # Alta Rotación (KPI 9): Comercial (~24% base)
        ratio_rii = ventas / max(inv_inicial, 1)

        score_rot = -2.80
        if ratio_rii >= 0.75: score_rot += 3.20      # Rotación masiva real
        elif ratio_rii >= 0.50: score_rot += 1.50    # Rotación media
        if promo_base in ['2x1', '2X1', 'Temporada']: score_rot += 1.40
        if clasificacion_abc == 'A': score_rot += 1.20
        if canal in ['Web', 'Mayorista']: score_rot += 0.80
        
        alta_rotacion = 1 if random.random() < sigmoid(score_rot) else 0

        # =================================================================
        # AUDITORÍA Y CALIDAD DE DATOS (Data Steward)
        # =================================================================
        canal_final = canal if random.random() > 0.03 else None
        quiebre_final = quiebre_real if random.random() > 0.02 else None

        if random.random() < 0.04 and promo_base == '2x1': promocion = '2X1'
        elif random.random() < 0.04 and promo_base == 'Combo': promocion = 'COMBO'
        elif random.random() < 0.04 and promo_base == 'Descuento': promocion = 'DESCUENTO'
        else: promocion = promo_base

        if random.random() < 0.03:
            ventas_final = random.choice([-15, 290, 450])
        else:
            ventas_final = ventas

        data.append({
            'id_producto_tienda_semana': f"REG-{i:06d}",
            'inicio_semana': inicio_sem.strftime('%Y-%m-%d'),
            'tienda': tienda,
            'canal_venta': canal_final,
            'familia_producto': familia,
            'tipo_promocion': promocion,
            'ventas_unidades': ventas_final,
            'dias_cobertura': dias_cobertura,
            'inventario_inicial': inv_inicial,
            'dias_retraso_proveedor': dias_retraso,
            'clasificacion_abc': clasificacion_abc,
            'sistema_origen': sistema_origen,
            'quiebre_stock': quiebre_final,
            'target_retraso_critico': retraso_critico,
            'target_preferencia_digital': preferencia_digital,
            'target_alta_rotacion': alta_rotacion
        })

    return pd.DataFrame(data)