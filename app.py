from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from db_connection import create_connection, close_connection
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify

app = Flask(__name__)
app.secret_key = 'supersecretkey'
print(f"Clave secreta configurada: {app.secret_key}")

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
    error = None
    if request.method == "POST":
        # Obteniendo los datos del formulario
        usuario = request.form["correo"]
        contrasena = request.form["contrasena"]

        conn = create_connection()
        try:
            cursor = conn.cursor()
            # Verificando si el usuario existe en la base de datos
            cursor.execute("SELECT * FROM usuario WHERE correo = %s", (usuario,))
            user = cursor.fetchone()  # Obtiene un registro de usuario

            # Verificando si la contraseña es correcta
            if user:
                print(f"Usuario encontrado: {user}")  # Verifica si el usuario existe
                if check_password_hash(user[3], contrasena):  # Compara la contraseña con el hash
                    print("Contraseña válida")
                    session["usuario"] = user[1]  # Guarda el nombre del usuario en la sesión
                    session["usuario_id"] = user[0]  # Guarda el ID del usuario en la sesión
                    return redirect(url_for("panel_usuario"))  # Redirige al panel de usuario
                else:
                    error = "Contraseña incorrecta"  # Error en caso de que la contraseña sea incorrecta
            else:
                error = "Usuario no encontrado"  # Si no existe el usuario en la base de datos

        except Exception as e:
            error = f"Error al iniciar sesión: {e}"  # Si ocurre un error al consultar la base de datos
        finally:
            close_connection(conn)  # Cerrar la conexión con la base de datos
    
    # Renderiza el formulario de inicio de sesión con el posible error
    return render_template("login.html", error=error)

    
# Ruta para el panel de usuario
@app.route("/panelUser")
def panel_usuario():
    if "usuario_id" in session:  # Verifica si el usuario está logueado
        usuario_id = session.get("usuario_id")
        conn = create_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            # Obtiene los datos del usuario desde la base de datos
            cursor.execute("SELECT Nombre, Correo FROM usuario WHERE id_usuario = %s", (usuario_id,))
            usuario = cursor.fetchone()  # Obtiene un único registro de usuario
            if usuario:
                return render_template("panelUser.html", usuario=usuario)  # Muestra el panel del usuario
            else:
                flash("Usuario no encontrado.", "danger")  # Si no se encuentra el usuario
                return redirect(url_for("login"))  # Redirige a la página de login
        except Exception as e:
            flash(f"Error al obtener datos del usuario: {e}", "danger")
            return redirect(url_for("login"))
        finally:
            close_connection(conn)  # Cierra la conexión con la base de datos
    else:
        return redirect(url_for("login"))  # Si no está logueado, redirige al login


# Ruta para la página de edición
@app.route("/editar_usuario", methods=["GET", "POST"])
def editar_usuario():
    if "usuario_id" in session:  # Verifica si el usuario está logueado
        usuario_id = session["usuario_id"]

        conn = create_connection()
        cursor = conn.cursor(dictionary=True)

        try:
            # Obtiene los datos del usuario desde la base de datos
            cursor.execute("SELECT Nombre, Correo FROM usuario WHERE ID_Usuario = %s", (usuario_id,))
            usuario = cursor.fetchone()
            if request.method == "POST":
                # Si se envían datos para actualizar
                nombre = request.form["nombre"]
                correo = request.form["correo"]

                # Actualiza los datos del usuario en la base de datos
                cursor.execute("""
                    UPDATE usuario 
                    SET Nombre = %s, Correo = %s
                    WHERE ID_Usuario = %s
                """, (nombre, correo, usuario_id))
                conn.commit()  # Guarda los cambios en la base de datos
                flash("Información actualizada correctamente", "success")
                return redirect(url_for("panel_usuario"))  # Redirige al panel de usuario

            if usuario:
                return render_template("editar_usuario.html", usuario=usuario)  # Muestra el formulario de edición
            else:
                flash("Usuario no encontrado", "danger")
                return redirect(url_for("login"))  # Si no se encuentra el usuario, redirige al login

        except Exception as e:
            flash(f"Error: {e}", "danger")
            return redirect(url_for("login"))
        finally:
            close_connection(conn)
    else:
        return redirect(url_for("login"))  # Si no está logueado, redirige al login





# Ruta para guardar los cambios del usuario
@app.route('/guardar_cambios_usuario', methods=['POST'])
def guardar_cambios_usuario():
    if "usuario_id" in session:
        usuario_id = session.get("usuario_id")
        nombre = request.form.get('nombre')
        correo = request.form.get('correo')
        contrasena = request.form.get('contrasena')
        tienda = request.form.get('tienda')

        # Validaciones básicas
        if not nombre or not correo or not tienda:
            flash("Por favor, completa todos los campos requeridos.", "warning")
            return redirect(url_for('editar_usuario'))

        conn = create_connection()
        cursor = conn.cursor()
        try:
            if contrasena:
                contrasena_hash = generate_password_hash(contrasena)
                cursor.execute("""
                    UPDATE usuario 
                    SET Nombre = %s, Correo = %s, Contraseña = %s, Tienda = %s 
                    WHERE id_usuario = %s
                """, (nombre, correo, contrasena_hash, tienda, usuario_id))
            else:
                cursor.execute("""
                    UPDATE usuario 
                    SET Nombre = %s, Correo = %s, Tienda = %s 
                    WHERE id_usuario = %s
                """, (nombre, correo, tienda, usuario_id))
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
@app.route('/productos')
def productos():
    return render_template('Productos.html')

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

@app.route("/pedido", methods=["POST"])
def ver_pedido():
    
    return render_template("pedido.html")

#Ruta  para agregar la categoria con los productos
# Este código se encarga de obtener los productos por categoría
@app.route("/productos_por_categoria", methods=["GET"])
def productos_por_categoria():
    categoria_id = request.args.get("categoria_id")
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM producto WHERE ID_Categoria = %s", (categoria_id,))
    productos = cursor.fetchall()
    conn.close()
    return jsonify({"productos": productos})

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)