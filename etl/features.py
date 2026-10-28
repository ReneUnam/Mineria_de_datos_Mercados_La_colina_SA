import pandas as pd

def construir_features(df_limpio):
    print("⚙️ [FEATURES] Construyendo Tablón Analítico para los 4 Modelos...")
    df = df_limpio.copy()

    # Fechas y ordenamiento temporal estricto
    df['inicio_semana'] = pd.to_datetime(df['inicio_semana'])
    df = df.sort_values(by=['tienda', 'familia_producto', 'inicio_semana']).reset_index(drop=True)

    # 1. Variables Generales existentes
    df['feature_es_digital'] = df['canal_venta'].isin(['Web', 'WhatsApp']).astype(int)
    df['feature_es_clase_A'] = (df['clasificacion_abc'] == 'A').astype(int)
    df['es_cadena_frio'] = df['familia_producto'].isin(['Lácteos', 'Congelados']).astype(int)

    # 2. Factor Logístico: Ruta foránea hacia Carazo vs local Managua
    # Jinotepe, Diriamba, San Marcos y Masatepe sufren mayor fricción de transporte
    df['es_ruta_foranea'] = df['tienda'].isin(['Jinotepe', 'Diriamba', 'San Marcos', 'Masatepe']).astype(int)

    # 3. Factor Comercial: Promociones que saturan la capacidad de carga
    df['es_promocion_alta_demanda'] = df['tipo_promocion'].isin(['2x1', 'Temporada', 'Combo']).astype(int)

    # 4. Indicador de Tensión de Inventario (Burn Rate)
    # Ratio entre lo vendido y lo que había en bodega al abrir la semana
    df['ratio_tension_inventario'] = (df['ventas_unidades'] / (df['inventario_inicial'] + 1)).round(3)

    # 5. Vulnerabilidad Crítica: Cadena de frío + Bajos días de cobertura
    # Si la cobertura es menor a 5 días en refrigerados, el retraso del proveedor es inminente
    df['alerta_frio_critico'] = (
        (df['es_cadena_frio'] == 1) & (df['dias_cobertura'] <= 5)
    ).astype(int)

    # 6. Historial de comportamiento (Lag / Tasa expansiva sin fuga de datos)
    col_grupo = ['tienda', 'familia_producto']
    if 'target_retraso_critico' in df.columns:
        df['hist_tasa_retraso_proveedor'] = (
            df.groupby(col_grupo)['target_retraso_critico']
            .transform(lambda x: x.shift(1).expanding().mean())
            .fillna(df['target_retraso_critico'].mean())
        )

    # 7. Inercia de ventas recientes (Rolling 2 semanas)
    df['lag_ventas_promedio_2sem'] = (
        df.groupby(col_grupo)['ventas_unidades']
        .transform(lambda x: x.shift(1).rolling(2, min_periods=1).mean())
        .fillna(df['ventas_unidades'].median())
    )

    # Cobertura frente al promedio real reciente
    df['ratio_cobertura_stock'] = (
        df['inventario_inicial'] / (df['lag_ventas_promedio_2sem'] + 1)
    ).round(2)

    df = df.sort_values(by=['tienda', 'familia_producto', 'inicio_semana']).reset_index(drop=True)

    # 1. El retraso que tuvo la entrega de la semana inmediatamente anterior (Lag 1)
    df['retraso_semana_anterior'] = (
        df.groupby(['tienda', 'familia_producto'])['dias_retraso_proveedor']
        .shift(1)
        .fillna(0)
    )

    # 2. Promedio móvil de días de retraso de las últimas 3 semanas
    df['promedio_dias_retraso_ultimas_3sem'] = (
        df.groupby(['tienda', 'familia_producto'])['dias_retraso_proveedor']
        .transform(lambda x: x.shift(1).rolling(3, min_periods=1).mean())
        .fillna(df['dias_retraso_proveedor'].median())
    )

    # 3. Tendencia: ¿El retraso viene empeorando semana a semana?
    df['tendencia_empeoramiento_retraso'] = (
        df['retraso_semana_anterior'] - df['promedio_dias_retraso_ultimas_3sem']
    ).round(2)
    

    return df