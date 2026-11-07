
from src.repositories.consulta_repository import ConsultaRepository


def ejecutar_consultas():

    consultas = [
        ("1. Historial de ventas", ConsultaRepository.historial_ventas),
        ("2. Compras por cliente ID 1",
            lambda: ConsultaRepository.compras_por_cliente(1)),
        ("3. Ventas por empleado > Q10,000",
            ConsultaRepository.ventas_por_empleado),
        ("4. Productos vendidos > 10 unidades",
            ConsultaRepository.productos_mas_vendidos),
        ("5. Ingresos por categoría > Q5,000",
            ConsultaRepository.ingresos_por_categoria),
        ("6. Compras cliente-categoría > Q2,000",
            ConsultaRepository.compras_cliente_categoria),
        ("7. Clientes que superan el promedio",
            ConsultaRepository.clientes_superan_promedio),
    ]

    print("\n========== VALIDACIÓN DE CONSULTAS ==========")

    for nombre, consulta in consultas:
        print(f"\n{nombre}")
        print("-" * 60)

        try:
            resultados = consulta()

            print(f"Registros encontrados: {len(resultados)}")

            for registro in resultados[:5]:
                print(registro)

            if len(resultados) > 5:
                print("...")

            print("CONSULTA CORRECTA")

        except Exception as error:
            print(f"ERROR: {error}")
            raise

    print("\nVALIDACIÓN FINALIZADA CORRECTAMENTE.")


if __name__ == "__main__":
    ejecutar_consultas()
