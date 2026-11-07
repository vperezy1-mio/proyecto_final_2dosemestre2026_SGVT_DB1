
from datetime import date, datetime
from decimal import Decimal

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QComboBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
    QLabel,
    QHeaderView,
)

from src.repositories.consulta_repository import ConsultaRepository
from src.repositories.cliente_repository import ClienteRepository


class ConsultasWindow(QWidget):
    """Ventana para visualizar los siete informes del sistema."""

    def __init__(self):
        super().__init__()

        self.consultas = [
            ("Historial de ventas", ConsultaRepository.historial_ventas),
            ("Compras por cliente", None),
            ("Ventas por empleado", ConsultaRepository.ventas_por_empleado),
            ("Productos más vendidos", ConsultaRepository.productos_mas_vendidos),
            ("Ingresos por categoría", ConsultaRepository.ingresos_por_categoria),
            ("Compras por cliente y categoría",
             ConsultaRepository.compras_cliente_categoria),
            ("Clientes sobre el promedio",
             ConsultaRepository.clientes_superan_promedio),
        ]

        self.setWindowTitle("Consultas e Informes")
        self.resize(1000, 600)

        self.crear_interfaz()
        self.cargar_clientes()

    def crear_interfaz(self):
        layout_principal = QVBoxLayout(self)

        titulo = QLabel("CONSULTAS E INFORMES")
        titulo.setStyleSheet(
            "font-size: 20px; font-weight: bold; padding: 10px;"
        )
        layout_principal.addWidget(titulo)

        seleccion = QHBoxLayout()

        self.cmb_consulta = QComboBox()
        self.cmb_consulta.addItems([
            consulta[0] for consulta in self.consultas
        ])

        self.cmb_cliente = QComboBox()

        self.btn_consultar = QPushButton("Ejecutar consulta")

        seleccion.addWidget(QLabel("Informe:"))
        seleccion.addWidget(self.cmb_consulta, 3)
        seleccion.addWidget(QLabel("Cliente:"))
        seleccion.addWidget(self.cmb_cliente, 2)
        seleccion.addWidget(self.btn_consultar)

        layout_principal.addLayout(seleccion)

        self.lbl_resultado = QLabel(
            "Seleccione un informe y presione Ejecutar consulta."
        )
        layout_principal.addWidget(self.lbl_resultado)

        self.tabla_resultados = QTableWidget()

        self.tabla_resultados.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )

        self.tabla_resultados.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )

        self.tabla_resultados.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents
        )

        self.tabla_resultados.horizontalHeader().setStretchLastSection(
            True
        )

        layout_principal.addWidget(self.tabla_resultados)

        self.cmb_consulta.currentIndexChanged.connect(
            self.actualizar_selector_cliente
        )

        self.btn_consultar.clicked.connect(
            self.ejecutar_consulta
        )

        self.actualizar_selector_cliente()

    def cargar_clientes(self):
        try:
            clientes = ClienteRepository.obtener_todos()

            self.cmb_cliente.clear()

            for cliente in clientes:
                nombre = f"{cliente.nombre} {cliente.apellido}"

                self.cmb_cliente.addItem(
                    nombre,
                    cliente.id_cliente
                )

        except Exception as error:
            QMessageBox.critical(
                self,
                "Error",
                f"No fue posible cargar los clientes:\n{error}"
            )

    def actualizar_selector_cliente(self):
        # El selector de clientes solo se necesita en la consulta 2.
        visible = self.cmb_consulta.currentIndex() == 1

        self.cmb_cliente.setVisible(visible)

        for widget in self.findChildren(QLabel):
            if widget.text() == "Cliente:":
                widget.setVisible(visible)

    def ejecutar_consulta(self):
        indice = self.cmb_consulta.currentIndex()

        try:
            if indice == 1:
                id_cliente = self.cmb_cliente.currentData()

                if id_cliente is None:
                    QMessageBox.warning(
                        self,
                        "Aviso",
                        "Seleccione un cliente."
                    )
                    return

                resultados = (
                    ConsultaRepository.compras_por_cliente(id_cliente)
                )

            else:
                funcion = self.consultas[indice][1]
                resultados = funcion()

            self.mostrar_resultados(resultados)

            self.lbl_resultado.setText(
                f"Registros encontrados: {len(resultados)}"
            )

        except Exception as error:
            QMessageBox.critical(
                self,
                "Error",
                f"No fue posible ejecutar la consulta:\n{error}"
            )

    def mostrar_resultados(self, resultados):
        self.tabla_resultados.clear()

        if not resultados:
            self.tabla_resultados.setRowCount(0)
            self.tabla_resultados.setColumnCount(0)
            return

        columnas = list(resultados[0].keys())

        self.tabla_resultados.setColumnCount(len(columnas))
        self.tabla_resultados.setRowCount(len(resultados))
        self.tabla_resultados.setHorizontalHeaderLabels(columnas)

        for fila, registro in enumerate(resultados):
            for columna, nombre in enumerate(columnas):
                valor = registro[nombre]

                if isinstance(valor, Decimal):
                    texto = f"Q{valor:,.2f}"

                elif isinstance(valor, (date, datetime)):
                    texto = valor.strftime("%d/%m/%Y %H:%M") \
                        if isinstance(valor, datetime) \
                        else valor.strftime("%d/%m/%Y")

                else:
                    texto = str(valor) if valor is not None else ""

                self.tabla_resultados.setItem(
                    fila,
                    columna,
                    QTableWidgetItem(texto)
                )

        self.tabla_resultados.resizeColumnsToContents()
