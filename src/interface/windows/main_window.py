
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QStackedWidget,
)

from src.interface.windows.clientes_window import ClientesWindow
from src.interface.windows.ventas_window import VentasWindow
from src.interface.windows.consultas_window import ConsultasWindow


class MainWindow(QMainWindow):
    """Ventana principal del Sistema de Gestión de Ventas."""

    def __init__(self):
        super().__init__()

        self.setWindowTitle(
            "SGVT | Sistema de Gestión de Ventas de una Tienda"
        )
        self.resize(1100, 700)

        self.crear_interfaz()

    def crear_interfaz(self):
        central = QWidget()
        layout_principal = QVBoxLayout(central)

        titulo = QLabel(
            "SGVT | SISTEMA DE GESTIÓN DE VENTAS"
        )
        titulo.setStyleSheet("""
            font-size: 22px;
            font-weight: bold;
            padding: 15px;
        """)

        layout_principal.addWidget(titulo)

        # Navegación principal.
        navegacion = QHBoxLayout()

        self.btn_clientes = QPushButton("Clientes")
        self.btn_ventas = QPushButton("Ventas")
        self.btn_consultas = QPushButton("Consultas")

        navegacion.addWidget(self.btn_clientes)
        navegacion.addWidget(self.btn_ventas)
        navegacion.addWidget(self.btn_consultas)

        layout_principal.addLayout(navegacion)

        # Contenedor de módulos.
        self.paginas = QStackedWidget()

        self.clientes_window = ClientesWindow()
        self.ventas_window = VentasWindow()
        self.consultas_window = ConsultasWindow()

        self.paginas.addWidget(self.clientes_window)
        self.paginas.addWidget(self.ventas_window)
        self.paginas.addWidget(self.consultas_window)

        layout_principal.addWidget(self.paginas)

        self.setCentralWidget(central)

        # Navegación entre módulos.
        self.btn_clientes.clicked.connect(
            lambda: self.paginas.setCurrentWidget(
                self.clientes_window
            )
        )

        self.btn_ventas.clicked.connect(
            lambda: self.paginas.setCurrentWidget(
                self.ventas_window
            )
        )

        self.btn_consultas.clicked.connect(
            lambda: self.paginas.setCurrentWidget(
                self.consultas_window
            )
        )
