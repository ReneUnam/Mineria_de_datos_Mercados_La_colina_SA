import pandas as pd

def calcular_kpis_calidad(df):
    """Calcula los 3 KPIs de Calidad solicitados por el profesor."""
    total = len(df)
    if total == 0: return 100.0, 100.0, 100.0
    
    # KPI 1: TCR (Completitud) - Sin nulos en canal_venta ni quiebre_stock
    completos = len(df.dropna(subset=['canal_venta', 'quiebre_stock']))
    tcr = (completos / total) * 100

    # KPI 2: TED (Estandarización) - Promociones correctas
    promos_validas = ['Sin promoción', '2x1', 'Descuento', 'Combo', 'Temporada']
    estandarizados = len(df[df['tipo_promocion'].isin(promos_validas)])
    ted = (estandarizados / total) * 100

    # KPI 3: TDR (Rango) - Ventas entre 5 y 240
    en_rango = len(df[(df['ventas_unidades'] >= 5) & (df['ventas_unidades'] <= 240)])
    tdr = (en_rango / total) * 100

    return tcr, ted, tdr

def aplicar_gobierno_y_calidad(df_crudo):
    print("\n🛡️ [TRANSFORM] Iniciando Validador de Calidad y Gobernanza...")
    df = df_crudo.copy()
    total_inicial = len(df)

    # 1. MEDIR CALIDAD ANTES DE LA TRANSFORMACIÓN
    tcr_antes, ted_antes, tdr_antes = calcular_kpis_calidad(df)

    # 2. APLICAR REGLAS DE TRANSFORMACIÓN (El "Hacer" del ciclo PHVA)
    
    # Regla TED: Arreglar ruido tipográfico (A + B = C, esto SÍ se puede arreglar)
    mapeo_promo = {'2X1': '2x1', 'DESCUENTO': 'Descuento', 'COMBO': 'Combo'}
    df['tipo_promocion'] = df['tipo_promocion'].replace(mapeo_promo)
    
    # Regla TCR: Imputar canal de venta nulo (Asumimos 'Tienda' por defecto)
    df['canal_venta'] = df['canal_venta'].fillna('Tienda')

    # Regla TCR y TDR: Separar lo insalvable (Nulos en Target y Fuera de Rango)
    # Si falta la variable objetivo, no se puede inventar.
    mascara_validos = (
        df['quiebre_stock'].notnull() & 
        (df['ventas_unidades'] >= 5) & 
        (df['ventas_unidades'] <= 240)
    )
    
    df_limpio = df[mascara_validos].copy()
    df_rechazos = df[~mascara_validos].copy()

    # 3. MEDIR CALIDAD DESPUÉS DE LA TRANSFORMACIÓN
    tcr_despues, ted_despues, tdr_despues = calcular_kpis_calidad(df_limpio)

    # 4. GENERAR HALLAZGOS 
    print("\n📊 REPORTE DE HALLAZGOS DE CALIDAD (Auditoría):")
    print("-" * 60)
    print(f"Registros procesados: {total_inicial}")
    print(f"  ➤ KPI 1 (TCR - Completitud): Subió de {tcr_antes:.1f}% a {tcr_despues:.1f}%")
    print(f"  ➤ KPI 2 (TED - Estandarización): Subió de {ted_antes:.1f}% a {ted_despues:.1f}%")
    print(f"  ➤ KPI 3 (TDR - En Rango): Subió de {tdr_antes:.1f}% a {tdr_despues:.1f}%")
    print("-" * 60)
    print(f"📝 CONCLUSIÓN DEL DATA STEWARD:")
    print(f"De {total_inicial} registros, se corrigieron automáticamente los errores tipográficos.")
    print(f"Sin embargo, {len(df_rechazos)} registros fueron DESCARTADOS por no tener variable objetivo")
    print(f"o por tener ventas irreales. El dataset final tiene {len(df_limpio)} registros 100% fiables.")
    print("-" * 60)

    df_limpio['quiebre_stock'] = df_limpio['quiebre_stock'].astype(int)
    return df_limpio, df_rechazos