
from src.models.venta import Venta
from src.models.detalle_venta import DetalleVenta
from src.repositories.venta_repository import VentaRepository


class VentaService:
    """Contiene las reglas de negocio para registrar ventas."""

    @staticmethod
    def registrar_venta(id_cliente, id_empleado, detalles):
        """
        Valida y coordina el registro de una venta.

        Args:
            id_cliente: Identificador del cliente.
            id_empleado: Identificador del empleado.
            detalles: Lista de DetalleVenta.

        Returns:
            ID de la venta registrada.
        """

        if not isinstance(id_cliente, int) or id_cliente <= 0:
            raise ValueError("Debe seleccionar un cliente válido.")

        if not isinstance(id_empleado, int) or id_empleado <= 0:
            raise ValueError("Debe seleccionar un empleado válido.")

        if not detalles:
            raise ValueError("Debe agregar al menos un producto.")

        productos_agregados = set()

        for detalle in detalles:

            if not isinstance(detalle, DetalleVenta):
                raise TypeError("Los detalles deben ser objetos DetalleVenta.")

            if detalle.id_producto <= 0:
                raise ValueError("El producto seleccionado no es válido.")

            if detalle.cantidad_venta <= 0:
                raise ValueError("La cantidad debe ser mayor que cero.")

            if detalle.id_producto in productos_agregados:
                raise ValueError(
                    "No agregue el mismo producto más de una vez. "
                    "Modifique su cantidad en una sola línea."
                )

            productos_agregados.add(detalle.id_producto)

        venta = Venta(
            id_venta=0,
            id_cliente=id_cliente,
            id_empleado=id_empleado
        )

        return VentaRepository.registrar_venta(venta, detalles)
