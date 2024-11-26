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

    # Consulta para describir la estructura de la tabla
    cursor.execute("DESCRIBE usuario;")
    columnas = cursor.fetchall()

    print("Columnas de la tabla 'usuario':")
    for idx, columna in enumerate(columnas):
        print(f"{idx}: {columna[0]}")

except Exception as e:
    print(f"Error al conectarse a la base de datos: {e}")
finally:
    if conn.is_connected():
        cursor.close()
        conn.close()
        print("Conexión cerrada.")
