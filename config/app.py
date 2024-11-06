from flask import Flask, render_template, request, redirect, url_for, session, flash
from db_connection import create_connection, close_connection

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Página principal que redirige a "Pagina_de_inicio.html"
@app.route("/")
def inicio():
    return redirect(url_for("pagina_inicio"))

# Ruta para la página de inicio
@app.route("/pagina_inicio")
def pagina_inicio():
    return render_template("Pagina_de_inicio.html")

# Ruta para el registro de usuarios
@app.route("/registro", methods=["POST"])
def registro():
    nombre = request.form["nombre"]
    correo = request.form["correo"]
    contrasena = request.form["contrasena"]
    
    try:
        # Guardar datos en la base de datos
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO usuario (nombre, correo, contraseña) 
            VALUES (%s, %s, %s)
        """, (nombre, correo, contrasena))
        conn.commit()
    except Exception as e:
        flash("Error al registrar el usuario: " + str(e))
        return redirect(url_for("pagina_inicio"))
    finally:
        close_connection(conn)
    
    flash("Registro exitoso. Ahora puede iniciar sesión.")
    return redirect(url_for("login"))

# Ruta para la página de inicio de sesión
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form["usuario"]
        contrasena = request.form["contrasena"]
        
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuario WHERE nombre = %s AND contraseña = %s", (usuario, contrasena))
        user = cursor.fetchone()
        
        if user:
            session["usuario"] = usuario
            session["usuario_id"] = user[0]
            return redirect(url_for("panel_usuario"))
        else:
            error = "Usuario o contraseña incorrectos"
            return render_template("iniciar_sesion.html", error=error)
    
    return render_template("iniciar_sesion.html")

# Ruta para el panel de usuario
@app.route("/panel_usuario")
def panel_usuario():
    if "usuario" in session:
        return render_template("panel_de_usuario.html", usuario=session["usuario"])
    else:
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
    return render_template('productos.html')

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

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)