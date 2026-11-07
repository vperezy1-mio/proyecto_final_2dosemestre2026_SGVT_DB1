USE master;
GO

create database VentaTecnologia;

-- Crear el login si todavía no existe
IF SUSER_ID('venta_tecnologia_app') IS NULL
BEGIN
    CREATE LOGIN venta_tecnologia_app
    WITH PASSWORD = 'venta_2026';
END;
GO

USE VentaTecnologia;
GO

-- Crear el usuario de la base de datos
IF USER_ID('venta_tecnologia_app') IS NULL
BEGIN
    CREATE USER venta_tecnologia_app
    FOR LOGIN venta_tecnologia_app;
END;
GO

-- Crear el rol de la aplicación
IF DATABASE_PRINCIPAL_ID('app_crud') IS NULL
BEGIN
    CREATE ROLE app_crud;
END;
GO

-- Asignar el usuario al rol
ALTER ROLE app_crud
ADD MEMBER venta_tecnologia_app;
GO

-- Permisos de operaciones CRUD
GRANT SELECT, INSERT, UPDATE, DELETE
ON SCHEMA::dbo
TO app_crud;
GO

USE VentaTecnologia;
GO

CREATE TABLE dbo.Cliente (
    id_cliente INT IDENTITY(1,1),

    nombre VARCHAR(80) NOT NULL,
    apellido VARCHAR(80) NOT NULL,
    telefono VARCHAR(20) NULL,
    direccion VARCHAR(200) NULL,
    correo VARCHAR(150) NULL,

    CONSTRAINT PK_Cliente
        PRIMARY KEY (id_cliente)
);
GO

CREATE TABLE dbo.Empleado (
    id_empleado INT IDENTITY(1,1),

    nombre VARCHAR(80) NOT NULL,
    apellido VARCHAR(80) NOT NULL,
    telefono VARCHAR(20) NULL,
    direccion VARCHAR(200) NULL,

    fecha_ingreso DATE NOT NULL
        CONSTRAINT DF_Empleado_FechaIngreso
        DEFAULT (CONVERT(DATE, GETDATE())),

    CONSTRAINT PK_Empleado
        PRIMARY KEY (id_empleado)
);
GO

CREATE TABLE dbo.Categoria (
    id_categoria INT IDENTITY(1,1),

    nombre VARCHAR(100) NOT NULL,

    CONSTRAINT PK_Categoria
        PRIMARY KEY (id_categoria),

    CONSTRAINT UQ_Categoria_Nombre
        UNIQUE (nombre)
);
GO

CREATE TABLE dbo.Producto (
    id_producto INT IDENTITY(1,1),

    nombre VARCHAR(120) NOT NULL,
    precio DECIMAL(10,2) NOT NULL,
    stock INT NOT NULL
        CONSTRAINT DF_Producto_Stock DEFAULT (0),

    id_categoria INT NOT NULL,

    CONSTRAINT PK_Producto
        PRIMARY KEY (id_producto),

    CONSTRAINT FK_Producto_Categoria
        FOREIGN KEY (id_categoria)
        REFERENCES dbo.Categoria(id_categoria)
        ON DELETE NO ACTION,

    CONSTRAINT CK_Producto_Precio
        CHECK (precio >= 0),

    CONSTRAINT CK_Producto_Stock
        CHECK (stock >= 0)
);
GO

CREATE TABLE dbo.Venta (
    id_venta INT IDENTITY(1,1),

    fecha_venta DATETIME2(0) NOT NULL
        CONSTRAINT DF_Venta_Fecha
        DEFAULT (SYSDATETIME()),

    id_cliente INT NOT NULL,
    id_empleado INT NOT NULL,

    CONSTRAINT PK_Venta
        PRIMARY KEY (id_venta),

    CONSTRAINT FK_Venta_Cliente
        FOREIGN KEY (id_cliente)
        REFERENCES dbo.Cliente(id_cliente)
        ON DELETE NO ACTION,

    CONSTRAINT FK_Venta_Empleado
        FOREIGN KEY (id_empleado)
        REFERENCES dbo.Empleado(id_empleado)
        ON DELETE NO ACTION
);
GO

CREATE TABLE dbo.DetalleVenta (
    id_venta INT NOT NULL,
    id_producto INT NOT NULL,

    cantidad_venta INT NOT NULL,
    precio_venta DECIMAL(10,2) NOT NULL,

    CONSTRAINT PK_DetalleVenta
        PRIMARY KEY (id_venta, id_producto),

    CONSTRAINT FK_DetalleVenta_Venta
        FOREIGN KEY (id_venta)
        REFERENCES dbo.Venta(id_venta)
        ON DELETE NO ACTION,

    CONSTRAINT FK_DetalleVenta_Producto
        FOREIGN KEY (id_producto)
        REFERENCES dbo.Producto(id_producto)
        ON DELETE NO ACTION,

    CONSTRAINT CK_DetalleVenta_Cantidad
        CHECK (cantidad_venta > 0),

    CONSTRAINT CK_DetalleVenta_Precio
        CHECK (precio_venta >= 0)
);
GO

-- Buscar rápidamente las ventas de un cliente
CREATE INDEX IX_Venta_Cliente
ON dbo.Venta(id_cliente);
GO

-- Buscar rápidamente las ventas de un empleado
CREATE INDEX IX_Venta_Empleado
ON dbo.Venta(id_empleado);
GO

-- Consultar los productos pertenecientes a una categoría
CREATE INDEX IX_Producto_Categoria
ON dbo.Producto(id_categoria);
GO

-- Consultar las ventas en las que aparece un producto
CREATE INDEX IX_DetalleVenta_Producto
ON dbo.DetalleVenta(id_producto);
GO

CREATE UNIQUE INDEX UX_Cliente_Correo
ON dbo.Cliente(correo)
WHERE correo IS NOT NULL;
GO

USE VentaTecnologia;
GO

SELECT
    dp.name AS Usuario,
    rp.name AS Rol
FROM sys.database_role_members drm
INNER JOIN sys.database_principals rp
    ON drm.role_principal_id = rp.principal_id
INNER JOIN sys.database_principals dp
    ON drm.member_principal_id = dp.principal_id
WHERE dp.name = 'venta_tecnologia_app';
GO

ALTER ROLE app_crud
ADD MEMBER venta_tecnologia_app;
GO

GRANT SELECT, INSERT, UPDATE
ON SCHEMA::dbo
TO app_crud;
GO

REVOKE DELETE
ON SCHEMA::dbo
FROM app_crud;
GO

USE VentaTecnologia;
GO

SELECT
    dp.name AS Usuario,
    rp.name AS Rol
FROM sys.database_role_members drm
INNER JOIN sys.database_principals rp
    ON drm.role_principal_id = rp.principal_id
INNER JOIN sys.database_principals dp
    ON drm.member_principal_id = dp.principal_id
WHERE dp.name = 'venta_tecnologia_app';
GO

GRANT SELECT, INSERT, UPDATE
ON SCHEMA::dbo
TO app_crud;
GO

--consulta de tablas existentes
USE VentaTecnologia;
GO

SELECT
    TABLE_NAME
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_TYPE = 'BASE TABLE'
ORDER BY TABLE_NAME;
GO

--consulta de columna y tipos de datos y nulabilidad
SELECT
    TABLE_NAME,
    COLUMN_NAME,
    DATA_TYPE,
    IS_NULLABLE
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = 'dbo'
ORDER BY TABLE_NAME, ORDINAL_POSITION;
GO

--consulta de PK y FK
SELECT
    TABLE_NAME,
    CONSTRAINT_NAME,
    CONSTRAINT_TYPE
FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS
WHERE TABLE_SCHEMA = 'dbo'
ORDER BY TABLE_NAME, CONSTRAINT_TYPE;
GO

--consulta de indices
SELECT
    OBJECT_NAME(object_id) AS Tabla,
    name AS Indice,
    type_desc AS Tipo
FROM sys.indexes
WHERE object_id IN (
    OBJECT_ID('dbo.Cliente'),
    OBJECT_ID('dbo.Empleado'),
    OBJECT_ID('dbo.Categoria'),
    OBJECT_ID('dbo.Producto'),
    OBJECT_ID('dbo.Venta'),
    OBJECT_ID('dbo.DetalleVenta')
)
AND name IS NOT NULL
ORDER BY Tabla, Indice;
GO

SELECT
    id_venta,
    SUM(cantidad_venta * precio_venta) AS total_venta
FROM dbo.DetalleVenta
GROUP BY id_venta;


USE VentaTecnologia;
GO

SELECT
    TABLE_NAME AS Tabla,
    COLUMN_NAME AS Columna,
    DATA_TYPE AS TipoDato,
    CHARACTER_MAXIMUM_LENGTH AS Longitud,
    IS_NULLABLE AS PermiteNulos,
    COLUMN_DEFAULT AS ValorPredeterminado
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = 'dbo'
AND TABLE_NAME IN (
    'Cliente',
    'Empleado',
    'Categoria',
    'Producto',
    'Venta',
    'DetalleVenta'
)
ORDER BY TABLE_NAME, ORDINAL_POSITION;
GO

SELECT
    fk.name AS NombreRelacion,
    OBJECT_NAME(fk.parent_object_id) AS TablaOrigen,
    COL_NAME(
        fkc.parent_object_id,
        fkc.parent_column_id
    ) AS ColumnaOrigen,
    OBJECT_NAME(fk.referenced_object_id) AS TablaDestino,
    COL_NAME(
        fkc.referenced_object_id,
        fkc.referenced_column_id
    ) AS ColumnaDestino
FROM sys.foreign_keys fk
INNER JOIN sys.foreign_key_columns fkc
    ON fk.object_id = fkc.constraint_object_id
ORDER BY TablaOrigen;
GO




USE VentaTecnologia;
GO

SET XACT_ABORT ON;

BEGIN TRY
    BEGIN TRANSACTION;

    /* =========================================
       1. INSERTAR 4 EMPLEADOS
       ========================================= */

    INSERT INTO dbo.Empleado (nombre, apellido, telefono, direccion)
    SELECT datos.nombre, datos.apellido, datos.telefono, datos.direccion
    FROM (VALUES
        ('Luis', 'Gomez', '55551001', 'Zona 1'),
        ('Marta', 'Lopez', '55551002', 'Zona 7'),
        ('Carlos', 'Mendez', '55551003', 'Zona 10'),
        ('Ana', 'Morales', '55551004', 'Zona 12')
    ) AS datos(nombre, apellido, telefono, direccion)
    WHERE NOT EXISTS (
        SELECT 1
        FROM dbo.Empleado e
        WHERE e.nombre = datos.nombre
          AND e.apellido = datos.apellido
    );

    /* =========================================
       2. INSERTAR 5 CATEGORIAS
       ========================================= */

    INSERT INTO dbo.Categoria (nombre)
    SELECT datos.nombre
    FROM (VALUES
        ('Perifericos'),
        ('Componentes'),
        ('Computadoras'),
        ('Almacenamiento'),
        ('Pantallas')
    ) AS datos(nombre)
    WHERE NOT EXISTS (
        SELECT 1
        FROM dbo.Categoria c
        WHERE c.nombre = datos.nombre
    );

    /* =========================================
       3. INSERTAR 15 PRODUCTOS
       ========================================= */

    INSERT INTO dbo.Producto (nombre, precio, stock, id_categoria)
    SELECT
        datos.nombre,
        datos.precio,
        datos.stock,
        c.id_categoria
    FROM (VALUES
        ('Teclado mecanico', 450.00, 25, 'Perifericos'),
        ('Mouse inalambrico', 175.00, 40, 'Perifericos'),
        ('Audifonos', 325.00, 30, 'Perifericos'),
        ('Webcam HD', 275.00, 20, 'Perifericos'),

        ('Memoria RAM 16GB', 650.00, 20, 'Componentes'),
        ('Procesador Ryzen 5', 1450.00, 12, 'Componentes'),
        ('Tarjeta madre', 1100.00, 10, 'Componentes'),
        ('Fuente de poder', 550.00, 15, 'Componentes'),

        ('Laptop Lenovo', 6500.00, 8, 'Computadoras'),
        ('PC de escritorio', 5800.00, 6, 'Computadoras'),

        ('SSD 1TB', 850.00, 20, 'Almacenamiento'),
        ('Disco duro 2TB', 950.00, 15, 'Almacenamiento'),
        ('Memoria USB 128GB', 120.00, 50, 'Almacenamiento'),

        ('Monitor 24 pulgadas', 1250.00, 12, 'Pantallas'),
        ('Proyector multimedia', 3200.00, 5, 'Pantallas')
    ) AS datos(nombre, precio, stock, categoria)
    INNER JOIN dbo.Categoria c
        ON c.nombre = datos.categoria
    WHERE NOT EXISTS (
        SELECT 1
        FROM dbo.Producto p
        WHERE p.nombre = datos.nombre
    );

    /* =========================================
       4. INSERTAR 5 CLIENTES
       ========================================= */

    INSERT INTO dbo.Cliente
        (nombre, apellido, telefono, direccion, correo)
    SELECT
        datos.nombre,
        datos.apellido,
        datos.telefono,
        datos.direccion,
        datos.correo
    FROM (VALUES
        ('Ana', 'Perez', '55552001', 'Zona 4', 'ana.perez@example.com'),
        ('Carlos', 'Diaz', '55552002', 'Zona 5', 'carlos.diaz@example.com'),
        ('Sofia', 'Ramirez', '55552003', 'Zona 9', 'sofia.ramirez@example.com'),
        ('Diego', 'Castillo', '55552004', 'Zona 11', 'diego.castillo@example.com'),
        ('Laura', 'Mendez', '55552005', 'Zona 15', 'laura.mendez@example.com')
    ) AS datos(nombre, apellido, telefono, direccion, correo)
    WHERE NOT EXISTS (
        SELECT 1
        FROM dbo.Cliente cl
        WHERE cl.correo = datos.correo
    );

    COMMIT TRANSACTION;

    PRINT 'Datos iniciales insertados correctamente.';
END TRY
BEGIN CATCH
    IF @@TRANCOUNT > 0
        ROLLBACK TRANSACTION;

    THROW;
END CATCH;
GO

/* =========================================
   5. VERIFICAR LOS REGISTROS
   ========================================= */

SELECT 'Empleados' AS Tabla, COUNT(*) AS Total
FROM dbo.Empleado

UNION ALL

SELECT 'Categorias', COUNT(*)
FROM dbo.Categoria

UNION ALL

SELECT 'Productos', COUNT(*)
FROM dbo.Producto

UNION ALL

SELECT 'Clientes', COUNT(*)
FROM dbo.Cliente;
GO

/* Consultar los productos y sus categorias */

SELECT
    p.id_producto,
    p.nombre AS Producto,
    p.precio,
    p.stock,
    c.nombre AS Categoria
FROM dbo.Producto p
INNER JOIN dbo.Categoria c
    ON p.id_categoria = c.id_categoria
ORDER BY c.nombre, p.nombre;
GO


USE VentaTecnologia;
GO

SELECT 'Empleados' AS Tabla, COUNT(*) AS Total FROM dbo.Empleado
UNION ALL
SELECT 'Categorias', COUNT(*) FROM dbo.Categoria
UNION ALL
SELECT 'Productos', COUNT(*) FROM dbo.Producto
UNION ALL
SELECT 'Clientes', COUNT(*) FROM dbo.Cliente;
GO


USE VentaTecnologia;
GO

SET XACT_ABORT ON;

BEGIN TRY
    BEGIN TRANSACTION;

    -- Evitar duplicar las ventas de prueba.
    IF EXISTS (SELECT 1 FROM dbo.Venta)
    BEGIN
        ;THROW 50001, 'Ya existen ventas. No se insertaron ventas de prueba.', 1;
    END;

    DECLARE @id_venta INT;

    DECLARE @items TABLE (
        nombre_producto VARCHAR(120),
        cantidad INT
    );

    /* =========================================
       VENTA 1: ANA PEREZ - LUIS GOMEZ
       ========================================= */

    INSERT INTO dbo.Venta (id_cliente, id_empleado)
    SELECT c.id_cliente, e.id_empleado
    FROM dbo.Cliente c
    CROSS JOIN dbo.Empleado e
    WHERE c.correo = 'ana.perez@example.com'
      AND e.nombre = 'Luis'
      AND e.apellido = 'Gomez';

    SET @id_venta = SCOPE_IDENTITY();

    DELETE FROM @items;
    INSERT INTO @items VALUES
        ('Laptop Lenovo', 2),
        ('Mouse inalambrico', 3);

    IF EXISTS (
        SELECT 1
        FROM @items i
        JOIN dbo.Producto p ON p.nombre = i.nombre_producto
        WHERE p.stock < i.cantidad
    )
        THROW 50002, 'Stock insuficiente en venta 1.', 1;

    INSERT INTO dbo.DetalleVenta
        (id_venta, id_producto, cantidad_venta, precio_venta)
    SELECT @id_venta, p.id_producto, i.cantidad, p.precio
    FROM @items i
    JOIN dbo.Producto p ON p.nombre = i.nombre_producto;

    UPDATE p
    SET p.stock = p.stock - i.cantidad
    FROM dbo.Producto p
    JOIN @items i ON i.nombre_producto = p.nombre;

    /* =========================================
       VENTA 2: CARLOS DIAZ - MARTA LOPEZ
       ========================================= */

    INSERT INTO dbo.Venta (id_cliente, id_empleado)
    SELECT c.id_cliente, e.id_empleado
    FROM dbo.Cliente c
    CROSS JOIN dbo.Empleado e
    WHERE c.correo = 'carlos.diaz@example.com'
      AND e.nombre = 'Marta'
      AND e.apellido = 'Lopez';

    SET @id_venta = SCOPE_IDENTITY();

    DELETE FROM @items;
    INSERT INTO @items VALUES
        ('PC de escritorio', 2),
        ('Monitor 24 pulgadas', 2);

    IF EXISTS (
        SELECT 1
        FROM @items i
        JOIN dbo.Producto p ON p.nombre = i.nombre_producto
        WHERE p.stock < i.cantidad
    )
        THROW 50003, 'Stock insuficiente en venta 2.', 1;

    INSERT INTO dbo.DetalleVenta
        (id_venta, id_producto, cantidad_venta, precio_venta)
    SELECT @id_venta, p.id_producto, i.cantidad, p.precio
    FROM @items i
    JOIN dbo.Producto p ON p.nombre = i.nombre_producto;

    UPDATE p
    SET p.stock = p.stock - i.cantidad
    FROM dbo.Producto p
    JOIN @items i ON i.nombre_producto = p.nombre;

    /* =========================================
       VENTA 3: SOFIA RAMIREZ - CARLOS MENDEZ
       ========================================= */

    INSERT INTO dbo.Venta (id_cliente, id_empleado)
    SELECT c.id_cliente, e.id_empleado
    FROM dbo.Cliente c
    CROSS JOIN dbo.Empleado e
    WHERE c.correo = 'sofia.ramirez@example.com'
      AND e.nombre = 'Carlos'
      AND e.apellido = 'Mendez';

    SET @id_venta = SCOPE_IDENTITY();

    DELETE FROM @items;
    INSERT INTO @items VALUES
        ('Proyector multimedia', 2),
        ('SSD 1TB', 4);

    IF EXISTS (
        SELECT 1
        FROM @items i
        JOIN dbo.Producto p ON p.nombre = i.nombre_producto
        WHERE p.stock < i.cantidad
    )
        THROW 50004, 'Stock insuficiente en venta 3.', 1;

    INSERT INTO dbo.DetalleVenta
        (id_venta, id_producto, cantidad_venta, precio_venta)
    SELECT @id_venta, p.id_producto, i.cantidad, p.precio
    FROM @items i
    JOIN dbo.Producto p ON p.nombre = i.nombre_producto;

    UPDATE p
    SET p.stock = p.stock - i.cantidad
    FROM dbo.Producto p
    JOIN @items i ON i.nombre_producto = p.nombre;

    /* =========================================
       VENTA 4: DIEGO CASTILLO - ANA MORALES
       ========================================= */

    INSERT INTO dbo.Venta (id_cliente, id_empleado)
    SELECT c.id_cliente, e.id_empleado
    FROM dbo.Cliente c
    CROSS JOIN dbo.Empleado e
    WHERE c.correo = 'diego.castillo@example.com'
      AND e.nombre = 'Ana'
      AND e.apellido = 'Morales';

    SET @id_venta = SCOPE_IDENTITY();

    DELETE FROM @items;
    INSERT INTO @items VALUES
        ('Memoria RAM 16GB', 12),
        ('Memoria USB 128GB', 15);

    IF EXISTS (
        SELECT 1
        FROM @items i
        JOIN dbo.Producto p ON p.nombre = i.nombre_producto
        WHERE p.stock < i.cantidad
    )
        THROW 50005, 'Stock insuficiente en venta 4.', 1;

    INSERT INTO dbo.DetalleVenta
        (id_venta, id_producto, cantidad_venta, precio_venta)
    SELECT @id_venta, p.id_producto, i.cantidad, p.precio
    FROM @items i
    JOIN dbo.Producto p ON p.nombre = i.nombre_producto;

    UPDATE p
    SET p.stock = p.stock - i.cantidad
    FROM dbo.Producto p
    JOIN @items i ON i.nombre_producto = p.nombre;

    /* =========================================
       VENTA 5: ANA PEREZ - LUIS GOMEZ
       ========================================= */

    INSERT INTO dbo.Venta (id_cliente, id_empleado)
    SELECT c.id_cliente, e.id_empleado
    FROM dbo.Cliente c
    CROSS JOIN dbo.Empleado e
    WHERE c.correo = 'ana.perez@example.com'
      AND e.nombre = 'Luis'
      AND e.apellido = 'Gomez';

    SET @id_venta = SCOPE_IDENTITY();

    DELETE FROM @items;
    INSERT INTO @items VALUES
        ('Procesador Ryzen 5', 3),
        ('Tarjeta madre', 2),
        ('Fuente de poder', 3);

    IF EXISTS (
        SELECT 1
        FROM @items i
        JOIN dbo.Producto p ON p.nombre = i.nombre_producto
        WHERE p.stock < i.cantidad
    )
        THROW 50006, 'Stock insuficiente en venta 5.', 1;

    INSERT INTO dbo.DetalleVenta
        (id_venta, id_producto, cantidad_venta, precio_venta)
    SELECT @id_venta, p.id_producto, i.cantidad, p.precio
    FROM @items i
    JOIN dbo.Producto p ON p.nombre = i.nombre_producto;

    UPDATE p
    SET p.stock = p.stock - i.cantidad
    FROM dbo.Producto p
    JOIN @items i ON i.nombre_producto = p.nombre;

    /* =========================================
       VENTA 6: ANA PEREZ - MARTA LOPEZ
       ========================================= */

    INSERT INTO dbo.Venta (id_cliente, id_empleado)
    SELECT c.id_cliente, e.id_empleado
    FROM dbo.Cliente c
    CROSS JOIN dbo.Empleado e
    WHERE c.correo = 'ana.perez@example.com'
      AND e.nombre = 'Marta'
      AND e.apellido = 'Lopez';

    SET @id_venta = SCOPE_IDENTITY();

    DELETE FROM @items;
    INSERT INTO @items VALUES
        ('Laptop Lenovo', 1),
        ('SSD 1TB', 2);

    IF EXISTS (
        SELECT 1
        FROM @items i
        JOIN dbo.Producto p ON p.nombre = i.nombre_producto
        WHERE p.stock < i.cantidad
    )
        THROW 50007, 'Stock insuficiente en venta 6.', 1;

    INSERT INTO dbo.DetalleVenta
        (id_venta, id_producto, cantidad_venta, precio_venta)
    SELECT @id_venta, p.id_producto, i.cantidad, p.precio
    FROM @items i
    JOIN dbo.Producto p ON p.nombre = i.nombre_producto;

    UPDATE p
    SET p.stock = p.stock - i.cantidad
    FROM dbo.Producto p
    JOIN @items i ON i.nombre_producto = p.nombre;

    COMMIT TRANSACTION;

    PRINT 'Se registraron correctamente las seis ventas.';

END TRY
BEGIN CATCH

    IF @@TRANCOUNT > 0
        ROLLBACK TRANSACTION;

    THROW;

END CATCH;
GO


SELECT
    v.id_venta,
    v.fecha_venta,
    c.nombre + ' ' + c.apellido AS Cliente,
    e.nombre + ' ' + e.apellido AS Empleado,
    SUM(d.cantidad_venta * d.precio_venta) AS TotalVenta
FROM dbo.Venta v
INNER JOIN dbo.Cliente c
    ON v.id_cliente = c.id_cliente
INNER JOIN dbo.Empleado e
    ON v.id_empleado = e.id_empleado
INNER JOIN dbo.DetalleVenta d
    ON v.id_venta = d.id_venta
GROUP BY
    v.id_venta,
    v.fecha_venta,
    c.nombre,
    c.apellido,
    e.nombre,
    e.apellido
ORDER BY v.id_venta;

SELECT
    v.id_venta,
    c.nombre + ' ' + c.apellido AS Cliente,
    p.nombre AS Producto,
    d.cantidad_venta AS Cantidad,
    d.precio_venta AS PrecioUnitario,
    d.cantidad_venta * d.precio_venta AS Subtotal
FROM dbo.Venta v
INNER JOIN dbo.Cliente c
    ON v.id_cliente = c.id_cliente
INNER JOIN dbo.DetalleVenta d
    ON v.id_venta = d.id_venta
INNER JOIN dbo.Producto p
    ON d.id_producto = p.id_producto
ORDER BY v.id_venta, p.nombre;






USE VentaTecnologia;
GO

/* =====================================================
   CONSULTA 1. HISTORIAL DE VENTAS CON IMPORTE TOTAL
   ===================================================== */

SELECT
    v.id_venta,
    v.fecha_venta,
    c.nombre + ' ' + c.apellido AS Cliente,
    e.nombre + ' ' + e.apellido AS Empleado,
    SUM(d.cantidad_venta * d.precio_venta) AS TotalVenta
FROM dbo.Venta v
INNER JOIN dbo.Cliente c
    ON v.id_cliente = c.id_cliente
INNER JOIN dbo.Empleado e
    ON v.id_empleado = e.id_empleado
INNER JOIN dbo.DetalleVenta d
    ON v.id_venta = d.id_venta
GROUP BY
    v.id_venta,
    v.fecha_venta,
    c.nombre,
    c.apellido,
    e.nombre,
    e.apellido
ORDER BY v.id_venta;


/* =====================================================
   CONSULTA 2. COMPRAS REALIZADAS POR CLIENTE
   ===================================================== */

SELECT
    c.id_cliente,
    c.nombre + ' ' + c.apellido AS Cliente,
    v.id_venta,
    v.fecha_venta,
    p.nombre AS Producto,
    d.cantidad_venta AS Cantidad,
    d.precio_venta AS PrecioUnitario,
    d.cantidad_venta * d.precio_venta AS Subtotal
FROM dbo.Cliente c
INNER JOIN dbo.Venta v
    ON c.id_cliente = v.id_cliente
INNER JOIN dbo.DetalleVenta d
    ON v.id_venta = d.id_venta
INNER JOIN dbo.Producto p
    ON d.id_producto = p.id_producto
ORDER BY c.id_cliente, v.id_venta;


/* =====================================================
   CONSULTA 3. VENTAS POR EMPLEADO SUPERIORES A Q10,000
   ===================================================== */

SELECT
    e.id_empleado,
    e.nombre + ' ' + e.apellido AS Empleado,
    COUNT(DISTINCT v.id_venta) AS CantidadVentas,
    SUM(d.cantidad_venta * d.precio_venta) AS TotalVentas
FROM dbo.Empleado e
INNER JOIN dbo.Venta v
    ON e.id_empleado = v.id_empleado
INNER JOIN dbo.DetalleVenta d
    ON v.id_venta = d.id_venta
GROUP BY
    e.id_empleado,
    e.nombre,
    e.apellido
HAVING SUM(d.cantidad_venta * d.precio_venta) > 10000
ORDER BY TotalVentas DESC;


/* =====================================================
   CONSULTA 4. PRODUCTOS MAS VENDIDOS
   CANTIDAD TOTAL SUPERIOR A 10
   ===================================================== */

SELECT
    p.id_producto,
    p.nombre AS Producto,
    SUM(d.cantidad_venta) AS UnidadesVendidas
FROM dbo.Producto p
INNER JOIN dbo.DetalleVenta d
    ON p.id_producto = d.id_producto
GROUP BY
    p.id_producto,
    p.nombre
HAVING SUM(d.cantidad_venta) > 10
ORDER BY UnidadesVendidas DESC;


/* =====================================================
   CONSULTA 5. INGRESOS POR CATEGORIA SUPERIORES A Q5,000
   ===================================================== */

SELECT
    c.id_categoria,
    c.nombre AS Categoria,
    SUM(d.cantidad_venta * d.precio_venta) AS Ingresos
FROM dbo.Categoria c
INNER JOIN dbo.Producto p
    ON c.id_categoria = p.id_categoria
INNER JOIN dbo.DetalleVenta d
    ON p.id_producto = d.id_producto
GROUP BY
    c.id_categoria,
    c.nombre
HAVING SUM(d.cantidad_venta * d.precio_venta) > 5000
ORDER BY Ingresos DESC;


/* =====================================================
   CONSULTA 6. REPORTE CLIENTE - CATEGORIA
   IMPORTES SUPERIORES A Q2,000
   ===================================================== */

SELECT
    c.id_cliente,
    c.nombre + ' ' + c.apellido AS Cliente,
    cat.nombre AS Categoria,
    SUM(d.cantidad_venta * d.precio_venta) AS ImporteComprado
FROM dbo.Cliente c
INNER JOIN dbo.Venta v
    ON c.id_cliente = v.id_cliente
INNER JOIN dbo.DetalleVenta d
    ON v.id_venta = d.id_venta
INNER JOIN dbo.Producto p
    ON d.id_producto = p.id_producto
INNER JOIN dbo.Categoria cat
    ON p.id_categoria = cat.id_categoria
GROUP BY
    c.id_cliente,
    c.nombre,
    c.apellido,
    cat.id_categoria,
    cat.nombre
HAVING SUM(d.cantidad_venta * d.precio_venta) > 2000
ORDER BY Cliente, ImporteComprado DESC;


/* =====================================================
   CONSULTA 7. CLIENTES CUYAS COMPRAS ACUMULADAS
   SUPERAN EL PROMEDIO DE LOS IMPORTES DE VENTAS
   ===================================================== */

WITH TotalesPorVenta AS (
    SELECT
        v.id_venta,
        v.id_cliente,
        SUM(d.cantidad_venta * d.precio_venta) AS TotalVenta
    FROM dbo.Venta v
    INNER JOIN dbo.DetalleVenta d
        ON v.id_venta = d.id_venta
    GROUP BY
        v.id_venta,
        v.id_cliente
),
PromedioVentas AS (
    SELECT AVG(TotalVenta) AS Promedio
    FROM TotalesPorVenta
)
SELECT
    c.id_cliente,
    c.nombre + ' ' + c.apellido AS Cliente,
    SUM(tv.TotalVenta) AS ComprasAcumuladas,
    pv.Promedio AS PromedioVentaIndividual
FROM dbo.Cliente c
INNER JOIN TotalesPorVenta tv
    ON c.id_cliente = tv.id_cliente
CROSS JOIN PromedioVentas pv
GROUP BY
    c.id_cliente,
    c.nombre,
    c.apellido,
    pv.Promedio
HAVING SUM(tv.TotalVenta) > pv.Promedio
ORDER BY ComprasAcumuladas DESC;
GO


USE VentaTecnologia;
GO

SELECT
    t.name AS Tabla,
    i.name AS Indice,
    i.type_desc AS TipoIndice,
    i.is_primary_key AS EsClavePrimaria,
    i.is_unique AS EsUnico
FROM sys.indexes i
INNER JOIN sys.tables t
    ON i.object_id = t.object_id
WHERE t.name IN (
    'Cliente',
    'Empleado',
    'Categoria',
    'Producto',
    'Venta',
    'DetalleVenta'
)
AND i.name IS NOT NULL
ORDER BY t.name, i.name;
GO


USE VentaTecnologia;
GO

SELECT
    t.name AS Tabla,
    cc.name AS Restriccion,
    'CHECK' AS Tipo,
    cc.definition AS Definicion,
    cc.is_disabled AS Deshabilitada
FROM sys.check_constraints cc
INNER JOIN sys.tables t
    ON cc.parent_object_id = t.object_id

UNION ALL

SELECT
    t.name,
    kc.name,
    kc.type_desc,
    NULL,
    NULL
FROM sys.key_constraints kc
INNER JOIN sys.tables t
    ON kc.parent_object_id = t.object_id
ORDER BY Tabla, Restriccion;
GO


USE VentaTecnologia;
GO

SELECT
    USER_NAME(dp.grantee_principal_id) AS Usuario,
    dp.permission_name AS Permiso,
    dp.state_desc AS Estado,
    dp.class_desc AS Ambito
FROM sys.database_permissions dp
WHERE USER_NAME(dp.grantee_principal_id)
      IN ('app_crud', 'venta_tecnologia_app')
ORDER BY Usuario, Permiso;
GO

SELECT
    r.name AS Rol,
    m.name AS Miembro
FROM sys.database_role_members drm
INNER JOIN sys.database_principals r
    ON drm.role_principal_id = r.principal_id
INNER JOIN sys.database_principals m
    ON drm.member_principal_id = m.principal_id
WHERE m.name = 'venta_tecnologia_app';
GO



SELECT
    V.id_venta,
    V.fecha_venta,
    C.nombre AS cliente,
    E.nombre AS empleado,
    P.nombre AS producto,
    DV.cantidad_venta,
    DV.precio_venta,
    DV.cantidad_venta * DV.precio_venta AS subtotal
FROM Venta V
INNER JOIN Cliente C
    ON V.id_cliente = C.id_cliente
INNER JOIN Empleado E
    ON V.id_empleado = E.id_empleado
INNER JOIN DetalleVenta DV
    ON V.id_venta = DV.id_venta
INNER JOIN Producto P
    ON DV.id_producto = P.id_producto
ORDER BY V.id_venta DESC;