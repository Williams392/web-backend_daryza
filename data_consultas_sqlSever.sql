------------------------------------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------CONSULTAS, SUBCONSULTAS Y PROCESOS ALMACENADOS----------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------TABLA ROL---------------------------
---CONSULTA
SELECT * FROM tb_rol;

----SUBCONSULTA
SELECT u.username, u.email, (SELECT r.name_role FROM tb_rol r WHERE r.id_rol = u.name_role) AS role_name
FROM tb_usuario u;

---PROCESO ALMACENADO
GO
CREATE PROCEDURE InsertarRol
    @name_role NVARCHAR(50)
AS
BEGIN
    
    IF EXISTS (SELECT 1 FROM tb_rol WHERE name_role = @name_role)
    BEGIN
        PRINT 'El rol ya existe en la base de datos.'
    END
    ELSE
    BEGIN
      
        INSERT INTO tb_rol (name_role) 
        VALUES (@name_role);
        
        PRINT 'Rol insertado correctamente.'
    END
END;

EXEC InsertarRol @name_role = 'Administrador';
--------------------------------------------------------------------------
--------------------------------------------TABLA USUARIO
---CONSULTA
SELECT u.username, u.email, r.name_role
FROM tb_usuario u
JOIN tb_rol r ON u.name_role = r.id_rol;

---SUBCONSULTA 
SELECT username, email
FROM tb_usuario
WHERE name_role = (SELECT id_rol FROM tb_rol WHERE name_role = 'Administrador');

---PROCESO ALMACENADO
GO
CREATE PROCEDURE InsertarUsuario
    @username NVARCHAR(50),
    @password NVARCHAR(128),
    @email NVARCHAR(150),
    @phone_number NVARCHAR(15),
    @name_role INT,
    @first_name NVARCHAR(50),
    @last_name NVARCHAR(50)
AS
BEGIN
    
    IF EXISTS (SELECT 1 FROM tb_usuario WHERE username = @username)
    BEGIN
        PRINT 'El usuario ya existe en la base de datos.'
    END
    ELSE
    BEGIN
        
        INSERT INTO tb_usuario (username, password, email, phone_number, name_role, first_name, last_name)
        VALUES (@username, HASHBYTES('SHA2_256', @password), @email, @phone_number, @name_role, @first_name, @last_name);

        PRINT 'Usuario insertado correctamente.'
    END
END;
EXEC InsertarUsuario 
    @username = 'juanperez', 
    @password = 'claveSegura123', 
    @email = 'juan.perez@email.com', 
    @phone_number = '1234567890', 
    @name_role = 1, 
    @first_name = 'Juan', 
    @last_name = 'Perez';


--------------------------------------------------------------------------
---------------------------------------------TABLA CATEGORIA
---CONSULTA
SELECT * FROM tb_categoria WHERE estado_categoria = 1;

---SUBCONSULTA 
SELECT c.nombre_categoria, (SELECT COUNT(*) FROM tb_producto p WHERE p.categoria = c.id_categoria) AS cantidad_productos
FROM tb_categoria c;

---PROCESO ALMACENADO
GO
CREATE PROCEDURE InsertarCategoria
    @nombre_categoria NVARCHAR(100),
    @estado_categoria BIT
AS
BEGIN
   
    IF EXISTS (SELECT 1 FROM tb_categoria WHERE nombre_categoria = @nombre_categoria)
    BEGIN
        PRINT 'La categoría ya existe en la base de datos.'
    END
    ELSE
    BEGIN
        
        INSERT INTO tb_categoria (nombre_categoria, estado_categoria)
        VALUES (@nombre_categoria, @estado_categoria);

        PRINT 'Categoría insertada correctamente.'
    END
END;
EXEC InsertarCategoria 
    @nombre_categoria = 'Electrónica', 
    @estado_categoria = 1;

--------------------------------------------------------------------------
-------------------------------------------------TABLA MARCA
---CONSULTA
SELECT * FROM tb_marca WHERE estado_marca = 1;

---SUBCONSULTA 
SELECT p.nombre_prod, (SELECT m.nombre_marca FROM tb_marca m WHERE m.id_marca = p.marca) AS marca
FROM tb_producto p;

---PROCESO ALMACENADO
GO
CREATE PROCEDURE InsertarMarca
    @nombre_marca NVARCHAR(100),
    @estado_marca BIT
AS
BEGIN
    
    IF EXISTS (SELECT 1 FROM tb_marca WHERE nombre_marca = @nombre_marca)
    BEGIN
        PRINT 'La marca ya existe en la base de datos.'
    END
    ELSE
    BEGIN
        
        INSERT INTO tb_marca (nombre_marca, estado_marca)
        VALUES (@nombre_marca, @estado_marca);

        PRINT 'Marca insertada correctamente.'
    END
END;
EXEC InsertarMarca 
    @nombre_marca = 'Samsung', 
    @estado_marca = 1;

--------------------------------------------------------------------------
----------------------------------------------TABLA UNIDAD DE MEDIDA
---CONSULTA
SELECT * FROM tb_unidadMedida;

---SUBCONSULTA 
SELECT p.nombre_prod, (SELECT u.abreviacion FROM tb_unidadMedida u WHERE u.id_unidadMedida = p.unidad_medida) AS unidad
FROM tb_producto p;

---PROCESO ALMACENADO
GO
CREATE PROCEDURE InsertarUnidadMedida
    @nombre_unidad NVARCHAR(100),
    @abreviacion NVARCHAR(100)
AS
BEGIN
    -- Verificar si la unidad de medida ya existe
    IF EXISTS (SELECT 1 FROM tb_unidadMedida WHERE nombre_unidad = @nombre_unidad)
    BEGIN
        PRINT 'La unidad de medida ya existe en la base de datos.'
    END
    ELSE
    BEGIN
        -- Insertar la nueva unidad de medida
        INSERT INTO tb_unidadMedida (nombre_unidad, abreviacion)
        VALUES (@nombre_unidad, @abreviacion);

        PRINT 'Unidad de medida insertada correctamente.'
    END
END;
EXEC InsertarUnidadMedida 
    @nombre_unidad = 'Kilogramo', 
    @abreviacion = 'kg';

--------------------------------------------------------------------------
-------------------------------------------------------TABLA PRODUCTO
---CONSULTA
SELECT p.nombre_prod, p.precio_venta, c.nombre_categoria, m.nombre_marca
FROM tb_producto p
JOIN tb_categoria c ON p.categoria = c.id_categoria
JOIN tb_marca m ON p.marca = m.id_marca;

---SUBCONSULTA 
SELECT nombre_prod, precio_venta
FROM tb_producto
WHERE precio_venta = (SELECT MAX(precio_venta) FROM tb_producto WHERE categoria = tb_producto.categoria);

---PROCESO ALMACENADO
GO
CREATE PROCEDURE InsertarProducto
    @nombre_prod NVARCHAR(100),
    @descripcion_pro NVARCHAR(MAX),
    @precio_compra DECIMAL(10, 2),
    @precio_venta DECIMAL(10, 2),
    @codigo NVARCHAR(100),
    @estado BIT,
    @estock INT,
    @estock_minimo INT,
    @marca INT,
    @categoria INT,
    @unidad_medida INT
AS
BEGIN
    -- Verificar si el código del producto ya existe
    IF EXISTS (SELECT 1 FROM tb_producto WHERE codigo = @codigo)
    BEGIN
        PRINT 'El producto con el código proporcionado ya existe en la base de datos.'
    END
    ELSE
    BEGIN
        -- Insertar el nuevo producto
        INSERT INTO tb_producto (nombre_prod, descripcion_pro, precio_compra, precio_venta, codigo, estado, estock, estock_minimo, marca, categoria, unidad_medida)
        VALUES (@nombre_prod, @descripcion_pro, @precio_compra, @precio_venta, @codigo, @estado, @estock, @estock_minimo, @marca, @categoria, @unidad_medida);

        PRINT 'Producto insertado correctamente.'
    END
END;
EXEC InsertarProducto 
    @nombre_prod = 'Producto A', 
    @descripcion_pro = 'Descripción del producto A',
    @precio_compra = 100.50, 
    @precio_venta = 150.75, 
    @codigo = 'PROD001',
    @estado = 1, 
    @estock = 50, 
    @estock_minimo = 10, 
    @marca = 1, 
    @categoria = 2, 
    @unidad_medida = 3;

--------------------------------------------------------------------------
-----------------------------------------------------------TABLA CLIENTE
---CONSULTA
SELECT * FROM tb_cliente;

---SUBCONSULTA 
SELECT nombre_clie, apellido_clie
FROM tb_cliente
WHERE tipo_empresa = 'Natural';

---PROCESO ALMACENADO
GO
CREATE PROCEDURE InsertarCliente
    @nombre_clie NVARCHAR(255),
    @apellido_clie NVARCHAR(255),
    @direccion_clie NVARCHAR(255),
    @dni_cliente NVARCHAR(8),
    @ruc_cliente NVARCHAR(11),
    @tipo_empresa NVARCHAR(255),
    @email_cliente NVARCHAR(50),
    @telefono_cliente NVARCHAR(20)
AS
BEGIN
    -- Verificar si ya existe un cliente con el mismo DNI o RUC
    IF EXISTS (SELECT 1 FROM tb_cliente WHERE dni_cliente = @dni_cliente OR ruc_cliente = @ruc_cliente)
    BEGIN
        PRINT 'Ya existe un cliente con el DNI o RUC proporcionado.'
    END
    ELSE
    BEGIN
        -- Insertar el nuevo cliente
        INSERT INTO tb_cliente (nombre_clie, apellido_clie, direccion_clie, dni_cliente, ruc_cliente, tipo_empresa, email_cliente, telefono_cliente)
        VALUES (@nombre_clie, @apellido_clie, @direccion_clie, @dni_cliente, @ruc_cliente, @tipo_empresa, @email_cliente, @telefono_cliente);

        PRINT 'Cliente insertado correctamente.'
    END
END;
EXEC InsertarCliente 
    @nombre_clie = 'Juan', 
    @apellido_clie = 'Perez', 
    @direccion_clie = 'Av. Siempre Viva 123', 
    @dni_cliente = '12345678', 
    @ruc_cliente = '12345678901', 
    @tipo_empresa = 'Persona Natural', 
    @email_cliente = 'juan.perez@example.com', 
    @telefono_cliente = '987654321';

--------------------------------------------------------------------------
---------------------------------------------TABLA DETALLE_COMPROBANTE
---CONSULTA
SELECT * FROM tb_detalle_comprobante;

---SUBCONSULTA 
SELECT c.id_comprobante, 
       COALESCE(dc.total_productos, 0) AS total_productos
FROM tb_comprobante AS c
LEFT JOIN (
    SELECT id_comprobante, SUM(cantidad) AS total_productos
    FROM tb_detalle_comprobante
    GROUP BY id_comprobante
) dc ON c.id_comprobante = dc.id_comprobante;

---PROCESO ALMACENADO

GO
CREATE PROCEDURE InsertarDetalleComprobantee
    @unidad NVARCHAR(6),
    @cantidad INT,
    @id_producto NVARCHAR(10),
    @descripcion NVARCHAR(255),
    @monto_valorUnitario FLOAT = 0,
    @igv_detalle FLOAT = 0,
    @monto_Precio_Unitario DECIMAL(10, 2) = 0,
    @monto_Valor_Venta DECIMAL(10, 2) = 0,
    @comprobante INT = NULL,
    @producto INT = NULL
AS
BEGIN
    BEGIN TRY
        BEGIN TRANSACTION;

        -- Verificar que la cantidad no sea negativa
        IF @cantidad < 0
        BEGIN
            RAISERROR('La cantidad no puede ser negativa.', 16, 1);
            ROLLBACK TRANSACTION;
            RETURN;
        END

        -- Verificar que el producto existe en tb_producto
        IF NOT EXISTS (SELECT 1 FROM dbo.tb_producto WHERE id_producto = @producto)
        BEGIN
            RAISERROR('El producto especificado no existe en la tabla tb_producto.', 16, 1);
            ROLLBACK TRANSACTION;
            RETURN;
        END

        -- Realizar la inserción
        INSERT INTO dbo.tb_detalle_comprobante (unidad, cantidad, id_producto, descripcion, monto_valorUnitario, igv_detalle, monto_Precio_Unitario, monto_Valor_Venta, comprobante, producto)
        VALUES (@unidad, @cantidad, @id_producto, @descripcion, @monto_valorUnitario, @igv_detalle, @monto_Precio_Unitario, @monto_Valor_Venta, @comprobante, @producto);

        COMMIT TRANSACTION;

        -- Mensaje de éxito
        SELECT 'El detalle del comprobante se ha insertado correctamente.' AS Mensaje;

    END TRY
    BEGIN CATCH
        ROLLBACK TRANSACTION;

        DECLARE @ErrorMessage NVARCHAR(4000) = ERROR_MESSAGE();
        DECLARE @ErrorNumber INT = ERROR_NUMBER();
        DECLARE @ErrorLine INT = ERROR_LINE();
        
        RAISERROR('Error al insertar el detalle del comprobante. Número de error: %d, Línea: %d, Mensaje: %s', 
                  16, 1, @ErrorNumber, @ErrorLine, @ErrorMessage);
    END CATCH
END;


EXEC InsertarDetalleComprobante 
    @unidad = 'UND',
    @cantidad = 5,
    @id_producto = 'PROD123',
    @descripcion = 'Producto de limpieza',
    @monto_valorUnitario = 12.50,
    @igv_detalle = 2.25,
    @monto_Precio_Unitario = 14.75,
    @monto_Valor_Venta = 73.75,
    @comprobante = 4,
    @producto = 1; 