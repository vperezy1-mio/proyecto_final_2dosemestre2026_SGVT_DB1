from src.database.connection import DatabaseConnection
from src.models.categoria import Categoria


class CategoriaRepository:
    """Administra las consultas de categorías."""

    @staticmethod
    def obtener_todas():
        """Consulta todas las categorías registradas."""

        connection = DatabaseConnection.get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    id_categoria,
                    nombre
                FROM Categoria
                ORDER BY id_categoria
            """)

            categorias = []

            for row in cursor.fetchall():
                categorias.append(
                    Categoria(
                        id_categoria=row.id_categoria,
                        nombre=row.nombre
                    )
                )

            return categorias

        finally:
            connection.close()