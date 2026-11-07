from src.repositories.empleado_repository import EmpleadoRepository


def main():
    try:
        empleados = EmpleadoRepository.obtener_todos()

        print("CONSULTA DE EMPLEADOS EXITOSA")
        print(f"Total de empleados: {len(empleados)}")

        for empleado in empleados:
            print(
                f"ID: {empleado.id_empleado} | "
                f"Nombre: {empleado.nombre} {empleado.apellido} | "
                f"Fecha de ingreso: {empleado.fecha_ingreso}"
            )

    except Exception as error:
        print("ERROR AL CONSULTAR EMPLEADOS")
        print(error)


if __name__ == "__main__":
    main()