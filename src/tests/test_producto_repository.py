from src.repositories.producto_repository import ProductoRepository


def main():
    try:
        productos = ProductoRepository.obtener_todos()

        print("CONSULTA DE PRODUCTOS EXITOSA")
        print(f"Total de productos: {len(productos)}")

        for producto in productos:
            print(
                f"ID: {producto.id_producto} | "
                f"Nombre: {producto.nombre}"
            )

    except Exception as error:
        print("ERROR AL CONSULTAR PRODUCTOS")
        print(error)


if __name__ == "__main__":
    main()