from decimal import Decimal

from src.database.connection import DatabaseConnection
from src.models.venta import Venta
from src.models.detalle_venta import DetalleVenta
from src.repositories.venta_repository import VentaRepository


def contar_ventas():
    connection = DatabaseConnection.get_connection()

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM Venta")
        return cursor.fetchone()[0]
    finally:
        connection.close()


def probar_rollback():
    ventas_antes = contar_ventas()

    venta = Venta(
        id_venta=0,
        id_cliente=1,
        id_empleado=1
    )

    detalles = [
        DetalleVenta(
            id_venta=0,
            id_producto=999999,
            cantidad_venta=1,
            precio_venta=Decimal("1.00")
        )
    ]

    try:
        VentaRepository.registrar_venta(venta, detalles)

    except ValueError as error:
        print("Error controlado:", error)

    ventas_despues = contar_ventas()

    print("Ventas antes:", ventas_antes)
    print("Ventas después:", ventas_despues)

    if ventas_antes == ventas_despues:
        print("ROLLBACK CORRECTO: no se guardó ninguna venta.")
    else:
        print("ERROR: la cantidad de ventas cambió.")


if __name__ == "__main__":
    probar_rollback()