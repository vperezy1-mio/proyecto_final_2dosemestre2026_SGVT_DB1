from dataclasses import dataclass


@dataclass
class Categoria:
    """Representa una categoría de productos."""

    id_categoria: int
    nombre: str