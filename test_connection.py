from mysql.connector import Error

def test_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='plataforma',
            user='root',  
            password=''  
        )
        if connection.is_connected():
            print("Conexión exitosa a la base de datos")
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM usuario")
            rows = cursor.fetchall()
            for row in rows:
                print(row)
    except Error as e:
        print(f"Error al conectarse a la base de datos: {e}")
    finally:
        if connection.is_connected():
            connection.close()

test_connection()
