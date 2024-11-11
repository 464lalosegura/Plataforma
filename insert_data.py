from db_connection import create_connection, close_connection

# Insertar en la tabla Categoria
def insert_categoria(connection, nombre):
    cursor = connection.cursor()
    cursor.execute("INSERT INTO categoria (Nombre) VALUES (%s)", (nombre,))
    connection.commit()
    print(f"Categoría '{nombre}' insertada.")

# Insertar en la tabla Direccion
def insert_direccion(connection, calle, numero, colonia, localidad, cp):
    cursor = connection.cursor()
    cursor.execute("""
    INSERT INTO direccion (Calle, Numero, Colonia, Localidad, CP)
    VALUES (%s, %s, %s, %s, %s)
    """, (calle, numero, colonia, localidad, cp))
    connection.commit()
    print(f"Dirección '{calle} {numero}' insertada.")

# Insertar en la tabla Usuario (Encargado)
def insert_usuario(connection, nombre, correo, contraseña, id_direccion):
    cursor = connection.cursor()
    cursor.execute("""
    INSERT INTO usuario (Nombre, Correo, Contraseña, ID_Direccion)
    VALUES (%s, %s, %s, %s)
    """, (nombre, correo, contraseña, id_direccion))
    connection.commit()
    print(f"Usuario '{nombre}' insertado.")

# Insertar en la tabla Tienda
def insert_tienda(connection, nombre, direccion, telefono):
    cursor = connection.cursor()
    cursor.execute("""
    INSERT INTO tienda (Nombre, Direccion, Telefono)
    VALUES (%s, %s, %s)
    """, (nombre, direccion, telefono))
    connection.commit()
    print(f"Tienda '{nombre}' insertada.")

# Insertar en la tabla Producto
def insert_producto(connection, descripcion, precio, cantidad, id_categoria, id_tienda):
    cursor = connection.cursor()
    cursor.execute("""
    INSERT INTO producto (Descripcion, Precio, Cantidad, ID_Categoria, ID_Tienda)
    VALUES (%s, %s, %s, %s, %s)
    """, (descripcion, precio, cantidad, id_categoria, id_tienda))
    connection.commit()
    print(f"Producto '{descripcion}' insertado.")

# Insertar en la tabla Pedido
def insert_pedido(connection, fecha, estado, tipo, id_usuario):
    cursor = connection.cursor()
    cursor.execute("""
    INSERT INTO pedido (Fecha, Estado, Tipo, ID_Usuario)
    VALUES (%s, %s, %s, %s)
    """, (fecha, estado, tipo, id_usuario))
    connection.commit()
    print(f"Pedido del usuario '{id_usuario}' insertado.")

# Insertar en la tabla Pedido_Producto (relación N:M entre Pedido y Producto)
def insert_pedido_producto(connection, id_pedido, id_producto, cantidad):
    cursor = connection.cursor()
    cursor.execute("""
    INSERT INTO pedido_producto (ID_Pedido, ID_Producto, Cantidad)
    VALUES (%s, %s, %s)
    """, (id_pedido, id_producto, cantidad))
    connection.commit()
    print(f"Producto '{id_producto}' añadido al pedido '{id_pedido}'.")

# Insertar en la tabla Almacen
def insert_almacen(connection, reporte):
    cursor = connection.cursor()
    cursor.execute("""
    INSERT INTO almacen (Reporte)
    VALUES (%s)
    """, (reporte,))
    connection.commit()
    print(f"Almacén creado con reporte '{reporte}'.")

# Insertar en la tabla Entrada_Salida (relacionada con Producto y Almacen)
def insert_entrada_salida(connection, tipo, fecha, cantidad, id_producto, id_almacen):
    cursor = connection.cursor()
    cursor.execute("""
    INSERT INTO entrada_salida (Tipo, Fecha, Cantidad, ID_Producto, ID_Almacen)
    VALUES (%s, %s, %s, %s, %s)
    """, (tipo, fecha, cantidad, id_producto, id_almacen))
    connection.commit()
    print(f"Movimiento '{tipo}' insertado para el producto '{id_producto}'.")

# Ejemplo de uso (sin inserciones)
if __name__ == "__main__":
    conn = create_connection()
    if conn:
        print("Conexión establecida. Puedes comenzar a insertar datos.")
        close_connection(conn)
