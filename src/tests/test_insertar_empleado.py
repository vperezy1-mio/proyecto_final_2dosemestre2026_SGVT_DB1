from src.repositories.empleado_repository import EmpleadoRepository
from src.models.empleado import Empleado


def main():
    empleado = Empleado(
        id_empleado=0,
        nombre="Prueba",
        apellido="Repositorio",
        telefono="55550000",
        direccion="Direccion de prueba"
    )

    try:
        resultado = EmpleadoRepository.insertar(empleado)

        if resultado:
            print("EMPLEADO REGISTRADO CORRECTAMENTE")
        else:
            print("NO SE REGISTRO EL EMPLEADO")

        empleados = EmpleadoRepository.obtener_todos()

        for registrado in empleados:
            if registrado.direccion == empleado.direccion:
                print(f"ID generado por SQL Server: {registrado.id_empleado}")
                print(f"Nombre: {registrado.nombre} {registrado.apellido}")

    except Exception as error:
        print("ERROR AL REGISTRAR EMPLEADO")
        print(error)


if __name__ == "__main__":
    main()