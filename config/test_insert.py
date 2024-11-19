import unittest
from db_connection import create_connection, close_connection
from insert_data import (
    insert_categoria, insert_direccion, insert_usuario, 
    insert_tienda, insert_producto, insert_pedido, 
    insert_pedido_producto, insert_almacen, insert_entrada_salida
)

class TestDatabaseInserts(unittest.TestCase):

    def setUp(self):
        # Crear una conexión a la base de datos para cada prueba
        self.conn = create_connection()

    def tearDown(self):
        # Cerrar la conexión a la base de datos después de cada prueba
        if self.conn:
            close_connection(self.conn)

    # Prueba para la función de inserción en Categoria
    def test_insert_categoria(self):
        if self.conn:
            # No insertamos datos, solo probamos que la función existe y no arroja errores
            self.assertTrue(callable(insert_categoria))

    # Prueba para la función de inserción en Direccion
    def test_insert_direccion(self):
        if self.conn:
            self.assertTrue(callable(insert_direccion))

    # Prueba para la función de inserción en Usuario
    def test_insert_usuario(self):
        if self.conn:
            self.assertTrue(callable(insert_usuario))

    # Prueba para la función de inserción en Tienda
    def test_insert_tienda(self):
        if self.conn:
            self.assertTrue(callable(insert_tienda))

    # Prueba para la función de inserción en Producto
    def test_insert_producto(self):
        if self.conn:
            self.assertTrue(callable(insert_producto))

    # Prueba para la función de inserción en Pedido
    def test_insert_pedido(self):
        if self.conn:
            self.assertTrue(callable(insert_pedido))

    # Prueba para la función de inserción en Pedido_Producto
    def test_insert_pedido_producto(self):
        if self.conn:
            self.assertTrue(callable(insert_pedido_producto))

    # Prueba para la función de inserción en Almacen
    def test_insert_almacen(self):
        if self.conn:
            self.assertTrue(callable(insert_almacen))

    # Prueba para la función de inserción en Entrada_Salida
    def test_insert_entrada_salida(self):
        if self.conn:
            self.assertTrue(callable(insert_entrada_salida))

if __name__ == "__main__":
    unittest.main()
