from sqlalchemy import create_engine, text

def test_connection():
    conexion_str = 'postgresql://rasm:rambito12@localhost:5432/la_colina_sa'
    
    print("="*50)
    print("󰑓 Trying to connect to PostgreSQL...")
    print("="*50)
    
    try:
        # Crear el motor de conexión
        engine = create_engine(conexion_str)
        
        # Intentar abrir la conexión
        with engine.connect() as conn:
            # Ejecutar un query básico para probar
            resultado = conn.execute(text("SELECT version();")).fetchone()
            
            print("󰸞 SUCCESS!")
            print(f" Database response: {resultado[0]}")
            
    except Exception as e:
        print(" ERROR DE CONEXIÓN.")
        print("Por favor, verifica lo siguiente:")
        print("  1. ¿PostgreSQL está encendido (servicio corriendo)?")
        print("  2. ¿El usuario 'postgres' y la contraseña 'rambito12' son correctos?")
        print("  3. ¿Creaste la base de datos llamada 'LaColinaSA' en pgAdmin/DBeaver?")
        print("\nDetalle técnico del error:")
        print(e)
    print("="*50)

if __name__ == "__main__":
    test_connection()