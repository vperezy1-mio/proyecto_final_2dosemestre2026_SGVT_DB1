
from src.database.connection import DatabaseConnection


def main():
    try:
        with DatabaseConnection.get_connection() as connection:
            cursor = connection.cursor()

            cursor.execute(
                "SELECT DB_NAME(), SUSER_SNAME()"
            )

            database, login = cursor.fetchone()

            print("CONEXIÓN REUTILIZABLE EXITOSA")
            print(f"Base de datos: {database}")
            print(f"Usuario: {login}")

    except Exception as error:
        print("ERROR DE CONEXIÓN")
        print(error)


if __name__ == "__main__":
    main()
