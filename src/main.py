
import sys

from PySide6.QtWidgets import QApplication, QMessageBox

from src.interface.windows.main_window import MainWindow


def main():
    app = QApplication(sys.argv)

    try:
        ventana = MainWindow()
        ventana.show()

        sys.exit(app.exec())

    except Exception as error:
        QMessageBox.critical(
            None,
            "Error de inicio",
            f"No fue posible iniciar SGVT:\n{error}"
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
