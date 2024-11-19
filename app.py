from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from db_connection import create_connection, close_connection

app = Flask(__name__)
app.secret_key = 'supersecretkey'

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
            cursor.execute("""
                INSERT INTO usuario (nombre, correo, contraseña) 
                VALUES (%s, %s, %s)
            """, (nombre, correo, contrasena_hash))
            conn.commit()
            session["usuario"] = nombre
            session["usuario_id"] = cursor.lastrowid
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
        usuario = request.form["usuario"]
        contrasena = request.form["contrasena"]

        conn = create_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM usuario WHERE correo = %s", (usuario,))
            user = cursor.fetchone()

            if user and check_password_hash(user[2], contrasena):
                session["usuario"] = usuario
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
@app.route("/panel_usuario")
def panel_usuario():
    if "usuario" in session:
        return render_template("panelUser.html", usuario=session["usuario"])
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
@app.route('/enviar_reclamo', methods=['POST'])
def enviar_reclamo():
    usuario_id = session.get("usuario_id")
    if not usuario_id:
        return redirect(url_for("login"))

    producto_id = request.form["producto_id"]
    categoria = request.form["categoria"]
    mensaje = request.form["mensaje"]
    
    try:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO reclamo (usuario_id, producto_id, categoria, mensaje)
            VALUES (%s, %s, %s, %s)
        """, (usuario_id, producto_id, categoria, mensaje))
        conn.commit()
    except Exception as e:
        flash("Error al enviar el reclamo: " + str(e))
        return redirect(url_for("panel_usuario"))
    finally:
        close_connection(conn)
    
    flash("Tu reclamo fue enviado con éxito.")
    return redirect(url_for("panel_usuario"))

# Ruta para quejas
@app.route('/quejas')
def quejas():
    return render_template('quejas.html')

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
    # Aquí podrías capturar datos del formulario si es necesario
    return render_template("pedido.html")



if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
