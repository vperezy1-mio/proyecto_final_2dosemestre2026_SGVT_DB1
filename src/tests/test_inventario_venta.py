from src.database.connection import DatabaseConnection


def consultar_inventario():
    connection = DatabaseConnection.get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                id_producto,
                nombre,
                precio,
                stock
            FROM Producto
            ORDER BY id_producto
        """)

        productos = cursor.fetchall()

        print("\n========== INVENTARIO ACTUAL ==========")

        for producto in productos:
            print(
                f"ID: {producto.id_producto} | "
                f"Producto: {producto.nombre} | "
                f"Precio: Q{producto.precio} | "
                f"Stock: {producto.stock}"
            )

    finally:
        connection.close()


if __name__ == "__main__":
    consultar_inventario()