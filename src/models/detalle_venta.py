from dataclasses import dataclass
from decimal import Decimal


@dataclass
class DetalleVenta:
    """Representa un producto incluido en una venta."""

    id_venta: int
    id_producto: int
    cantidad_venta: int
    precio_venta: Decimal