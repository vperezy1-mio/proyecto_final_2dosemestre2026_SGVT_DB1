from src.database.connection import DatabaseConnection
from src.models.producto import Producto


class ProductoRepository:
    """Administra las consultas de productos."""

    @staticmethod
    def obtener_todos():
        """Consulta todos los productos registrados."""

        connection = DatabaseConnection.get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    id_producto,
                    nombre,
                    precio,
                    stock,
                    id_categoria
                FROM Producto
                ORDER BY id_producto
            """)

            productos = []

            for row in cursor.fetchall():
                productos.append(
                    Producto(
                        id_producto=row.id_producto,
                        nombre=row.nombre,
                        precio=row.precio,
                        stock=row.stock,
                        id_categoria=row.id_categoria
                    )
                )

            return productos

        finally:
            connection.close()