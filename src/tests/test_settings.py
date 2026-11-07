
from src.config.settings import AppConfig


def main():
    config = AppConfig.get_database_config()

    print("CONFIGURACIÓN CARGADA CORRECTAMENTE")
    print(f"Servidor: {config['server']}")
    print(f"Base de datos: {config['database']}")
    print(f"Controlador: {config['driver']}")
    print("Credenciales: cargadas (no se muestran)")


if __name__ == "__main__":
    main()
