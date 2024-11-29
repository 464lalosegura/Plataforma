from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from db_connection import create_connection, close_connection

app = Flask(__name__)
app.secret_key = 'supersecretkey'
print(f"Clave secreta configurada: {app.secret_key}")

# Página principal
@app.route("/")
def inicio():
    return render_template("home.html")

# Ruta para el formulario de registro
@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        nombre = request.form["nombre"]
        correo = request.form["correo"]
        contrasena = request.form["contrasena"]
        contrasena_hash = generate_password_hash(contrasena)

        try:
            conn = create_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM usuario")
            usuarios = cursor.fetchall()
            print("Usuarios en la base de datos:")
            for usuario in usuarios:
                print(usuario) 
            cursor.execute("""
                INSERT INTO usuario (nombre, correo, contraseña) 
                VALUES (%s, %s, %s)
            """, (nombre, correo, contrasena_hash))
            conn.commit()
            session["usuario"] = nombre
            session["usuario_id"] = cursor.lastrowid
            print(f"Usuario: {session.get('usuario')}, Usuario ID: {session.get('usuario_id')}")
            flash("Registro exitoso. Bienvenido al panel de usuario.")
            return redirect(url_for("panel_usuario"))
        except Exception as e:
            flash("Error al registrar el usuario: " + str(e))
            return redirect(url_for("registro"))
        finally:
            close_connection(conn)
    return render_template("logup.html")

# Ruta para la página de inicio de sesión
@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        usuario = request.form["correo"]
        contrasena = request.form["contrasena"]

        conn = create_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM usuario WHERE correo = %s", (usuario,))
            user = cursor.fetchone()

            if user and check_password_hash(user[3], contrasena):
                session["usuario"] = user[1]  
                session["usuario_id"] = user[0]  
                return redirect(url_for("panel_usuario"))
            else:
                error = "Usuario o contraseña incorrectos"
        except Exception as e:
            error = f"Error al iniciar sesión: {e}"
        finally:
            close_connection(conn)
    
    return render_template("login.html", error=error)
    
# Ruta para el panel de usuario
@app.route("/panelUser")
def panel_usuario():
    if "usuario" in session:
        print(f"Bienvenido al panel de usuario: {session.get('usuario')}, ID de usuario: {session.get('usuario_id')}")
        return render_template("panelUser.html", usuario=session["usuario"])
    return redirect(url_for("registro"))





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
        usuario_id = request.form["usuario_id"]
        categoria_id = request.form["categoria_id"]
        mensaje = request.form["mensaje"]

        # Insertar la queja en la base de datos
        cursor.execute("""
            INSERT INTO reclamos (ID_Usuario, ID_Categoria, Mensaje, Fecha)
            VALUES (%s, %s, %s, NOW())
        """, (usuario_id, categoria_id, mensaje))
        conn.commit()

        flash("Tu queja, opinión o sugerencia fue enviada exitosamente.")
        return redirect(url_for("quejas"))

    except Exception as e:
        flash(f"Error al enviar la queja: {e}")
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



if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
