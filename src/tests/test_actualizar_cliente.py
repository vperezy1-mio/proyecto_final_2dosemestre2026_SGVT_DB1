from src.repositories.cliente_repository import ClienteRepository
from src.models.cliente import Cliente


def main():
    cliente = Cliente(
        id_cliente=6,
        nombre="Prueba Actualizada",
        apellido="Repositorio",
        telefono="55551111",
        direccion="Nueva direccion de prueba",
        correo="prueba.actualizada@example.com"
    )

    try:
        resultado = ClienteRepository.actualizar(cliente)

        if resultado:
            print("CLIENTE ACTUALIZADO CORRECTAMENTE")
        else:
            print("NO SE ENCONTRO EL CLIENTE")

        clientes = ClienteRepository.obtener_todos()

        for registrado in clientes:
            if registrado.id_cliente == 6:
                print(f"ID: {registrado.id_cliente}")
                print(f"Nombre: {registrado.nombre} {registrado.apellido}")
                print(f"Telefono: {registrado.telefono}")
                print(f"Correo: {registrado.correo}")

    except Exception as error:
        print("ERROR AL ACTUALIZAR CLIENTE")
        print(error)


if __name__ == "__main__":
    main()