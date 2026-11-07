
import pyodbc

from src.config.settings import AppConfig


class DatabaseConnection:
    """Administra las conexiones con SQL Server."""

    @staticmethod
    def get_connection():
        """Crea y devuelve una conexión con la base de datos."""

        config = AppConfig.get_database_config()

        def odbc_value(value):
            return "{" + value.replace("}", "}}") + "}"

        connection_string = (
            f"DRIVER={odbc_value(config['driver'])};"
            f"SERVER={odbc_value(config['server'])};"
            f"DATABASE={odbc_value(config['database'])};"
            f"UID={odbc_value(config['username'])};"
            f"PWD={odbc_value(config['password'])};"
            "Encrypt=yes;"
            f"TrustServerCertificate="
            f"{'yes' if config['trust_server_certificate'] else 'no'};"
        )

        return pyodbc.connect(
            connection_string,
            timeout=5
        )
