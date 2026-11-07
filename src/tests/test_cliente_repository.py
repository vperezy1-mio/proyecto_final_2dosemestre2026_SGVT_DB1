from src.repositories.cliente_repository import ClienteRepository


def main():
    try:
        clientes = ClienteRepository.obtener_todos()

        print("CONSULTA DE CLIENTES EXITOSA")
        print(f"Total de clientes: {len(clientes)}")

        for cliente in clientes:
            print(
                f"ID: {cliente.id_cliente} | "
                f"Nombre: {cliente.nombre} {cliente.apellido} | "
                f"Correo: {cliente.correo}"
            )

    except Exception as error:
        print("ERROR AL CONSULTAR CLIENTES")
        print(error)


if __name__ == "__main__":
    main()