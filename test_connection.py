from sqlalchemy import create_engine, text

def test_connection():
    conexion_str = 'postgresql://rasm:rambito12@localhost:5432/la_colina_sa'
    
    print("="*50)
    print("Trying to connect to PostgreSQL...")
    print("="*50)
    
    try:
        # Crear el motor de conexión
        engine = create_engine(conexion_str)
        
        # Intentar abrir la conexión
        with engine.connect() as conn:
            # Ejecutar un query básico para probar
            resultado = conn.execute(text("SELECT version();")).fetchone()
            
            print("SUCCESS!")
            print(f" Database response: {resultado[0]}")
            
    except Exception as e:
        print("CONNECTION FAILED.")
        print("Please check the following:")
        print("  1. Is PostgreSQL running (service running)?")
        print("  2. Are the user and the password correct?")
        print("  3. Did you create the database called like in 'conexion_str' in pgAdmin/DBeaver?")
        print("\nTechnical details of the error:")
        print(e)
    print("="*50)

if __name__ == "__main__":
    test_connection()