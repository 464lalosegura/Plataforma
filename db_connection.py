from flask import Flask, render_template, request, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# Función para crear la conexión a la base de datos
def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='plataforma',
            user='root',  
            password=''  
        )
        if connection.is_connected():
            print("Conexión exitosa a la base de datos")
            return connection
    except Error as e:
        print(f"Error al conectarse a la base de datos: {e}")
        return None

# Función para cerrar la conexión a la base de datos
def close_connection(connection):
    if connection.is_connected():
        connection.close()
        print("Conexión cerrada")

@app.route('/productos_por_categoria', methods=['POST'])
def productos_por_categoria():
    # Obtener el ID de la categoría desde el formulario o la petición
    categoria_id = request.form.get('categoria_id')
    if categoria_id:
        conn = create_connection()
        if conn:
            cursor = conn.cursor(dictionary=True)
            # Hacer la consulta a la base de datos
            cursor.execute('SELECT * FROM producto WHERE ID_Categoria = %s', (categoria_id,))
            productos = cursor.fetchall()
            close_connection(conn)  # Cerrar la conexión después de obtener los resultados

            return jsonify(productos)  # Retornar los productos como JSON

    # Si no se selecciona categoría o no se obtiene conexión
    return jsonify([])

# Otra ruta que puedas necesitar
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
