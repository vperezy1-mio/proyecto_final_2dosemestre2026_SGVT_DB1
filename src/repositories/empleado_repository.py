from src.database.connection import DatabaseConnection
from src.models.empleado import Empleado


class EmpleadoRepository:
    """Administra las operaciones de acceso a datos de empleados."""

    @staticmethod
    def obtener_todos():
        """Consulta todos los empleados registrados."""

        connection = DatabaseConnection.get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    id_empleado,
                    nombre,
                    apellido,
                    telefono,
                    direccion,
                    fecha_ingreso
                FROM Empleado
                ORDER BY id_empleado
            """)

            empleados = []

            for row in cursor.fetchall():
                empleados.append(
                    Empleado(
                        id_empleado=row.id_empleado,
                        nombre=row.nombre,
                        apellido=row.apellido,
                        telefono=row.telefono,
                        direccion=row.direccion,
                        fecha_ingreso=row.fecha_ingreso
                    )
                )

            return empleados

        finally:
            connection.close()

    @staticmethod
    def insertar(empleado: Empleado):
        """Registra un nuevo empleado en la base de datos."""

        connection = DatabaseConnection.get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                INSERT INTO Empleado (
                    nombre,
                    apellido,
                    telefono,
                    direccion
                )
                VALUES (?, ?, ?, ?)
            """, (
                empleado.nombre,
                empleado.apellido,
                empleado.telefono,
                empleado.direccion
            ))

            connection.commit()

            return cursor.rowcount > 0

        except Exception:
            connection.rollback()
            raise

        finally:
            connection.close()