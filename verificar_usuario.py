import mysql.connector

def create_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root", 
        password="", 
        database="plataforma"  
    )

try:
    conn = create_connection()
    cursor = conn.cursor()

    # Consulta para verificar un usuario
    cursor.execute("SELECT * FROM usuario LIMIT 1;")
    usuario = cursor.fetchone()

    print("Datos de un usuario:")
    print(usuario)

except Exception as e:
    print(f"Error al consultar la base de datos: {e}")
finally:
    if conn.is_connected():
        cursor.close()
        conn.close()
        print("Conexión cerrada.")
