from src.repositories.cliente_repository import ClienteRepository
from src.models.cliente import Cliente


def main():
    cliente = Cliente(
        id_cliente=0,
        nombre="Prueba",
        apellido="Repositorio",
        telefono="55550000",
        direccion="Direccion de prueba",
        correo="prueba.repositorio@example.com"
    )

    try:
        resultado = ClienteRepository.insertar(cliente)

        if resultado:
            print("CLIENTE REGISTRADO CORRECTAMENTE")
        else:
            print("NO SE REGISTRO EL CLIENTE")

        clientes = ClienteRepository.obtener_todos()

        for registrado in clientes:
            if registrado.correo == cliente.correo:
                print(f"ID generado por SQL Server: {registrado.id_cliente}")
                print(f"Nombre: {registrado.nombre} {registrado.apellido}")

    except Exception as error:
        print("ERROR AL REGISTRAR CLIENTE")
        print(error)


if __name__ == "__main__":
    main()