from src.repositories.cliente_repository import ClienteRepository


def main():
    try:
        print("========== CLIENTE EXISTENTE ==========")

        cliente = ClienteRepository.obtener_por_id(6)

        if cliente:
            print(f"ID: {cliente.id_cliente}")
            print(f"Nombre: {cliente.nombre} {cliente.apellido}")
            print(f"Telefono: {cliente.telefono}")
            print(f"Correo: {cliente.correo}")
        else:
            print("Cliente no encontrado.")

        print("\n========== CLIENTE INEXISTENTE ==========")

        cliente = ClienteRepository.obtener_por_id(999)

        if cliente is None:
            print("Busqueda correcta: el cliente no existe.")
        else:
            print(f"Cliente encontrado: {cliente}")

    except Exception as error:
        print("ERROR AL CONSULTAR CLIENTE")
        print(error)


if __name__ == "__main__":
    main()