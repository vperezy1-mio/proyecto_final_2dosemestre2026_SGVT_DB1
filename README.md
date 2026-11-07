
# SGVT - Sistema de Gestión de Ventas de una Tienda

Proyecto académico desarrollado para el curso de Base de Datos 1 de la Universidad Mariano Gálvez de Guatemala.

## 1. Descripción del proyecto

SGVT es una aplicación de escritorio desarrollada en Python que permite gestionar las operaciones principales de una tienda de tecnología.

El sistema utiliza SQL Server como motor de base de datos y PySide6 para construir una interfaz gráfica que facilita la administración de clientes, el registro de ventas y la generación de consultas e informes.

## 2. Objetivo general

Desarrollar un sistema de gestión de ventas que permita administrar información de clientes, empleados, productos, categorías y ventas, aplicando los principios de diseño, normalización e integridad de bases de datos relacionales.

## 3. Tecnologías utilizadas

- Python 3.12
- Microsoft SQL Server
- SQL Server Express
- PySide6
- pyodbc
- Git y GitHub

## 4. Funcionalidades principales

### Gestión de clientes
- Registrar clientes.
- Consultar clientes registrados.
- Actualizar información de clientes.

### Gestión de ventas
- Seleccionar cliente y empleado.
- Agregar productos al carrito.
- Establecer cantidades.
- Calcular subtotales y total de venta.
- Registrar encabezado y detalles de venta.
- Descontar automáticamente las existencias.
- Conservar el precio histórico de cada producto.
- Aplicar transacciones con COMMIT y ROLLBACK.

### Consultas e informes
El sistema incluye siete consultas:

1. Historial de ventas con total.
2. Compras realizadas por cliente.
3. Ventas por empleado superiores a Q10,000.
4. Productos más vendidos con cantidades superiores a 10.
5. Ingresos por categoría superiores a Q5,000.
6. Compras por cliente y categoría superiores a Q2,000.
7. Clientes cuyas compras acumuladas superan el promedio de ventas individuales.

## 5. Diseño de la base de datos

La base de datos se denomina `VentaTecnologia`.

Está compuesta por las siguientes tablas:

- Cliente
- Empleado
- Categoria
- Producto
- Venta
- DetalleVenta

Se implementaron:

- Llaves primarias (PK).
- Llaves foráneas (FK).
- Restricciones NOT NULL.
- Restricciones UNIQUE.
- Valores DEFAULT.
- Restricciones CHECK.
- Índices para optimizar consultas.

El diseño contempla la integridad referencial y la normalización hasta tercera forma normal (3FN).

## 6. Arquitectura del proyecto

El proyecto utiliza una estructura modular organizada en:

- `config`: configuración de conexión.
- `database`: conexión con SQL Server.
- `models`: modelos de las entidades.
- `repositories`: operaciones de acceso a datos.
- `services`: lógica de negocio.
- `interface`: ventanas y componentes gráficos.
- `tests`: pruebas y validaciones realizadas.

## 7. Requisitos

- Windows.
- Python 3.12.
- Microsoft SQL Server o SQL Server Express.
- Controlador ODBC para SQL Server.
- Entorno virtual de Python.

## 8. Instalación

Clonar el repositorio:

```bash
git clone URL_DEL_REPOSITORIO
```

Ingresar al directorio:

```bash
cd proyecto_final_2dosemestre2026_SGVT_DB1
```

Crear el entorno virtual:

```bash
python -m venv .venv
```

Activar el entorno virtual en Windows:

```bash
.venv\Scripts\activate
```

Instalar dependencias:

```bash
python -m pip install -r requirements.txt
```

## 9. Configuración de la base de datos

Crear la base de datos `VentaTecnologia` en SQL Server.

Configurar las credenciales de conexión en un archivo `.env` ubicado en la raíz del proyecto.

Las variables requeridas son:

```env
DB_SERVER=localhost\SQLEXPRESS
DB_PORT=
DB_NAME=VentaTecnologia
DB_USER=usuario
DB_PASSWORD=contraseña
DB_DRIVER=ODBC Driver 18 for SQL Server
DB_TRUST_SERVER_CERTIFICATE=yes
```

**Importante:** utilizar las credenciales correspondientes al entorno local. No publicar el archivo `.env` ni las contraseñas en GitHub.

## 10. Ejecución

Con el entorno virtual activado y la base de datos configurada, ejecutar:

```bash
python -m src.main
```

Se abrirá la interfaz principal del sistema, desde donde se podrá acceder a los módulos de Clientes, Ventas y Consultas.

## 11. Pruebas y validaciones

Durante el desarrollo se realizaron validaciones de:

- Configuración y conexión con SQL Server.
- Modelos de datos.
- Operaciones de repositorios.
- Registro y actualización de clientes.
- Consultas e informes.
- Integridad de inventario.
- Transacciones de ventas.
- Recuperación mediante ROLLBACK.

## 12. Autoría

Proyecto académico desarrollado para el curso de Base de Datos 1.

Universidad Mariano Gálvez de Guatemala.
