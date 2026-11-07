
from pathlib import Path

import pyodbc



from pathlib import Path


def load_env():
    """Lee las variables del archivo .env ubicado en la raíz."""

    project_root = Path(__file__).resolve().parents[2]
    env_path = project_root / ".env"

    print(f"Buscando archivo .env en: {env_path}")

    if not env_path.is_file():
        raise FileNotFoundError(
            f"No se encontró el archivo .env en: {env_path}"
        )

    config = {}

    for line in env_path.read_text(encoding="utf-8-sig").splitlines():
        line = line.strip()

        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        config[key.strip()] = value.strip().strip('"').strip("'")

    return config


def main():
    config = load_env()

    required = [
        "DB_SERVER",
        "DB_NAME",
        "DB_USER",
        "DB_PASSWORD",
        "DB_DRIVER",
    ]

    missing = [key for key in required if not config.get(key)]

    if missing:
        raise ValueError(f"Faltan variables en .env: {', '.join(missing)}")

    def odbc_value(value):
        return "{" + value.replace("}", "}}") + "}"

    trust_certificate = (
        config.get("DB_TRUST_SERVER_CERTIFICATE", "no").lower()
        in ("yes", "true", "1")
    )

    connection_string = (
        f"DRIVER={odbc_value(config['DB_DRIVER'])};"
        f"SERVER={odbc_value(config['DB_SERVER'])};"
        f"DATABASE={odbc_value(config['DB_NAME'])};"
        f"UID={odbc_value(config['DB_USER'])};"
        f"PWD={odbc_value(config['DB_PASSWORD'])};"
        f"Encrypt=yes;"
        f"TrustServerCertificate={'yes' if trust_certificate else 'no'};"
    )

    try:
        with pyodbc.connect(connection_string, timeout=5) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT DB_NAME(), SUSER_SNAME()")

            database, login = cursor.fetchone()

            print("CONEXIÓN EXITOSA")
            print(f"Base de datos: {database}")
            print(f"Usuario conectado: {login}")

    except pyodbc.Error as error:
        print("ERROR AL CONECTAR CON SQL SERVER")
        print(error)


if __name__ == "__main__":
    main()
