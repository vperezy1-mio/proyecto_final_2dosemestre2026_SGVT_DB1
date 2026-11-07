from src.database.connection import DatabaseConnection
from src.models.cliente import Cliente


class ClienteRepository:
    """Administra las operaciones de acceso a datos de clientes."""

    @staticmethod
    def obtener_todos():
        """Consulta todos los clientes registrados."""

        connection = DatabaseConnection.get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    id_cliente,
                    nombre,
                    apellido,
                    telefono,
                    direccion,
                    correo
                FROM Cliente
                ORDER BY id_cliente
            """)

            clientes = []

            for row in cursor.fetchall():
                clientes.append(
                    Cliente(
                        id_cliente=row.id_cliente,
                        nombre=row.nombre,
                        apellido=row.apellido,
                        telefono=row.telefono,
                        direccion=row.direccion,
                        correo=row.correo
                    )
                )

            return clientes

        finally:
            connection.close()

    @staticmethod
    def insertar(cliente: Cliente):
        """Registra un nuevo cliente en la base de datos."""

        connection = DatabaseConnection.get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                INSERT INTO Cliente (
                    nombre,
                    apellido,
                    telefono,
                    direccion,
                    correo
                )
                VALUES (?, ?, ?, ?, ?)
            """, (
                cliente.nombre,
                cliente.apellido,
                cliente.telefono,
                cliente.direccion,
                cliente.correo
            ))

            connection.commit()

            return cursor.rowcount > 0

        except Exception:
            connection.rollback()
            raise

        finally:
            connection.close()

    @staticmethod
    def actualizar(cliente: Cliente):
        """Actualiza los datos de un cliente existente."""

        connection = DatabaseConnection.get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                UPDATE Cliente
                SET
                    nombre = ?,
                    apellido = ?,
                    telefono = ?,
                    direccion = ?,
                    correo = ?
                WHERE id_cliente = ?
            """, (
                cliente.nombre,
                cliente.apellido,
                cliente.telefono,
                cliente.direccion,
                cliente.correo,
                cliente.id_cliente
            ))

            actualizado = cursor.rowcount > 0

            connection.commit()

            return actualizado

        except Exception:
            connection.rollback()
            raise

        finally:
            connection.close()


    @staticmethod
    def obtener_por_id(id_cliente: int):
        """Consulta un cliente mediante su identificador."""

        connection = DatabaseConnection.get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    id_cliente,
                    nombre,
                    apellido,
                    telefono,
                    direccion,
                    correo
                FROM Cliente
                WHERE id_cliente = ?
            """, (id_cliente,))

            row = cursor.fetchone()

            if row is None:
                return None

            return Cliente(
                id_cliente=row.id_cliente,
                nombre=row.nombre,
                apellido=row.apellido,
                telefono=row.telefono,
                direccion=row.direccion,
                correo=row.correo
            )

        finally:
            connection.close()