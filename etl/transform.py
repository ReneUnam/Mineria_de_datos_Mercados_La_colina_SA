import pandas as pd

def aplicar_gobierno(df_crudo):
    print("[TRANSFORM] Aplicando Políticas de Gobierno de Datos...")
    df = df_crudo.copy()
    
    # POL-USO-01: Estandarización de catálogo
    mapeo_promo = {'2X1': '2x1', 'DESCUENTO': 'Descuento', 'COMBO': 'Combo', 'SIN PROMOCIÓN': 'Sin promoción'}
    df['tipo_promocion'] = df['tipo_promocion'].replace(mapeo_promo)
    
    # POL-CAL-01: Ventas lógicas (5 a 240)
    df = df[(df['ventas_unidades'] >= 5) & (df['ventas_unidades'] <= 240)]
    
    # POL-TRA-01: Imputación de canal huérfano
    df['canal_venta'] = df['canal_venta'].fillna('Sin Especificar')
    
    # POL-CAL-01: Aislamiento de nulos en variable objetivo
    df_rechazos = df[df['quiebre_stock'].isnull()].copy()
    df_limpio = df[df['quiebre_stock'].notnull()].copy()
    
    df_limpio['quiebre_stock'] = df_limpio['quiebre_stock'].astype(int)
    df_limpio['inicio_semana'] = pd.to_datetime(df_limpio['inicio_semana'])
    
    return df_limpio, df_rechazos