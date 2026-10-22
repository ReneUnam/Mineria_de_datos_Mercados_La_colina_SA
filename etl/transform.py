import pandas as pd

def calcular_kpis_calidad(df):
    """Calcula los 3 KPIs de Calidad programados."""
    total = len(df)
    if total == 0: return 100.0, 100.0, 100.0
    
    # KPI 1: TCR (Completitud)
    completos = len(df.dropna(subset=['canal_venta', 'quiebre_stock']))
    tcr = (completos / total) * 100

    # KPI 2: TED (Estandarización)
    promos_validas = ['Sin promoción', '2x1', 'Descuento', 'Combo', 'Temporada']
    estandarizados = len(df[df['tipo_promocion'].isin(promos_validas)])
    ted = (estandarizados / total) * 100

    # KPI 3: TDR (Rango)
    en_rango = len(df[(df['ventas_unidades'] >= 5) & (df['ventas_unidades'] <= 240)])
    tdr = (en_rango / total) * 100

    return tcr, ted, tdr

def aplicar_gobierno_y_calidad(df_crudo):
    df = df_crudo.copy()
    bitacora = [] # Aquí guardaremos las incidencias
    
    # 1. IDENTIFICAR INCIDENCIAS (Antes de transformar)
    nulos_target = df['quiebre_stock'].isnull().sum()
    fuera_rango = len(df[(df['ventas_unidades'] < 5) | (df['ventas_unidades'] > 240)])
    ruido_promo = len(df[df['tipo_promocion'].isin(['2X1', 'DESCUENTO', 'COMBO'])])
    
    # 2. REGISTRAR EN BITÁCORA 
    if nulos_target > 0:
        bitacora.append({'Incidencia': f'{nulos_target} registros con Target Nulo', 'Causa': 'Falta de consolidación POS/WMS', 'Tratamiento': 'Descarte (Aislamiento)', 'Responsable': 'Custodio TI'})
    if fuera_rango > 0:
        bitacora.append({'Incidencia': f'{fuera_rango} registros con Ventas fuera de rango', 'Causa': 'Error de digitación en sucursal', 'Tratamiento': 'Descarte (Aislamiento)', 'Responsable': 'Data Steward'})
    if ruido_promo > 0:
        bitacora.append({'Incidencia': f'{ruido_promo} registros con ruido tipográfico', 'Causa': 'Falta de validación en E-commerce', 'Tratamiento': 'Homologación (A+B=C)', 'Responsable': 'Data Steward'})

    df_bitacora = pd.DataFrame(bitacora)

    # 3. APLICAR ACCIÓN CORRECTIVA (Versión Derivada)
    # Homologación (Lo que se salva)
    mapeo_promo = {'2X1': '2x1', 'DESCUENTO': 'Descuento', 'COMBO': 'Combo'}
    df['tipo_promocion'] = df['tipo_promocion'].replace(mapeo_promo)
    df['canal_venta'] = df['canal_venta'].fillna('Tienda')

    # Descarte (Lo que no se salva)
    mascara_validos = (df['quiebre_stock'].notnull() & (df['ventas_unidades'] >= 5) & (df['ventas_unidades'] <= 240))
    df_limpio = df[mascara_validos].copy()
    df_rechazos = df[~mascara_validos].copy()

    df_limpio['quiebre_stock'] = df_limpio['quiebre_stock'].astype(int)
    
    return df_limpio, df_rechazos, df_bitacora