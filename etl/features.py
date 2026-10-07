import pandas as pd

def construir_features(df_limpio):
    print("[FEATURES] Calculando KPIs Predictivos (Feature Engineering)...")
    df = df_limpio.copy()
    
    # Ordenar para el KPI 10 (LAG)
    df = df.sort_values(by=['tienda', 'familia_producto', 'inicio_semana'])
    
    # KPI #6: TRCP (Retraso Crítico > 4 días)
    df['kpi6_retraso_critico'] = (df['dias_retraso_proveedor'] > 4).astype(int)
    
    # KPI #7: ITC (Tensión de Cobertura <= 5 días)
    df['kpi7_tension_cobertura'] = (df['dias_cobertura'] <= 5).astype(int)
    
    # KPI #8: TCD (Concentración Digital)
    df['kpi8_es_digital'] = df['canal_venta'].isin(['Web', 'WhatsApp']).astype(int)
    
    # KPI #9: IRP (Rotación Prioritaria Clase A)
    df['kpi9_prioridad_A'] = (df['clasificacion_abc'] == 'A').astype(int)
    
    # KPI #10: IQC (Quiebre en Cascada t-1)
    df['kpi10_quiebre_t_menos_1'] = df.groupby(['tienda', 'familia_producto'])['quiebre_stock'].shift(1)
    df['kpi10_quiebre_t_menos_1'] = df['kpi10_quiebre_t_menos_1'].fillna(0).astype(int)
    
    return df