
from decimal import Decimal

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QComboBox,
    QSpinBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
    QLabel,
    QHeaderView,
)

from src.repositories.cliente_repository import ClienteRepository
from src.repositories.empleado_repository import EmpleadoRepository
from src.repositories.producto_repository import ProductoRepository
from src.services.venta_service import VentaService
from src.models.detalle_venta import DetalleVenta


class VentasWindow(QWidget):
    """Ventana para registrar ventas y administrar el carrito."""

    def __init__(self):
        super().__init__()

        self.productos = {}
        self.carrito = {}

        self.setWindowTitle("Gestión de Ventas")
        self.resize(950, 650)

        self.crear_interfaz()
        self.cargar_catalogos()

    def crear_interfaz(self):
        layout_principal = QVBoxLayout(self)

        titulo = QLabel("REGISTRO DE VENTAS")
        titulo.setStyleSheet(
            "font-size: 20px; font-weight: bold; padding: 10px;"
        )
        layout_principal.addWidget(titulo)

        # Selección de cliente y empleado.
        formulario = QFormLayout()

        self.cmb_cliente = QComboBox()
        self.cmb_empleado = QComboBox()

        formulario.addRow("Cliente:", self.cmb_cliente)
        formulario.addRow("Empleado:", self.cmb_empleado)

        layout_principal.addLayout(formulario)

        # Selección de productos.
        seleccion = QHBoxLayout()

        self.cmb_producto = QComboBox()

        self.spn_cantidad = QSpinBox()
        self.spn_cantidad.setMinimum(1)
        self.spn_cantidad.setMaximum(99999)

        self.btn_agregar = QPushButton("Agregar producto")

        seleccion.addWidget(QLabel("Producto:"))
        seleccion.addWidget(self.cmb_producto, 3)
        seleccion.addWidget(QLabel("Cantidad:"))
        seleccion.addWidget(self.spn_cantidad)
        seleccion.addWidget(self.btn_agregar)

        layout_principal.addLayout(seleccion)

        # Carrito de compra.
        self.tabla_carrito = QTableWidget()
        self.tabla_carrito.setColumnCount(5)

        self.tabla_carrito.setHorizontalHeaderLabels([
            "ID",
            "Producto",
            "Cantidad",
            "Precio unitario",
            "Subtotal",
        ])

        self.tabla_carrito.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )

        self.tabla_carrito.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )

        self.tabla_carrito.setSelectionMode(
            QTableWidget.SelectionMode.SingleSelection
        )

        self.tabla_carrito.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        layout_principal.addWidget(self.tabla_carrito)

        # Total de la venta.
        self.lbl_total = QLabel("TOTAL: Q0.00")
        self.lbl_total.setStyleSheet(
            "font-size: 22px; font-weight: bold; padding: 10px;"
        )

        layout_principal.addWidget(self.lbl_total)

        # Botones de operación.
        botones = QHBoxLayout()

        self.btn_quitar = QPushButton("Quitar producto")
        self.btn_limpiar = QPushButton("Limpiar venta")
        self.btn_registrar = QPushButton("Registrar venta")

        botones.addWidget(self.btn_quitar)
        botones.addWidget(self.btn_limpiar)
        botones.addWidget(self.btn_registrar)

        layout_principal.addLayout(botones)

        # Conexiones.
        self.btn_agregar.clicked.connect(self.agregar_producto)
        self.btn_quitar.clicked.connect(self.quitar_producto)
        self.btn_limpiar.clicked.connect(self.limpiar_venta)
        self.btn_registrar.clicked.connect(self.registrar_venta)

    def cargar_catalogos(self):
        try:
            clientes = ClienteRepository.obtener_todos()
            empleados = EmpleadoRepository.obtener_todos()
            productos = ProductoRepository.obtener_todos()

            self.cmb_cliente.clear()
            self.cmb_empleado.clear()
            self.cmb_producto.clear()

            for cliente in clientes:
                nombre = f"{cliente.nombre} {cliente.apellido}"
                self.cmb_cliente.addItem(nombre, cliente.id_cliente)

            for empleado in empleados:
                nombre = f"{empleado.nombre} {empleado.apellido}"
                self.cmb_empleado.addItem(nombre, empleado.id_empleado)

            self.productos = {
                producto.id_producto: producto
                for producto in productos
            }

            for producto in productos:
                texto = (
                    f"{producto.nombre} | "
                    f"Q{producto.precio} | "
                    f"Stock: {producto.stock}"
                )

                if producto.stock > 0:
                    self.cmb_producto.addItem(
                        texto,
                        producto.id_producto
                    )

        except Exception as error:
            QMessageBox.critical(
                self,
                "Error",
                f"No fue posible cargar los catálogos:\n{error}"
            )

    def agregar_producto(self):
        id_producto = self.cmb_producto.currentData()

        if id_producto is None:
            QMessageBox.warning(
                self,
                "Aviso",
                "No hay productos disponibles."
            )
            return

        producto = self.productos[id_producto]
        cantidad = self.spn_cantidad.value()

        cantidad_actual = self.carrito.get(
            id_producto, {}
        ).get("cantidad", 0)

        nueva_cantidad = cantidad_actual + cantidad

        if nueva_cantidad > producto.stock:
            QMessageBox.warning(
                self,
                "Existencias insuficientes",
                f"Stock disponible: {producto.stock}\n"
                f"Cantidad solicitada: {nueva_cantidad}"
            )
            return

        self.carrito[id_producto] = {
            "producto": producto,
            "cantidad": nueva_cantidad,
            "precio": Decimal(str(producto.precio)),
        }

        self.actualizar_tabla()

    def actualizar_tabla(self):
        self.tabla_carrito.setRowCount(len(self.carrito))

        total = Decimal("0.00")

        for fila, (id_producto, item) in enumerate(
            self.carrito.items()
        ):
            producto = item["producto"]
            cantidad = item["cantidad"]
            precio = item["precio"]
            subtotal = precio * cantidad

            total += subtotal

            valores = [
                id_producto,
                producto.nombre,
                cantidad,
                f"Q{precio:.2f}",
                f"Q{subtotal:.2f}",
            ]

            for columna, valor in enumerate(valores):
                self.tabla_carrito.setItem(
                    fila,
                    columna,
                    QTableWidgetItem(str(valor))
                )

        self.lbl_total.setText(f"TOTAL: Q{total:.2f}")

    def quitar_producto(self):
        fila = self.tabla_carrito.currentRow()

        if fila < 0:
            QMessageBox.warning(
                self,
                "Aviso",
                "Seleccione un producto del carrito."
            )
            return

        item = self.tabla_carrito.item(fila, 0)

        if item is None:
            return

        id_producto = int(item.text())

        self.carrito.pop(id_producto, None)

        self.actualizar_tabla()

    def limpiar_venta(self):
        self.carrito.clear()
        self.tabla_carrito.setRowCount(0)
        self.lbl_total.setText("TOTAL: Q0.00")

    def registrar_venta(self):
        id_cliente = self.cmb_cliente.currentData()
        id_empleado = self.cmb_empleado.currentData()

        if id_cliente is None or id_empleado is None:
            QMessageBox.warning(
                self,
                "Aviso",
                "Debe seleccionar un cliente y un empleado."
            )
            return

        if not self.carrito:
            QMessageBox.warning(
                self,
                "Aviso",
                "Agregue al menos un producto."
            )
            return

        detalles = [
            DetalleVenta(
                id_venta=0,
                id_producto=id_producto,
                cantidad_venta=item["cantidad"],
                precio_venta=item["precio"],
            )
            for id_producto, item in self.carrito.items()
        ]

        total = sum(
            (
                item["precio"] * item["cantidad"]
                for item in self.carrito.values()
            ),
            Decimal("0.00")
        )

        respuesta = QMessageBox.question(
            self,
            "Confirmar venta",
            f"Total de la venta: Q{total:.2f}\n\n"
            "¿Desea registrar esta venta?",
            QMessageBox.StandardButton.Yes
            | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )

        if respuesta != QMessageBox.StandardButton.Yes:
            return

        try:
            id_venta = VentaService.registrar_venta(
                id_cliente,
                id_empleado,
                detalles
            )

            QMessageBox.information(
                self,
                "Venta registrada",
                f"Venta registrada correctamente.\n"
                f"Número de venta: {id_venta}\n"
                f"Total: Q{total:.2f}"
            )

            self.limpiar_venta()
            self.cargar_catalogos()

        except Exception as error:
            QMessageBox.critical(
                self,
                "Error al registrar",
                f"No fue posible registrar la venta:\n{error}"
            )
