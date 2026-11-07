
import sys

from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
)


def main():
    app = QApplication(sys.argv)

    window = QWidget()
    window.setWindowTitle("Prueba de PySide6 - SGVT")
    window.resize(400, 200)

    layout = QVBoxLayout(window)

    label = QLabel("PySide6 funciona correctamente.")
    label.setStyleSheet("font-size: 16px;")

    button = QPushButton("Cerrar ventana")
    button.clicked.connect(window.close)

    layout.addWidget(label)
    layout.addWidget(button)

    window.show()

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
