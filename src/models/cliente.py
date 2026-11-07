from dataclasses import dataclass
from typing import Optional


@dataclass
class Cliente:
    """Representa un cliente registrado en el sistema."""

    id_cliente: int
    nombre: str
    apellido: str
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    correo: Optional[str] = None