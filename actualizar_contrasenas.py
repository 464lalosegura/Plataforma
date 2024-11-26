from werkzeug.security import generate_password_hash
import mysql.connector 

# Configuración de la conexión
conn = mysql.connector.connect(
    host="localhost",  
    user="root", 
    password="", 
    database="plataforma" 
)
cursor = conn.cursor()

# Recuperar todas las contraseñas en texto plano
cursor.execute("SELECT ID_Usuario, contraseña FROM usuario")
usuarios = cursor.fetchall()

for usuario in usuarios:
    user_id, password_plain = usuario
    # Hashear la contraseña en texto plano
    password_hashed = generate_password_hash(password_plain)
    print(f"Actualizando usuario {user_id}: {password_plain} -> {password_hashed}")

    # Actualizar la contraseña en la base de datos
    cursor.execute(
         "UPDATE usuario SET contraseña = %s WHERE ID_Usuario = %s",
    (password_hashed, user_id)
    )

# Guardar cambios y cerrar conexión
conn.commit()
conn.close()
print("Contraseñas actualizadas correctamente.")
