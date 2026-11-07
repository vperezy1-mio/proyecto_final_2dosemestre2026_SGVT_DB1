from datetime import date, datetime
from decimal import Decimal

from src.models.cliente import Cliente
from src.models.empleado import Empleado
from src.models.categoria import Categoria
from src.models.producto import Producto
from src.models.venta import Venta
from src.models.detalle_venta import DetalleVenta


def main():
    cliente = Cliente(
        id_cliente=1,
        nombre="Carlos",
        apellido="Perez"
    )

    empleado = Empleado(
        id_empleado=1,
        nombre="Luis",
        apellido="Gomez",
        fecha_ingreso=date(2026, 1, 10)
    )

    categoria = Categoria(
        id_categoria=1,
        nombre="Perifericos"
    )

    producto = Producto(
        id_producto=1,
        nombre="Teclado mecanico",
        precio=Decimal("450.00"),
        stock=25,
        id_categoria=1
    )

    venta = Venta(
        id_venta=1,
        id_cliente=1,
        id_empleado=1,
        fecha_venta=datetime(2026, 11, 6, 10, 30)
    )

    detalle = DetalleVenta(
        id_venta=1,
        id_producto=1,
        cantidad_venta=2,
        precio_venta=Decimal("450.00")
    )

    print("MODELOS CREADOS CORRECTAMENTE")
    print(cliente)
    print(empleado)
    print(categoria)
    print(producto)
    print(venta)
    print(detalle)


if __name__ == "__main__":
    main()