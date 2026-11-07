
from src.database.connection import DatabaseConnection


class ConsultaRepository:
    """Centraliza las consultas e informes del sistema de ventas."""

    @staticmethod
    def _ejecutar_consulta(sql, parametros=None):
        """Ejecuta una consulta y devuelve sus resultados."""
        connection = DatabaseConnection.get_connection()

        try:
            cursor = connection.cursor()

            if parametros:
                cursor.execute(sql, parametros)
            else:
                cursor.execute(sql)

            columnas = [columna[0] for columna in cursor.description]
            resultados = cursor.fetchall()

            return [
                dict(zip(columnas, fila))
                for fila in resultados
            ]

        finally:
            connection.close()

    @staticmethod
    def historial_ventas():
        """Consulta el historial de ventas con su importe total."""
        sql = """
            SELECT
                V.id_venta,
                V.fecha_venta,
                C.nombre + ' ' + C.apellido AS cliente,
                E.nombre + ' ' + E.apellido AS empleado,
                SUM(D.cantidad_venta * D.precio_venta) AS total_venta
            FROM Venta V
            INNER JOIN Cliente C
                ON V.id_cliente = C.id_cliente
            INNER JOIN Empleado E
                ON V.id_empleado = E.id_empleado
            INNER JOIN DetalleVenta D
                ON V.id_venta = D.id_venta
            GROUP BY
                V.id_venta,
                V.fecha_venta,
                C.nombre,
                C.apellido,
                E.nombre,
                E.apellido
            ORDER BY V.fecha_venta DESC
        """

        return ConsultaRepository._ejecutar_consulta(sql)

    @staticmethod
    def compras_por_cliente(id_cliente):
        """Consulta los productos comprados por un cliente."""
        sql = """
            SELECT
                V.id_venta,
                V.fecha_venta,
                P.nombre AS producto,
                D.cantidad_venta,
                D.precio_venta,
                D.cantidad_venta * D.precio_venta AS subtotal
            FROM Venta V
            INNER JOIN DetalleVenta D
                ON V.id_venta = D.id_venta
            INNER JOIN Producto P
                ON D.id_producto = P.id_producto
            WHERE V.id_cliente = ?
            ORDER BY V.fecha_venta DESC
        """

        return ConsultaRepository._ejecutar_consulta(
            sql, (id_cliente,)
        )

    @staticmethod
    def ventas_por_empleado():
        """Empleados con ventas superiores a Q10,000."""
        sql = """
            SELECT
                E.id_empleado,
                E.nombre + ' ' + E.apellido AS empleado,
                COUNT(DISTINCT V.id_venta) AS cantidad_ventas,
                SUM(D.cantidad_venta * D.precio_venta) AS total_ventas
            FROM Empleado E
            INNER JOIN Venta V
                ON E.id_empleado = V.id_empleado
            INNER JOIN DetalleVenta D
                ON V.id_venta = D.id_venta
            GROUP BY
                E.id_empleado,
                E.nombre,
                E.apellido
            HAVING SUM(
                D.cantidad_venta * D.precio_venta
            ) > 10000
            ORDER BY total_ventas DESC
        """

        return ConsultaRepository._ejecutar_consulta(sql)

    @staticmethod
    def productos_mas_vendidos():
        """Productos vendidos en cantidades superiores a 10."""
        sql = """
            SELECT
                P.id_producto,
                P.nombre AS producto,
                SUM(D.cantidad_venta) AS cantidad_vendida
            FROM Producto P
            INNER JOIN DetalleVenta D
                ON P.id_producto = D.id_producto
            GROUP BY
                P.id_producto,
                P.nombre
            HAVING SUM(D.cantidad_venta) > 10
            ORDER BY cantidad_vendida DESC
        """

        return ConsultaRepository._ejecutar_consulta(sql)

    @staticmethod
    def ingresos_por_categoria():
        """Categorías con ingresos superiores a Q5,000."""
        sql = """
            SELECT
                C.id_categoria,
                C.nombre AS categoria,
                SUM(D.cantidad_venta * D.precio_venta) AS ingresos
            FROM Categoria C
            INNER JOIN Producto P
                ON C.id_categoria = P.id_categoria
            INNER JOIN DetalleVenta D
                ON P.id_producto = D.id_producto
            GROUP BY
                C.id_categoria,
                C.nombre
            HAVING SUM(
                D.cantidad_venta * D.precio_venta
            ) > 5000
            ORDER BY ingresos DESC
        """

        return ConsultaRepository._ejecutar_consulta(sql)

    @staticmethod
    def compras_cliente_categoria():
        """Compras por cliente y categoría superiores a Q2,000."""
        sql = """
            SELECT
                C.id_cliente,
                C.nombre + ' ' + C.apellido AS cliente,
                CAT.nombre AS categoria,
                SUM(D.cantidad_venta * D.precio_venta) AS total_comprado
            FROM Cliente C
            INNER JOIN Venta V
                ON C.id_cliente = V.id_cliente
            INNER JOIN DetalleVenta D
                ON V.id_venta = D.id_venta
            INNER JOIN Producto P
                ON D.id_producto = P.id_producto
            INNER JOIN Categoria CAT
                ON P.id_categoria = CAT.id_categoria
            GROUP BY
                C.id_cliente,
                C.nombre,
                C.apellido,
                CAT.id_categoria,
                CAT.nombre
            HAVING SUM(
                D.cantidad_venta * D.precio_venta
            ) > 2000
            ORDER BY total_comprado DESC
        """

        return ConsultaRepository._ejecutar_consulta(sql)

    @staticmethod
    def clientes_superan_promedio():
        """Clientes cuyas compras acumuladas superan el promedio
        de los importes individuales de las ventas.
        """
        sql = """
            WITH TotalesVenta AS (
                SELECT
                    V.id_venta,
                    V.id_cliente,
                    SUM(
                        D.cantidad_venta * D.precio_venta
                    ) AS total_venta
                FROM Venta V
                INNER JOIN DetalleVenta D
                    ON V.id_venta = D.id_venta
                GROUP BY
                    V.id_venta,
                    V.id_cliente
            ),
            PromedioVentas AS (
                SELECT AVG(total_venta) AS promedio
                FROM TotalesVenta
            )
            SELECT
                C.id_cliente,
                C.nombre + ' ' + C.apellido AS cliente,
                SUM(TV.total_venta) AS compras_acumuladas,
                PV.promedio AS promedio_ventas
            FROM Cliente C
            INNER JOIN TotalesVenta TV
                ON C.id_cliente = TV.id_cliente
            CROSS JOIN PromedioVentas PV
            GROUP BY
                C.id_cliente,
                C.nombre,
                C.apellido,
                PV.promedio
            HAVING SUM(TV.total_venta) > PV.promedio
            ORDER BY compras_acumuladas DESC
        """

        return ConsultaRepository._ejecutar_consulta(sql)
