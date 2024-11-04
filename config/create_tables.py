from db_connection import create_connection, close_connection

def create_tables(connection):
    cursor = connection.cursor()

    # Crear tabla Categoria
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS categoria (
      ID_Categoria INT AUTO_INCREMENT PRIMARY KEY,
      Nombre VARCHAR(50) NOT NULL
    );
    """)

    # Crear tabla Direccion
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS direccion (
      ID_Direccion INT AUTO_INCREMENT PRIMARY KEY,
      Calle VARCHAR(50) NOT NULL,
      Numero VARCHAR(50) NOT NULL,
      Colonia VARCHAR(50) NOT NULL,
      Localidad VARCHAR(50) NOT NULL,
      CP VARCHAR(10) NOT NULL
    );
    """)

    # Crear tabla Usuario (Encargado)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuario (
      ID_Usuario INT AUTO_INCREMENT PRIMARY KEY,
      Nombre VARCHAR(50) NOT NULL,
      Correo VARCHAR(100) NOT NULL UNIQUE,
      Contraseña VARCHAR(255) NOT NULL,
      ID_Direccion INT NOT NULL,
      FOREIGN KEY (ID_Direccion) REFERENCES direccion(ID_Direccion) ON DELETE CASCADE
    );
    """)

    # Crear tabla Tienda
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tienda (
      ID_Tienda INT AUTO_INCREMENT PRIMARY KEY,
      Nombre VARCHAR(255) NOT NULL,
      Direccion VARCHAR(255) NOT NULL,
      Telefono VARCHAR(20) NOT NULL
    );
    """)

    # Crear tabla Producto
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS producto (
      ID_Producto INT AUTO_INCREMENT PRIMARY KEY,
      Descripcion VARCHAR(255) NOT NULL,
      Precio DECIMAL(10, 2) NOT NULL,
      Cantidad INT NOT NULL,
      ID_Categoria INT NOT NULL,
      ID_Tienda INT NOT NULL,
      FOREIGN KEY (ID_Categoria) REFERENCES categoria(ID_Categoria),
      FOREIGN KEY (ID_Tienda) REFERENCES tienda(ID_Tienda)
    );
    """)

    # Crear tabla Pedido
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pedido (
      ID_Pedido INT AUTO_INCREMENT PRIMARY KEY,
      Fecha DATE NOT NULL,
      Estado VARCHAR(50) NOT NULL,
      Tipo VARCHAR(50) NOT NULL,
      ID_Usuario INT NOT NULL,
      FOREIGN KEY (ID_Usuario) REFERENCES usuario(ID_Usuario) ON DELETE CASCADE
    );
    """)

    # Crear tabla Pedido_Producto (relación N:M entre Pedido y Producto)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pedido_producto (
      ID_Pedido INT NOT NULL,
      ID_Producto INT NOT NULL,
      Cantidad INT NOT NULL,
      PRIMARY KEY (ID_Pedido, ID_Producto),
      FOREIGN KEY (ID_Pedido) REFERENCES pedido(ID_Pedido) ON DELETE CASCADE,
      FOREIGN KEY (ID_Producto) REFERENCES producto(ID_Producto) ON DELETE CASCADE
    );
    """)

    # Crear tabla Almacen
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS almacen (
      ID_Almacen INT AUTO_INCREMENT PRIMARY KEY,
      Reporte TEXT NOT NULL
    );
    """)

    # Crear tabla Entrada_Salida (relacionada con Producto y Almacen)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS entrada_salida (
      ID_EntradaSalida INT AUTO_INCREMENT PRIMARY KEY,
      Tipo ENUM('entrada', 'salida') NOT NULL,
      Fecha DATE NOT NULL,
      Cantidad INT NOT NULL,
      ID_Producto INT NOT NULL,
      ID_Almacen INT NOT NULL,
      FOREIGN KEY (ID_Producto) REFERENCES producto(ID_Producto) ON DELETE CASCADE,
      FOREIGN KEY (ID_Almacen) REFERENCES almacen(ID_Almacen) ON DELETE CASCADE
    );
    """)

    connection.commit()
    print("Tablas creadas exitosamente.")

if __name__ == "__main__":
    conn = create_connection()
    if conn:
        create_tables(conn)
        close_connection(conn)
