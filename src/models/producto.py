from dataclasses import dataclass
from decimal import Decimal


@dataclass
class Producto:
    """Representa un producto disponible para la venta."""

    id_producto: int
    nombre: str
    precio: Decimal
    stock: int
    id_categoria: int