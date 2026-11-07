from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Venta:
    """Representa el encabezado de una venta."""

    id_venta: int
    id_cliente: int
    id_empleado: int
    fecha_venta: Optional[datetime] = None