
from pathlib import Path


class AppConfig:
    """Carga y centraliza la configuración de la aplicación."""

    PROJECT_ROOT = Path(__file__).resolve().parents[2]
    ENV_FILE = PROJECT_ROOT / ".env"

    @classmethod
    def load_env(cls):
        """Carga las variables definidas en el archivo .env."""

        if not cls.ENV_FILE.is_file():
            raise FileNotFoundError(
                f"No se encontró el archivo de configuración: {cls.ENV_FILE}"
            )

        config = {}

        for line in cls.ENV_FILE.read_text(
            encoding="utf-8-sig"
        ).splitlines():

            line = line.strip()

            if not line or line.startswith("#") or "=" not in line:
                continue

            key, value = line.split("=", 1)
            config[key.strip()] = value.strip().strip('"').strip("'")

        return config

    @classmethod
    def get_database_config(cls):
        """Devuelve la configuración necesaria para SQL Server."""

        config = cls.load_env()

        required = [
            "DB_SERVER",
            "DB_NAME",
            "DB_USER",
            "DB_PASSWORD",
            "DB_DRIVER",
        ]

        missing = [
            key for key in required
            if not config.get(key)
        ]

        if missing:
            raise ValueError(
                f"Faltan variables de configuración: {', '.join(missing)}"
            )

        return {
            "server": config["DB_SERVER"],
            "database": config["DB_NAME"],
            "username": config["DB_USER"],
            "password": config["DB_PASSWORD"],
            "driver": config["DB_DRIVER"],
            "trust_server_certificate": (
                config.get("DB_TRUST_SERVER_CERTIFICATE", "no").lower()
                in ("yes", "true", "1")
            ),
        }
