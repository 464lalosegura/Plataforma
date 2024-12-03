from db_connection import create_connection

conn = create_connection()
if conn:
    print("Conexión exitosa a la base de datos")
    conn.close()
else:
    print("Error al conectar a la base de datos")
