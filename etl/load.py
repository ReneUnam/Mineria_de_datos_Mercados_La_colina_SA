import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()

def cargar_a_bd(df_analitico, df_rechazos):
    print("[LOAD] Cargando datos a PostgreSQL...")
    
    # Leer credenciales del archivo .env
    user = os.getenv('DB_USER', 'postgres')
    password = os.getenv('DB_PASSWORD', 'rambito12')
    host = os.getenv('DB_HOST', 'localhost')
    port = os.getenv('DB_PORT', '5432')
    db = os.getenv('DB_NAME', 'LaColinaSA')
    
    conexion = f'postgresql://{user}:{password}@{host}:{port}/{db}'
    
    try:
        engine = create_engine(conexion)
        
        # Dataset 1: Para Modelos Predictivos (Árboles, XGBoost, etc.)
        df_analitico.to_sql('dw_inventario_predictivo', engine, if_exists='replace', index=False)
        
        # Dataset 2: Para Reglas de Asociación (Apriori) - Solo columnas necesarias
        df_apriori = df_analitico[['id_producto_tienda_semana', 'tienda', 'familia_producto', 'tipo_promocion', 'quiebre_stock']]
        df_apriori.to_sql('dw_promociones_apriori', engine, if_exists='replace', index=False)
        
        # Tabla de Auditoría (Gobierno de Datos)
        df_rechazos.to_sql('staging_rechazos_calidad', engine, if_exists='replace', index=False)
        
        print("Carga exitosa en PostgreSQL.")
        print("POL-SEG-01: Recuerda configurar RBAC en PostgreSQL para la columna 'dias_retraso_proveedor'.")
        
    except Exception as e:
        print(f"❌ Error de conexión a BD: {e}")
        print("Guardando en CSV local como respaldo...")
        df_analitico.to_csv('dw_inventario_predictivo.csv', index=False)