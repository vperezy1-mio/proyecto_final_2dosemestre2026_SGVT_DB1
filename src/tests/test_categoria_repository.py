from src.repositories.categoria_repository import CategoriaRepository


def main():
    try:
        categorias = CategoriaRepository.obtener_todas()

        print("CONSULTA DE CATEGORIAS EXITOSA")
        print(f"Total de categorias: {len(categorias)}")

        for categoria in categorias:
            print(
                f"ID: {categoria.id_categoria} | "
                f"Nombre: {categoria.nombre}"
            )

    except Exception as error:
        print("ERROR AL CONSULTAR CATEGORIAS")
        print(error)


if __name__ == "__main__":
    main()