
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
    QLabel,
    QHeaderView,
)

from src.models.cliente import Cliente
from src.repositories.cliente_repository import ClienteRepository


class ClientesWindow(QWidget):
    """Ventana para administrar clientes."""

    def __init__(self):
        super().__init__()

        self.id_cliente = None

        self.setWindowTitle("Gestión de Clientes")
        self.resize(850, 550)

        self.crear_interfaz()
        self.cargar_clientes()

    def crear_interfaz(self):
        layout_principal = QVBoxLayout(self)

        titulo = QLabel("GESTIÓN DE CLIENTES")
        titulo.setStyleSheet(
            "font-size: 20px; font-weight: bold; padding: 10px;"
        )
        layout_principal.addWidget(titulo)

        formulario = QFormLayout()

        self.txt_nombre = QLineEdit()
        self.txt_apellido = QLineEdit()
        self.txt_telefono = QLineEdit()
        self.txt_direccion = QLineEdit()
        self.txt_correo = QLineEdit()

        formulario.addRow("Nombre:", self.txt_nombre)
        formulario.addRow("Apellido:", self.txt_apellido)
        formulario.addRow("Teléfono:", self.txt_telefono)
        formulario.addRow("Dirección:", self.txt_direccion)
        formulario.addRow("Correo:", self.txt_correo)

        layout_principal.addLayout(formulario)

        botones = QHBoxLayout()

        self.btn_nuevo = QPushButton("Nuevo")
        self.btn_guardar = QPushButton("Guardar")
        self.btn_actualizar = QPushButton("Actualizar")

        botones.addWidget(self.btn_nuevo)
        botones.addWidget(self.btn_guardar)
        botones.addWidget(self.btn_actualizar)

        layout_principal.addLayout(botones)

        self.tabla_clientes = QTableWidget()
        self.tabla_clientes.setColumnCount(6)
        self.tabla_clientes.setHorizontalHeaderLabels([
            "ID",
            "Nombre",
            "Apellido",
            "Teléfono",
            "Dirección",
            "Correo",
        ])

        self.tabla_clientes.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )

        self.tabla_clientes.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )

        self.tabla_clientes.setSelectionMode(
            QTableWidget.SelectionMode.SingleSelection
        )

        self.tabla_clientes.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        layout_principal.addWidget(self.tabla_clientes)

        self.btn_nuevo.clicked.connect(self.limpiar_formulario)
        self.btn_guardar.clicked.connect(self.guardar_cliente)
        self.btn_actualizar.clicked.connect(self.actualizar_cliente)

        self.tabla_clientes.cellClicked.connect(
            self.seleccionar_cliente
        )

    def cargar_clientes(self):
        try:
            clientes = ClienteRepository.obtener_todos()

            self.tabla_clientes.setRowCount(len(clientes))

            for fila, cliente in enumerate(clientes):
                valores = [
                    cliente.id_cliente,
                    cliente.nombre,
                    cliente.apellido,
                    cliente.telefono or "",
                    cliente.direccion or "",
                    cliente.correo or "",
                ]

                for columna, valor in enumerate(valores):
                    self.tabla_clientes.setItem(
                        fila,
                        columna,
                        QTableWidgetItem(str(valor))
                    )

        except Exception as error:
            QMessageBox.critical(
                self,
                "Error",
                f"No fue posible cargar los clientes:\n{error}"
            )

    def limpiar_formulario(self):
        self.id_cliente = None

        self.txt_nombre.clear()
        self.txt_apellido.clear()
        self.txt_telefono.clear()
        self.txt_direccion.clear()
        self.txt_correo.clear()

        self.tabla_clientes.clearSelection()

    def seleccionar_cliente(self, fila, columna):
        item = self.tabla_clientes.item(fila, 0)

        if item is None:
            return

        self.id_cliente = int(item.text())

        cliente = ClienteRepository.obtener_por_id(
            self.id_cliente
        )

        if cliente is None:
            QMessageBox.warning(
                self,
                "Aviso",
                "El cliente seleccionado ya no existe."
            )
            self.limpiar_formulario()
            return

        self.txt_nombre.setText(cliente.nombre)
        self.txt_apellido.setText(cliente.apellido)
        self.txt_telefono.setText(cliente.telefono or "")
        self.txt_direccion.setText(cliente.direccion or "")
        self.txt_correo.setText(cliente.correo or "")

    def obtener_datos_formulario(self):
        nombre = self.txt_nombre.text().strip()
        apellido = self.txt_apellido.text().strip()

        if not nombre or not apellido:
            raise ValueError(
                "El nombre y apellido son obligatorios."
            )

        return (
            nombre,
            apellido,
            self.txt_telefono.text().strip() or None,
            self.txt_direccion.text().strip() or None,
            self.txt_correo.text().strip() or None,
        )

    def guardar_cliente(self):
        try:
            datos = self.obtener_datos_formulario()

            cliente = Cliente(
                id_cliente=0,
                nombre=datos[0],
                apellido=datos[1],
                telefono=datos[2],
                direccion=datos[3],
                correo=datos[4],
            )

            if ClienteRepository.insertar(cliente):
                QMessageBox.information(
                    self,
                    "Éxito",
                    "Cliente registrado correctamente."
                )

                self.limpiar_formulario()
                self.cargar_clientes()

        except ValueError as error:
            QMessageBox.warning(self, "Validación", str(error))

        except Exception as error:
            QMessageBox.critical(
                self,
                "Error",
                f"No fue posible registrar el cliente:\n{error}"
            )

    def actualizar_cliente(self):
        if self.id_cliente is None:
            QMessageBox.warning(
                self,
                "Aviso",
                "Seleccione un cliente de la tabla."
            )
            return

        try:
            datos = self.obtener_datos_formulario()

            cliente = Cliente(
                id_cliente=self.id_cliente,
                nombre=datos[0],
                apellido=datos[1],
                telefono=datos[2],
                direccion=datos[3],
                correo=datos[4],
            )

            if ClienteRepository.actualizar(cliente):
                QMessageBox.information(
                    self,
                    "Éxito",
                    "Cliente actualizado correctamente."
                )

                self.limpiar_formulario()
                self.cargar_clientes()
            else:
                QMessageBox.warning(
                    self,
                    "Aviso",
                    "No se realizaron cambios en el cliente."
                )

        except ValueError as error:
            QMessageBox.warning(self, "Validación", str(error))

        except Exception as error:
            QMessageBox.critical(
                self,
                "Error",
                f"No fue posible actualizar el cliente:\n{error}"
            )
