from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class Empleado:
    """Representa un empleado registrado en el sistema."""

    id_empleado: int
    nombre: str
    apellido: str
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    fecha_ingreso: Optional[date] = None