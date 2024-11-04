import mysql.connector

# Establecer la conexión a la base de datos
connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password="",
    database="plataforma"
)

try:
    cursor = connection.cursor(dictionary=True)
    
    # Ejecutar la consulta de inserción
    cursor.execute(
        'INSERT INTO usuarios (nombre, apellido, correo, rol, fecha_creacion, ultima_actualizacion) VALUES (%s, %s, %s, %s, NOW(), NOW())',
        (nombre, apellido, correo, rol)
    )
    
    # Confirmar los cambios
    connection.commit()

except mysql.connector.Error as err:
    print(f"Error: {err}")
finally:
    # Cerrar el cursor y la conexión
    cursor.close()
    connection.close()
