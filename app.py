from flask import Flask, request, render_template, redirect, url_for, session, flash
import mysql.connector
from werkzeug.security import check_password_hash
import os
import datetime
import sqlite3

app = Flask(__name__)

# Usar una clave secreta segura para la sesión
app.secret_key = os.urandom(24)  # Clave secreta aleatoria y segura

# Configuración de la cookie de sesión
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SECURE'] = False  # Cambiar a True si usas HTTPS

# Conexión a la base de datos 
def create_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root", 
        password="",  
        database="plataforma"  
    )

def close_connection(conn):
    if conn.is_connected():
        conn.close()



# Página principal
@app.route("/")
def inicio():
    return render_template("home.html")

# Ruta para el formulario de registro
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash
from db_connection import create_connection, close_connection

@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        # Capturando datos del formulario
        nombre = request.form.get("nombre")
        correo = request.form.get("correo")
        contrasena = request.form.get("contrasena")
        contrasena_hash = generate_password_hash(contrasena)  # Hasheo de la contraseña

        # Verificando que los datos no estén vacíos
        if not nombre or not correo or not contrasena:
            flash("Todos los campos son obligatorios")
            return redirect(url_for("registro"))

        try:
            # Estableciendo conexión con la base de datos
            conn = create_connection()
            if not conn:
                raise Exception("No se pudo conectar a la base de datos")

            cursor = conn.cursor()

            # Insertando datos en la tabla 'usuario'
            cursor.execute("""
                INSERT INTO usuario (Nombre, Correo, Contraseña, ID_Direccion)
                VALUES (%s, %s, %s, NULL)
            """, (nombre, correo, contrasena_hash))

            # Confirmando los cambios
            conn.commit()
            usuario_id = cursor.lastrowid  # Obtener el ID del usuario recién insertado

            # Creando la sesión para el usuario
            session["usuario"] = nombre
            session["usuario_id"] = usuario_id

            # Redirigiendo al panel de usuario
            flash("Registro exitoso. Bienvenido al panel de usuario.")
            return redirect(url_for("panelUser"))  # Redirige al panel de usuario

        except Exception as e:
            # Mostrando un mensaje de error en caso de fallo
            flash("Error al registrar el usuario: " + str(e))
            return redirect(url_for("registro"))  # Redirige a la página de registro en caso de error

        finally:
            # Cerrando la conexión a la base de datos
            close_connection(conn)

    # Renderizando la plantilla de registro si el método es GET
    return render_template("logup.html")



# Ruta para la página de inicio de sesión
@app.route("/login", methods=["GET", "POST"])
def login():
    if "usuario_id" in session:  # Verifica si el usuario ya está logueado
        return redirect(url_for("panel_usuario"))  # Redirige al panel de usuario

    error = None
    if request.method == "POST":
        # Obteniendo los datos del formulario
        usuario = request.form["correo"]
        contrasena = request.form["contrasena"]

        conn = create_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM usuario WHERE correo = %s", (usuario,))
            user = cursor.fetchone()

            if user:
                # Verificando la contraseña
                if check_password_hash(user[3], contrasena):
                    session["usuario"] = user[1]  # Guarda el nombre del usuario
                    session["usuario_id"] = user[0]  # Guarda el ID del usuario
                    return redirect(url_for("panel_usuario"))  # Redirige al panel de usuario
                else:
                    error = "Contraseña incorrecta"
            else:
                error = "Usuario no encontrado"
        except Exception as e:
            error = f"Error al iniciar sesión: {e}"
        finally:
            close_connection(conn)

    return render_template("login.html", error=error)


@app.route("/panelUser")
def panel_usuario():
    if "usuario_id" not in session:  # Verifica si el usuario está logueado
        flash("Debes iniciar sesión para acceder al panel de usuario.", "warning")
        return redirect(url_for("login"))  # Redirige al login

    usuario_id = session.get("usuario_id")
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT Nombre, Correo FROM usuario WHERE ID_Usuario = %s", (usuario_id,))
        usuario = cursor.fetchone()
        if usuario:
            flash("Bienvenido a tu panel de usuario.", "success")
            return render_template("panelUser.html", usuario=usuario)
        else:
            flash("Usuario no encontrado.", "danger")
            return redirect(url_for("login"))
    except Exception as e:
        flash(f"Error al obtener datos del usuario: {e}", "danger")
        return redirect(url_for("login"))
    finally:
        close_connection(conn)

    
# Ruta para la página de edición
# Ruta para la página de edición
@app.route("/editar_usuario", methods=["GET", "POST"])
def editar_usuario():
    if "usuario_id" not in session:  # Verifica si el usuario está logueado
        flash("Debes iniciar sesión para acceder a esta página.", "warning")
        return redirect(url_for("login"))  # Redirige al login

    usuario_id = session.get("usuario_id")
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        if request.method == "POST":
            # Realiza las actualizaciones de datos
            nuevo_nombre = request.form["nombre"]
            nuevo_correo = request.form["correo"]

            cursor.execute(
                "UPDATE usuario SET Nombre = %s, Correo = %s WHERE ID_Usuario = %s",
                (nuevo_nombre, nuevo_correo, usuario_id)
            )
            conn.commit()
            flash("Datos actualizados correctamente.", "success")
            return redirect(url_for("panel_usuario"))  # Redirige al panel de usuario
        else:
            # Si es GET, muestra los datos del usuario para editar
            cursor.execute("SELECT Nombre, Correo FROM usuario WHERE ID_Usuario = %s", (usuario_id,))
            usuario = cursor.fetchone()
            return render_template("editar_usuario.html", usuario=usuario)
    except Exception as e:
        flash(f"Error al editar usuario: {e}", "danger")
        return redirect(url_for("panel_usuario"))
    finally:
        close_connection(conn)
  # Cerrar la conexión después de completar la tarea

# Ruta para guardar los cambios del usuario
@app.route('/guardar_cambios_usuario', methods=['POST'])
def guardar_cambios_usuario():
    if "usuario_id" in session:
        usuario_id = session.get("usuario_id")
        nombre = request.form.get('nombre')
        correo = request.form.get('correo')
        contrasena = request.form.get('contrasena')

        # Validaciones básicas
        if not nombre or not correo:
            flash("Por favor, completa todos los campos requeridos.", "warning")
            return redirect(url_for('editar_usuario'))

        conn = create_connection()
        cursor = conn.cursor()
        try:
            if contrasena:
                contrasena_hash = generate_password_hash(contrasena)
                cursor.execute("""
                    UPDATE usuario 
                    SET Nombre = %s, Correo = %s, Contraseña = %s 
                    WHERE ID_Usuario = %s
                """, (nombre, correo, contrasena_hash, usuario_id))
            else:
                cursor.execute("""
                    UPDATE usuario 
                    SET Nombre = %s, Correo = %s 
                    WHERE ID_Usuario = %s
                """, (nombre, correo, usuario_id))
            conn.commit()
            flash("Información actualizada correctamente.", "success")
            return redirect(url_for('panel_usuario'))
        except Exception as e:
            conn.rollback()
            flash(f"Error al actualizar la información: {e}", "danger")
            return redirect(url_for('editar_usuario'))
        finally:
            close_connection(conn)
    else:
        flash("Debes iniciar sesión primero.", "warning")
        return redirect(url_for("login"))




# Ruta para cerrar sesión
@app.route("/logout")
def logout():
    session.pop("usuario", None)
    session.pop("usuario_id", None)
    return redirect(url_for("login"))

# Ruta para mostrar productos
@app.route('/productos', methods=['GET', 'POST'])
def productos():
    if request.method == 'POST':
        id_producto = request.form['id_producto']
        cantidad = request.form['cantidad']

        # Verificar que la cantidad sea mayor que cero
        if int(cantidad) <= 0:
            return "La cantidad debe ser mayor que cero.", 400

        # Aquí se agrega la lógica de la base de datos (como en el código original)
        # Puedes agregar el código que maneja el pedido del producto

        # Finalmente, redirige a la página de ver el pedido
        return redirect(url_for('ver_pedido'))

    return render_template('productos_diconsa.html')

# Ruta para enviar reclamos
@app.route("/enviar_reclamo", methods=["POST"])
def enviar_reclamo():
    try:
        conn = create_connection()  # Conexión a la base de datos
        cursor = conn.cursor()

        # Obtener datos del formulario
        usuario_id = session.get("usuario_id")  # Obteniendo el ID del usuario de la sesión
        producto_id = request.form["producto_seleccionado"]
        descripcion = request.form["mensaje"]

        # Insertar la queja en la base de datos
        cursor.execute("""
            INSERT INTO reclamo (usuario_id, producto_id, descripcion, fecha)
            VALUES (%s, %s, %s, NOW())
        """, (usuario_id, producto_id, descripcion))
        conn.commit()

        # Confirmación
        flash("Tu reclamo se ha enviado correctamente :)")
        return redirect(url_for("quejas"))

    except Exception as e:
        flash(f"Error al enviar el reclamo: {e}")
        return redirect(url_for("quejas"))

    finally:
        close_connection(conn)

# Ruta para quejas
@app.route("/quejas", methods=["GET", "POST"])
def quejas():
    try:
        conn = create_connection()  # Conexión a la base de datos
        cursor = conn.cursor(dictionary=True)
        
        # Obtener las categorías desde la base de datos
        cursor.execute("SELECT ID_Categoria, Nombre FROM categoria")
        categorias = cursor.fetchall()

        return render_template("quejas.html", categorias=categorias)

    except Exception as e:
        flash(f"Error al cargar las categorías: {e}")
        return render_template("quejas.html", categorias=[])
    
    finally:
        close_connection(conn)

# Ruta para redes sociales
@app.route("/redessociales")
def redessociales():
    return render_template("redessociales.html")

# Ruta para sección de contacto
@app.route("/seccion_de_contacto")
def seccion_de_contacto():
    return render_template("seccion_de_contacto.html")

# Ruta para horarios
@app.route("/horarios")
def horarios():
    return render_template("horarios.html")
  # Ruta para informacion legal
@app.route("/informacionlegal")
def informacionlegal():
    return render_template("informacionlegal.html")

# Ruta para los productos dentro del panel del encargado de la Tienda Comunitaria
@app.route("/ProductosDiconsa")
def productos_diconsa():
    return render_template("ProductosDiconsa.html")

@app.route("/ver_pedido", methods=["GET"])
def ver_pedido():
    if "usuario_id" not in session:
        flash("Debes iniciar sesión para ver tu pedido.", "warning")
        return redirect(url_for("login"))

    usuario_id = session.get("usuario_id")
    conn = create_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT p.ID_Pedido, p.Estado
            FROM Pedido p
            WHERE p.ID_Usuario = %s
        """, (usuario_id,))
        pedido = cursor.fetchone()

        if pedido:
            cursor.execute("""
                SELECT pr.Nombre, pr.Cantidad
                FROM Producto pr
                JOIN Pedido_Producto pp ON pr.ID_Producto = pp.ID_Producto
                WHERE pp.ID_Pedido = %s
            """, (pedido['ID_Pedido'],))
            productos = cursor.fetchall()
        else:
            productos = []

        return render_template("ver_pedido.html", pedido=pedido, productos=productos)

    except Exception as e:
        flash(f"Error al obtener el pedido: {e}", "danger")
        return redirect(url_for("productos"))
    finally:
        close_connection(conn)





@app.route("/confirmar_pedido", methods=["POST"])
def confirmar_pedido():
    if "usuario_id" not in session:
        flash("Debes iniciar sesión para confirmar el pedido.", "warning")
        return redirect(url_for("login"))

    usuario_id = session.get("usuario_id")
    conn = create_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT ID_Pedido
            FROM Pedido
            WHERE ID_Usuario = %s AND Estado = 'pendiente'
        """, (usuario_id,))
        pedido = cursor.fetchone()

        if pedido:
            cursor.execute("""
                UPDATE Pedido
                SET Estado = 'confirmado'
                WHERE ID_Pedido = %s
            """, (pedido['ID_Pedido'],))
            conn.commit()

            flash("Tu pedido ha sido confirmado.", "success")
            return redirect(url_for("ver_pedido"))
        else:
            flash("No tienes un pedido pendiente para confirmar.", "warning")
            return redirect(url_for("productos"))
    except Exception as e:
        flash(f"Error al confirmar el pedido: {e}", "danger")
        return redirect(url_for("productos"))
    finally:
        close_connection(conn)


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
    