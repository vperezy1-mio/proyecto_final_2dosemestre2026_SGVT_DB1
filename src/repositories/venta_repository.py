from src.database.connection import DatabaseConnection
from src.models.venta import Venta
from src.models.detalle_venta import DetalleVenta


class VentaRepository:
    """Administra las operaciones de acceso a datos de ventas."""

    @staticmethod
    def registrar_venta(venta: Venta, detalles: list[DetalleVenta]):
        """Registra una venta completa mediante una transacción."""

        if not detalles:
            raise ValueError("La venta debe contener al menos un producto.")

        connection = DatabaseConnection.get_connection()

        try:
            cursor = connection.cursor()

            # 1. Insertar encabezado y recuperar el ID.
            cursor.execute("""
                INSERT INTO Venta (id_cliente, id_empleado)
                OUTPUT INSERTED.id_venta
                VALUES (?, ?)
            """, (
                venta.id_cliente,
                venta.id_empleado
            ))

            id_venta = cursor.fetchone()[0]

            # 2. Procesar los detalles.
            for detalle in detalles:

                if detalle.cantidad_venta <= 0:
                    raise ValueError(
                        "La cantidad debe ser mayor que cero."
                    )

                # Descontar stock y recuperar el precio real.
                cursor.execute("""
                    UPDATE Producto
                    SET stock = stock - ?
                    OUTPUT DELETED.precio
                    WHERE id_producto = ?
                    AND stock >= ?
                """, (
                    detalle.cantidad_venta,
                    detalle.id_producto,
                    detalle.cantidad_venta
                ))

                resultado = cursor.fetchone()

                if resultado is None:
                    raise ValueError(
                        f"Producto {detalle.id_producto} inexistente "
                        "o con existencias insuficientes."
                    )

                precio_actual = resultado[0]

                # 3. Guardar el precio histórico.
                cursor.execute("""
                    INSERT INTO DetalleVenta (
                        id_venta,
                        id_producto,
                        cantidad_venta,
                        precio_venta
                    )
                    VALUES (?, ?, ?, ?)
                """, (
                    id_venta,
                    detalle.id_producto,
                    detalle.cantidad_venta,
                    precio_actual
                ))

            # 4. Confirmar la transacción.
            connection.commit()

            return id_venta

        except Exception:
            connection.rollback()
            raise

        finally:
            connection.close()