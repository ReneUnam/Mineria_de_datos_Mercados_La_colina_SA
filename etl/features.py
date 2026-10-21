import pandas as pd

def construir_features(df_limpio):
    print("⚙️ [FEATURES] Construyendo Tablón Analítico para los 4 Modelos...")
    df = df_limpio.copy()
    
    # Convertimos fecha para ordenamiento
    df['inicio_semana'] = pd.to_datetime(df['inicio_semana'])
    df = df.sort_values(by=['tienda', 'familia_producto', 'inicio_semana'])
    
    # Features Predictivos Generales
    df['feature_es_digital'] = df['canal_venta'].isin(['Web', 'WhatsApp']).astype(int)
    df['feature_es_clase_A'] = (df['clasificacion_abc'] == 'A').astype(int)
    
    # Los 4 Targets ya vienen calculados desde la extracción, 
    # aquí solo aseguramos que estén listos para Minería.
    
    return df