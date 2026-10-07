from etl.extract import generar_datos_crudos
from etl.transform import aplicar_gobierno
from etl.features import construir_features
from etl.load import cargar_a_bd

def ejecutar_pipeline():
    print("="*50)
    print("🚀 INICIANDO PIPELINE - MERCADOS LA COLINA S.A.")
    print("="*50)
    
    # 1. Extraer
    df_crudo = generar_datos_crudos(15000)
    
    # 2. Transformar (Gobierno)
    df_limpio, df_rechazos = aplicar_gobierno(df_crudo)
    
    # 3. Feature Engineering
    df_features = construir_features(df_limpio)
    
    # 4. Cargar
    cargar_a_bd(df_features, df_rechazos)
    
    print("="*50)
    print("🎉 PIPELINE FINALIZADO. DATOS LISTOS PARA MINERÍA.")
    print("="*50)

if __name__ == "__main__":
    ejecutar_pipeline()