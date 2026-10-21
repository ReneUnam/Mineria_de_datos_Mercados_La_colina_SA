from etl.extract import generar_datos_crudos
from etl.transform import aplicar_gobierno_y_calidad
from etl.features import construir_features
from etl.load import cargar_a_bd # (Usa el mismo load.py que ya teníamos)

def ejecutar_pipeline():
    print("="*60)
    print("🚀 INICIANDO PIPELINE GOBERNADO - MERCADOS LA COLINA S.A.")
    print("="*60)
    
    # 1. Extraer (V0)
    df_crudo = generar_datos_crudos(15000)
    
    # 2. Transformar y Validar Calidad (V1 y Rechazos)
    df_limpio, df_rechazos = aplicar_gobierno_y_calidad(df_crudo)
    
    # 3. Feature Engineering (Tablón Analítico)
    df_features = construir_features(df_limpio)
    
    # 4. Cargar a BD
    cargar_a_bd(df_features, df_rechazos)
    
    print("="*60)
    print("🎉 PIPELINE FINALIZADO. DATOS LISTOS PARA MINERÍA.")
    print("="*60)

if __name__ == "__main__":
    ejecutar_pipeline()