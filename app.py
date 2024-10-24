from flask import Flask, render_template, request, redirect, url_for, session, flash
from db_connection import create_connection, close_connection

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Clave secreta para manejar las sesiones

# Ruta para la página de inicio de sesión
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form["usuario"]
        contrasena = request.form["contrasena"]
        
        # Conectarse a la base de datos para verificar las credenciales
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuario WHERE nombre = %s AND contraseña = %s", (usuario, contrasena))
        user = cursor.fetchone()
        
        # Si las credenciales son correctas, redirigir al panel de control
        if user:
            session["usuario"] = usuario
            return redirect(url_for("panel_control"))
        else:
            # Si las credenciales no son válidas, mostrar un mensaje de error
            error = "Usuario o contraseña incorrectos"
            return render_template("iniciar_sesion.html", error=error)
    
    return render_template("iniciar_sesion.html")

# Ruta para el panel de control después de iniciar sesión
@app.route("/panel_control")
def panel_control():
    if "usuario" in session:
        # Aquí puedes mostrar el CRUD para pedidos, reclamos, etc.
        return render_template("panel_control.html", usuario=session["usuario"])
    else:
        return redirect(url_for("login"))

# Ruta para cerrar sesión
@app.route("/logout")
def logout():
    session.pop("usuario", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
    
#/PLATAFORMA
#│
#├── templates/                # Carpeta que contiene los archivos HTML
#│   ├── iniciar_sesion.html    # Página de inicio de sesión
#│   ├── interfazusuario.html   # Página de quejas, opiniones o sugerencias
#│   ├── productos.html         # Página de productos
#│   ├── pagina_de_inicio.html  # Página de inicio que acabamos de modificar
#│   └── ...otros archivos HTML
#│
#├── static/                   # Carpeta para recursos estáticos (CSS, imágenes, JS)
#│
#├── app.py                    # Archivo principal de Flask
#├── db_connection.py          # Archivo de conexión con la base de datos
#└── insert_data.py            # Archivo opcional para insertar datos iniciales
