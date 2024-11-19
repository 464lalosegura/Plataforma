from create_tables import create_tables
from db_connection import create_connection, close_connection
from insert_data import (
    insert_categoria, insert_direccion, insert_usuario, 
    insert_tienda, insert_producto, insert_pedido, 
    insert_pedido_producto, insert_almacen, insert_entrada_salida
)

if __name__ == "__main__":
    # Establecer conexión con la base de datos
    conn = create_connection()
    
    if conn:
        # Crear las tablas de la base de datos (comentar esta línea si ya están creadas)
        create_tables(conn)
        print("Tablas creadas correctamente (si no existían).")
        
        # Aquí puedes agregar funciones de inserción si las necesitas en el futuro.
        # Las funciones importadas están listas para usar:
        # insert_categoria(conn, "Nombre de la categoría")
        # insert_direccion(conn, "Calle", numero, "Colonia", "Localidad", "CP")
        # insert_usuario(conn, "Nombre", "Correo", "Contraseña", id_direccion)
        # insert_tienda(conn, "Nombre de la tienda", "Dirección", "Teléfono")
        # insert_producto(conn, "Descripción", precio, cantidad, id_categoria, id_tienda)
        # insert_pedido(conn, "Fecha", "Estado", "Tipo", id_usuario)
        # insert_pedido_producto(conn, id_pedido, id_producto, cantidad)
        # insert_almacen(conn, "Reporte del almacén")
        # insert_entrada_salida(conn, "Tipo", "Fecha", cantidad, id_producto, id_almacen)

        # Cerrar la conexión
        close_connection(conn)
