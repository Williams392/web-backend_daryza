create table AUDITORIA ( -- NUEVA TABLA:
	CODIGO_AU INT IDENTITY(1,1) PRIMARY KEY,
	USUARIO_AU VARCHAR(50) NOT NULL,
	TABLA VARCHAR(50) NOT NULL,
	ACCION VARCHAR(20) NOT NULL,
	REGISTRO VARCHAR(20) NOT NULL,
	NOMBRE VARCHAR(100) NOT NULL,
	DESCRIPCION VARCHAR(50),
	FECHA_HORA DATETIME NOT NULL
);
GO

-----------------------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------- TRIGGER ROL ---------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------------


-- TRIGGER INSERTAR PARA tb_producto
CREATE TRIGGER TR_AuditoriaP_Insertar
ON tb_producto
FOR INSERT
AS
BEGIN
    INSERT INTO AUDITORIA 
    SELECT 'DESCONOCIDO', 'PRODUCTO', 'INSERTÓ', 
           CONVERT(NVARCHAR(12), id_producto), 
           nombre_prod, 
           'NINGUNA', 
           GETDATE()
    FROM inserted;
END;
GO

INSERT INTO tb_producto (nombre_prod, descripcion_pro, precio_compra, precio_venta, codigo, estado, estock, estock_minimo, marca_id, categoria_id, unidad_medida_id, created_at, update_at)
VALUES ('Producto C', 'Descripción del Producto A', 10.00, 15.00, 'P001', 1, 100, 10, 1, 1, 1,  GETDATE(),  GETDATE());
GO

SELECT * FROM tb_producto;
SELECT * FROM AUDITORIA;
GO

-------------------------------------

-- TRIGGER ELIMINAR PARA tb_producto
CREATE TRIGGER TR_AuditoriaP_Eliminar
ON tb_producto
FOR DELETE
AS
BEGIN
    INSERT INTO AUDITORIA 
    SELECT 'DESCONOCIDO', 'PRODUCTO', 'ELIMINÓ', 
           CONVERT(NVARCHAR(12), id_producto), 
           nombre_prod, 
           'NINGUNA', 
           GETDATE()
    FROM deleted;
END;
GO

DELETE FROM tb_producto
WHERE id_producto = 2;  
GO

SELECT * FROM tb_producto;
SELECT * FROM AUDITORIA;
GO

-------------------------------------

-- TRIGGER ACTUALIZAR PARA tb_producto
CREATE TRIGGER TR_AuditoriaP_Actualizar
ON tb_producto
FOR UPDATE
AS
BEGIN
    INSERT INTO AUDITORIA 
    SELECT 'DESCONOCIDO', 'PRODUCTO', 'ACTUALIZÓ', 
           CONVERT(NVARCHAR(12), id_producto), 
           nombre_prod, 
           (SELECT nombre_prod FROM deleted), 
           GETDATE()
    FROM inserted;
END;
GO

UPDATE tb_producto
SET nombre_prod = 'Producto A Actualizado'
WHERE id_producto = 3; 
GO

-- Verificar auditoría
SELECT * FROM tb_producto;
SELECT * FROM AUDITORIA;

-----------------------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------- TRIGGER ROL ---------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------------
use BD_DARYZA_DJANGO;
GO

-- TRIGGER INSERTAR PARA tb_rol
CREATE TRIGGER TR_AuditoriaR_Insertar
ON tb_rol
FOR INSERT
AS
BEGIN
    INSERT INTO AUDITORIA 
    SELECT 'DESCONOCIDO', 'ROL', 'INSERTÓ', 
           CONVERT(NVARCHAR(12), id_rol), 
           name_role, 
           'NINGUNA', 
           GETDATE()
    FROM inserted;
END;
GO

-- Ejemplo de inserción en tb_rol
INSERT INTO tb_rol (name_role)
VALUES ('Marketing');
GO

-- Verificar auditoría de inserción en tb_rol
SELECT * FROM tb_rol;
SELECT * FROM AUDITORIA;
GO

-------------------------------------

-- TRIGGER ELIMINAR PARA tb_rol
CREATE TRIGGER TR_AuditoriaR_Eliminar
ON tb_rol
FOR DELETE
AS
BEGIN
    INSERT INTO AUDITORIA 
    SELECT 'DESCONOCIDO', 'ROL', 'ELIMINÓ', 
           CONVERT(NVARCHAR(12), id_rol), 
           name_role, 
           'NINGUNA', 
           GETDATE()
    FROM deleted;
END;
GO

-- Ejemplo de eliminación en tb_rol
DELETE FROM tb_rol
WHERE id_rol = 2;  
GO

-- Verificar auditoría de eliminación en tb_rol
SELECT * FROM tb_rol;
SELECT * FROM AUDITORIA;
GO

-------------------------------------

-- TRIGGER ACTUALIZAR PARA tb_rol
CREATE TRIGGER TR_AuditoriaR_Actualizar
ON tb_rol
FOR UPDATE
AS
BEGIN
    INSERT INTO AUDITORIA 
    SELECT 'DESCONOCIDO', 'ROL', 'ACTUALIZÓ', 
           CONVERT(NVARCHAR(12), id_rol), 
           name_role, 
           (SELECT name_role FROM deleted), 
           GETDATE()
    FROM inserted;
END;
GO

-- Ejemplo de actualización en tb_rol
UPDATE tb_rol
SET name_role = 'Vendedor'
WHERE id_rol = 3; 
GO

-- Verificar auditoría de actualización en tb_rol
SELECT * FROM tb_rol;
SELECT * FROM AUDITORIA;
GO


-----------------------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------- TRIGGER USUARIO ------------------------------------------------------------- 
-----------------------------------------------------------------------------------------------------------------------------------

-- TRIGGER INSERTAR PARA tb_usuario
CREATE TRIGGER TR_AuditoriaU_Insertar
ON tb_usuario
FOR INSERT
AS
BEGIN
    INSERT INTO AUDITORIA 
    SELECT SUSER_SNAME(), 'USUARIO', 'INSERTÓ', 
           CONVERT(NVARCHAR(12), id_user), 
           username, 
           'NINGUNA', 
           GETDATE()
    FROM inserted;
END;
GO

-- Ejemplo de inserción en tb_usuario
INSERT INTO tb_usuario (username, email, phone_number, password, name_role_id, created, modified, is_superuser, is_staff, is_active, date_joined) VALUES
('pepe3', 'pepe3@gmail.com', '+51999999993', 'admin123456', 2, SYSDATETIME(), SYSDATETIME(), 1, 1, 1, SYSDATETIME());
GO

-- Verificar auditoría de inserción en tb_usuario
SELECT * FROM tb_usuario;
SELECT * FROM AUDITORIA;
GO

-------------------------------------

-- TRIGGER ELIMINAR PARA tb_usuario
CREATE TRIGGER TR_AuditoriaU_Eliminar
ON tb_usuario
FOR DELETE
AS
BEGIN
    INSERT INTO AUDITORIA 
    SELECT 'DESCONOCIDO', 'USUARIO', 'ELIMINÓ', 
           CONVERT(NVARCHAR(12), id_user), 
           username, 
           'NINGUNA', 
           GETDATE()
    FROM deleted;
END;
GO

-- Ejemplo de eliminación en tb_usuario
DELETE FROM tb_usuario
WHERE id_user = 2;  
GO

-- Verificar auditoría de eliminación en tb_usuario
SELECT * FROM tb_usuario;
SELECT * FROM AUDITORIA;
GO

-------------------------------------

-- TRIGGER ACTUALIZAR PARA tb_usuario
CREATE TRIGGER TR_AuditoriaU_Actualizar
ON tb_usuario
FOR UPDATE
AS
BEGIN
    INSERT INTO AUDITORIA 
    SELECT 'DESCONOCIDO', 'USUARIO', 'ACTUALIZÓ', 
           CONVERT(NVARCHAR(12), id_user), 
           username, 
           (SELECT username FROM deleted), 
           GETDATE()
    FROM inserted;
END;
GO

-- Ejemplo de actualización en tb_usuario
UPDATE tb_usuario
SET username = 'eduardo1'
WHERE id_user= 1; 
GO

-- Verificar auditoría de actualización en tb_usuario
SELECT * FROM tb_usuario;
SELECT * FROM AUDITORIA;
GO


-----------------------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------- TRIGGER CATEGORIA ------------------------------------------------------------- 
-----------------------------------------------------------------------------------------------------------------------------------

-- TRIGGER INSERTAR PARA tb_categoria
CREATE TRIGGER TR_AuditoriaC_Insertar
ON tb_categoria
FOR INSERT
AS
BEGIN
    INSERT INTO AUDITORIA 
    SELECT 'DESCONOCIDO', 'CATEGORIA', 'INSERTÓ', 
           CONVERT(NVARCHAR(12), id_categoria), 
           nombre_categoria, 
           'NINGUNA', 
           GETDATE()
    FROM inserted;
END;
GO

-- Ejemplo de inserción en tb_categoria
INSERT INTO tb_categoria (nombre_categoria, estado_categoria, created_at, update_at) VALUES
('Alcohol en gel', 1, GETDATE(), GETDATE());
GO

-- Verificar auditoría de inserción en tb_categoria
SELECT * FROM tb_categoria;
SELECT * FROM AUDITORIA;
GO

-------------------------------------

-- TRIGGER ELIMINAR PARA tb_categoria
CREATE TRIGGER TR_AuditoriaC_Eliminar
ON tb_categoria
FOR DELETE
AS
BEGIN
    INSERT INTO AUDITORIA 
    SELECT 'DESCONOCIDO', 'CATEGORIA', 'ELIMINÓ', 
           CONVERT(NVARCHAR(12), id_categoria), 
           nombre_categoria, 
           'NINGUNA', 
           GETDATE()
    FROM deleted;
END;
GO

-- Ejemplo de eliminación en tb_categoria
DELETE FROM tb_categoria
WHERE id_categoria = 2;  
GO

-- Verificar auditoría de eliminación en tb_categoria
SELECT * FROM tb_categoria;
SELECT * FROM AUDITORIA;
GO

-------------------------------------

-- TRIGGER ACTUALIZAR PARA tb_categoria
CREATE TRIGGER TR_AuditoriaC_Actualizar
ON tb_categoria
FOR UPDATE
AS
BEGIN
    INSERT INTO AUDITORIA 
    SELECT 'DESCONOCIDO', 'CATEGORIA', 'ACTUALIZÓ', 
           CONVERT(NVARCHAR(12), id_categoria), 
           nombre_categoria, 
           (SELECT nombre_categoria FROM deleted), 
           GETDATE()
    FROM inserted;
END;
GO

-- Ejemplo de actualización en tb_categoria
UPDATE tb_categoria
SET nombre_categoria = 'Jabón para ropa'
WHERE id_categoria = 3; 
GO

-- Verificar auditoría de actualización en tb_categoria
SELECT * FROM tb_categoria;
SELECT * FROM AUDITORIA;
GO


-----------------------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------- TRIGGER MARCA ------------------------------------------------------------- 
-----------------------------------------------------------------------------------------------------------------------------------

-- TRIGGER INSERTAR PARA tb_marca
CREATE TRIGGER TR_AuditoriaM_Insertar
ON tb_marca
FOR INSERT
AS
BEGIN
    INSERT INTO AUDITORIA 
    SELECT 'DESCONOCIDO', 'MARCA', 'INSERTÓ', 
           CONVERT(NVARCHAR(12), id_marca), 
           nombre_marca, 
           'NINGUNA', 
           GETDATE()
    FROM inserted;
END;
GO

-- Ejemplo de inserción en tb_marca
INSERT INTO tb_marca (nombre_marca, estado_marca, created_at, update_at) VALUES
('Easy cleaning', 1, GETDATE(), GETDATE());
GO

-- Verificar auditoría de inserción en tb_marca
SELECT * FROM tb_marca;
SELECT * FROM AUDITORIA;
GO

-------------------------------------

-- TRIGGER ELIMINAR PARA tb_marca
CREATE TRIGGER TR_AuditoriaM_Eliminar
ON tb_marca
FOR DELETE
AS
BEGIN
    INSERT INTO AUDITORIA 
    SELECT 'DESCONOCIDO', 'MARCA', 'ELIMINÓ', 
           CONVERT(NVARCHAR(12), id_marca), 
           nombre_marca, 
           'NINGUNA', 
           GETDATE()
    FROM deleted;
END;
GO

-- Ejemplo de eliminación en tb_marca
DELETE FROM tb_marca
WHERE id_marca = 2;  
GO

-- Verificar auditoría de eliminación en tb_marca
SELECT * FROM tb_marca;
SELECT * FROM AUDITORIA;
GO

-------------------------------------

-- TRIGGER ACTUALIZAR PARA tb_marca
CREATE TRIGGER TR_AuditoriaM_Actualizar
ON tb_marca
FOR UPDATE
AS
BEGIN
    INSERT INTO AUDITORIA 
    SELECT 'DESCONOCIDO', 'MARCA', 'ACTUALIZÓ', 
           CONVERT(NVARCHAR(12), id_marca), 
           nombre_marca, 
           (SELECT nombre_marca FROM deleted), 
           GETDATE()
    FROM inserted;
END;
GO

-- Ejemplo de actualización en tb_marca
UPDATE tb_marca
SET nombre_marca = 'Master Cleaning'
WHERE id_marca = 3; 
GO

-- Verificar auditoría de actualización en tb_marca
SELECT * FROM tb_marca;
SELECT * FROM AUDITORIA;
GO


-----------------------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------- TRIGGER UNIDAD MEDIDA ------------------------------------------------------------- 
-----------------------------------------------------------------------------------------------------------------------------------

-- TRIGGER INSERTAR PARA tb_unidad_medida
CREATE TRIGGER TR_AuditoriaUM_Insertar
ON tb_unidadMedida
FOR INSERT
AS
BEGIN
    INSERT INTO AUDITORIA 
    SELECT 'DESCONOCIDO', 'UNIDAD_MEDIDA', 'INSERTÓ', 
           CONVERT(NVARCHAR(12), id_unidadMedida), 
           nombre_unidad, 
           'NINGUNA', 
           GETDATE()
    FROM inserted;
END;
GO

-- Ejemplo de inserción en tb_unidad_medida
INSERT INTO tb_unidadMedida (nombre_unidad, abreviacion, created_at, update_at) VALUES
('Tonelada', 'T', GETDATE(), GETDATE());
GO

-- Verificar auditoría de inserción en tb_unidad_medida
SELECT * FROM tb_unidadMedida;
SELECT * FROM AUDITORIA;
GO

-------------------------------------

-- TRIGGER ELIMINAR PARA tb_unidad_medida
CREATE TRIGGER TR_AuditoriaUM_Eliminar
ON tb_unidadMedida
FOR DELETE
AS
BEGIN
    INSERT INTO AUDITORIA 
    SELECT 'DESCONOCIDO', 'UNIDAD_MEDIDA', 'ELIMINÓ', 
           CONVERT(NVARCHAR(12), id_unidadMedida), 
           nombre_unidad, 
           'NINGUNA', 
           GETDATE()
    FROM deleted;
END;
GO

-- Ejemplo de eliminación en tb_unidad_medida
DELETE FROM tb_unidadMedida
WHERE id_unidadMedida = 2;  
GO

-- Verificar auditoría de eliminación en tb_unidad_medida
SELECT * FROM tb_unidadMedida;
SELECT * FROM AUDITORIA;
GO

-------------------------------------

-- TRIGGER ACTUALIZAR PARA tb_unidad_medida
CREATE TRIGGER TR_AuditoriaUM_Actualizar
ON tb_unidadMedida
FOR UPDATE
AS
BEGIN
    INSERT INTO AUDITORIA 
    SELECT 'DESCONOCIDO', 'UNIDAD_MEDIDA', 'ACTUALIZÓ', 
           CONVERT(NVARCHAR(12), id_unidadMedida), 
           nombre_unidad, 
           (SELECT nombre_unidad FROM deleted), 
           GETDATE()
    FROM inserted;
END;
GO

-- Ejemplo de actualización en tb_unidad_medida
UPDATE tb_unidadMedida
SET nombre_unidad = 'Galonazo'
WHERE id_unidadMedida = 3; 
GO

-- Verificar auditoría de actualización en tb_unidad_medida
SELECT * FROM tb_unidadMedida;
SELECT * FROM AUDITORIA;
GO

-----------------------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------- TRIGGER LEGEND ------------------------------------------------------------- 
-----------------------------------------------------------------------------------------------------------------------------------

-- TRIGGER INSERTAR PARA tb_legend
CREATE TRIGGER TR_AuditoriaL_Insertar
ON tb_legend
FOR INSERT
AS
BEGIN
    INSERT INTO AUDITORIA 
    SELECT 'DESCONOCIDO', 'LEGEND', 'INSERTÓ', 
           CONVERT(NVARCHAR(12), id_legend), 
           legend_value, 
           'NINGUNA', 
           GETDATE()
    FROM inserted;
END;
GO

-- Ejemplo de inserción en tb_legend
INSERT INTO tb_legend (legend_code, legend_value)
VALUES 
('1000', 'SON TREINTA CON 50/100 SOLES');
GO

-- Verificar auditoría de inserción en tb_legend
SELECT * FROM tb_legend;
SELECT * FROM AUDITORIA;
GO

-------------------------------------

-- TRIGGER ELIMINAR PARA tb_legend
CREATE TRIGGER TR_AuditoriaL_Eliminar
ON tb_legend
FOR DELETE
AS
BEGIN
    INSERT INTO AUDITORIA 
    SELECT 'DESCONOCIDO', 'LEGEND', 'ELIMINÓ', 
           CONVERT(NVARCHAR(12), id_legend), 
           legend_value, 
           'NINGUNA', 
           GETDATE()
    FROM deleted;
END;
GO

-- Ejemplo de eliminación en tb_legend
DELETE FROM tb_legend
WHERE id_legend = 2;  
GO

-- Verificar auditoría de eliminación en tb_legend
SELECT * FROM tb_legend;
SELECT * FROM AUDITORIA;
GO

-------------------------------------

-- TRIGGER ACTUALIZAR PARA tb_legend
CREATE TRIGGER TR_AuditoriaL_Actualizar
ON tb_legend
FOR UPDATE
AS
BEGIN
    INSERT INTO AUDITORIA 
    SELECT 'DESCONOCIDO', 'LEGEND', 'ACTUALIZÓ', 
           CONVERT(NVARCHAR(12), id_legend), 
           legend_value, 
           (SELECT legend_value FROM deleted), 
           GETDATE()
    FROM inserted;
END;
GO

-- Ejemplo de actualización en tb_legend
UPDATE tb_legend
SET legend_value = 'SON CINCUENTA CON 50/100 SOLES'
WHERE id_legend = 3; 
GO

-- Verificar auditoría de actualización en tb_legend
SELECT * FROM tb_legend;
SELECT * FROM AUDITORIA;
GO


-----------------------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------- TRIGGER FORMA PAGO ------------------------------------------------------------- 
-----------------------------------------------------------------------------------------------------------------------------------

-- TRIGGER INSERTAR PARA tb_forma_pago
CREATE TRIGGER TR_AuditoriaFP_Insertar
ON tb_forma_pago
FOR INSERT
AS
BEGIN
    INSERT INTO AUDITORIA 
    SELECT 'DESCONOCIDO', 'FORMA PAGO', 'INSERTÓ', 
           CONVERT(NVARCHAR(12), id_formaPago), 
           tipo, 
           'NINGUNA', 
           GETDATE()
    FROM inserted;
END;
GO

-- Ejemplo de inserción en tb_forma_pago
INSERT INTO tb_forma_pago (tipo, monto, cuota, fecha_emision, fecha_vencimiento)
VALUES 
('Transferencia', 250.00, 1, GETDATE(), DATEADD(DAY, 30, GETDATE()));
GO

-- Verificar auditoría de inserción en tb_forma_pago
SELECT * FROM tb_forma_pago;
SELECT * FROM AUDITORIA;
GO

-------------------------------------

-- TRIGGER ELIMINAR PARA tb_forma_pago
CREATE TRIGGER TR_AuditoriaFP_Eliminar
ON tb_forma_pago
FOR DELETE
AS
BEGIN
    INSERT INTO AUDITORIA 
    SELECT 'DESCONOCIDO', 'FORMA PAGO', 'ELIMINÓ', 
           CONVERT(NVARCHAR(12), id_formaPago), 
           tipo, 
           'NINGUNA', 
           GETDATE()
    FROM deleted;
END;
GO

-- Ejemplo de eliminación en tb_forma_pago
DELETE FROM tb_forma_pago
WHERE id_formaPago = 2;  
GO

-- Verificar auditoría de eliminación en tb_forma_pago
SELECT * FROM tb_forma_pago;
SELECT * FROM AUDITORIA;
GO

-------------------------------------

-- TRIGGER ACTUALIZAR PARA tb_forma_pago
CREATE TRIGGER TR_AuditoriaFP_Actualizar
ON tb_forma_pago
FOR UPDATE
AS
BEGIN
    INSERT INTO AUDITORIA 
    SELECT 'DESCONOCIDO', 'FORMA PAGO', 'ACTUALIZÓ', 
           CONVERT(NVARCHAR(12), id_formaPago), 
           tipo, 
           (SELECT tipo FROM deleted), 
           GETDATE()
    FROM inserted;
END;
GO

-- Ejemplo de actualización en tb_forma_pago
UPDATE tb_forma_pago
SET tipo = 'Efectivo'
WHERE id_formaPago = 3; 
GO

-- Verificar auditoría de actualización en tb_forma_pago
SELECT * FROM tb_forma_pago;
SELECT * FROM AUDITORIA;
GO

-----------------------------------------------------------------------------------------------------------------------------------
--------------------------------------------------------- TRIGGER COMPROBANTE --------------------------------------------------------- 
-----------------------------------------------------------------------------------------------------------------------------------

-- TRIGGER INSERTAR PARA tb_comprobante
CREATE TRIGGER TR_AuditoriaCB_Insertar
ON tb_comprobante
FOR INSERT
AS
BEGIN
    INSERT INTO AUDITORIA 
    SELECT 'DESCONOCIDO', 'COMPROBANTE', 'INSERTÓ', 
           CONVERT(NVARCHAR(12), id_comprobante), 
           tipo_doc, 
           'NINGUNA', 
           GETDATE()
    FROM inserted;
END;
GO

-- Ejemplo de inserción en tb_comprobante
INSERT INTO tb_comprobante (
    tipo_operacion, tipo_doc, numero_serie, correlativo, tipo_moneda, fecha_emision, hora_emision,
    empresa_ruc, razon_social, nombre_comercial, urbanizacion, distrito, departamento, email_empresa, telefono_emp, 
    cliente_tipo_doc, monto_Oper_Gravadas, monto_Igv, valor_venta, sub_Total, monto_Imp_Venta, estado_Documento, 
    manual, pdf_url, cliente_id, usuario_id, forma_pago_id, legend_comprobante_id
) VALUES
('003', 'B003', '0030', '000003', 'PEN', GETDATE(), GETDATE(), '20512345678', 'Daryza S.A.C.', 'Daryza', 'Urbanización 2', 'Miraflores', 'Lima', 'ventas@daryza.com', '01-8765432', '12345678', 500.00, 90.00, 590.00, 590.00, 590.00, '1', 0, 2, 2, 2, 1);
GO

-- Verificar auditoría de inserción en tb_comprobante
SELECT * FROM tb_comprobante;
SELECT * FROM AUDITORIA;
GO

-------------------------------------

-- TRIGGER ELIMINAR PARA tb_comprobante
CREATE TRIGGER TR_AuditoriaCB_Eliminar
ON tb_comprobante
FOR DELETE
AS
BEGIN
    INSERT INTO AUDITORIA 
    SELECT 'DESCONOCIDO', 'COMPROBANTE', 'ELIMINÓ', 
           CONVERT(NVARCHAR(12), id_comprobante), 
           tipo_doc, 
           'NINGUNA', 
           GETDATE()
    FROM deleted;
END;
GO

-- Ejemplo de eliminación en tb_comprobante
DELETE FROM tb_comprobante
WHERE id_comprobante = 2;  
GO

-- Verificar auditoría de eliminación en tb_comprobante
SELECT * FROM tb_comprobante;
SELECT * FROM AUDITORIA;
GO

-------------------------------------

-- TRIGGER ACTUALIZAR PARA tb_comprobante
CREATE TRIGGER TR_AuditoriaCB_Actualizar
ON tb_comprobante
FOR UPDATE
AS
BEGIN
    INSERT INTO AUDITORIA 
    SELECT 'DESCONOCIDO', 'COMPROBANTE', 'ACTUALIZÓ', 
           CONVERT(NVARCHAR(12), id_comprobante), 
           tipo_doc, 
           (SELECT tipo_doc FROM deleted), 
           GETDATE()
    FROM inserted;
END;
GO

-- Ejemplo de actualización en tb_comprobante
UPDATE tb_comprobante
SET tipo_moneda = 'USD'
WHERE id_comprobante = 3; 
GO

-- Verificar auditoría de actualización en tb_comprobante
SELECT * FROM tb_comprobante;
SELECT * FROM AUDITORIA;
GO


-----------------------------------------------------------------------------------------------------------------------------------
---------------------------------------------------- TRIGGER DETALLE COMPROBANTE ---------------------------------------------------- 
-----------------------------------------------------------------------------------------------------------------------------------

-- TRIGGER INSERTAR PARA tb_detalle_comprobante
CREATE TRIGGER TR_AuditoriaDCB_Insertar
ON tb_detalle_comprobante
FOR INSERT
AS
BEGIN
    INSERT INTO AUDITORIA 
    SELECT 'DESCONOCIDO', 'DETALLE COMPROBANTE', 'INSERTÓ', 
           CONVERT(NVARCHAR(12), id_detalleComprobante), 
           CONVERT(NVARCHAR(12), comprobante_id), 
           'NINGUNA', 
           GETDATE()
    FROM inserted;
END;
GO

-- Ejemplo de inserción en tb_detalle_comprobante
INSERT INTO tb_detalle_comprobante (
    unidad, cantidad, id_producto, descripcion, monto_valorUnitario, 
    igv_detalle, monto_Precio_Unitario, monto_Valor_Venta, 
    fecha_emision, hora_emision, comprobante_id, producto_id
)
VALUES 
('LT', 5, 'P002', 'Limpiador Multiusos', 20.00, 3.60, 100.00, 106.60, 3, 2);
GO

-- Verificar auditoría de inserción en tb_detalle_comprobante
SELECT * FROM tb_detalle_comprobante;
SELECT * FROM AUDITORIA;
GO

-------------------------------------

-- TRIGGER ELIMINAR PARA tb_detalle_comprobante
CREATE TRIGGER TR_AuditoriaDCB_Eliminar
ON tb_detalle_comprobante
FOR DELETE
AS
BEGIN
    INSERT INTO AUDITORIA 
    SELECT 'DESCONOCIDO', 'DETALLE COMPROBANTE', 'ELIMINÓ', 
           CONVERT(NVARCHAR(12), id_detalleComprobante), 
           CONVERT(NVARCHAR(12), comprobante_id), 
           'NINGUNA', 
           GETDATE()
    FROM deleted;
END;
GO

-- Ejemplo de eliminación en tb_detalle_comprobante
DELETE FROM tb_detalle_comprobante
WHERE id_detalleComprobante = 3;  
GO

-- Verificar auditoría de eliminación en tb_detalle_comprobante
SELECT * FROM tb_detalle_comprobante;
SELECT * FROM AUDITORIA;
GO

-------------------------------------

-- TRIGGER ACTUALIZAR PARA tb_detalle_comprobante
CREATE TRIGGER TR_AuditoriaDCB_Actualizar
ON tb_detalle_comprobante
FOR UPDATE
AS
BEGIN
    INSERT INTO AUDITORIA 
    SELECT 'DESCONOCIDO', 'DETALLE COMPROBANTE', 'ACTUALIZÓ', 
           CONVERT(NVARCHAR(12), id_detalleComprobante), 
           CONVERT(NVARCHAR(12), comprobante_id), 
           (SELECT CONVERT(NVARCHAR(12), comprobante_id) FROM deleted), 
           GETDATE()
    FROM inserted;
END;
GO

-- Ejemplo de actualización en tb_detalle_comprobante
UPDATE tb_detalle_comprobante
SET cantidad = 3
WHERE id_detalleComprobante = 3; 
GO

-- Verificar auditoría de actualización en tb_detalle_comprobante
SELECT * FROM tb_detalle_comprobante;
SELECT * FROM AUDITORIA;
GO

-----------------------------------------------------------------------------------------------------------------------------------
--------------------------------------------------------- TRIGGER MOVIMIENTO --------------------------------------------------------- 
-----------------------------------------------------------------------------------------------------------------------------------

-- TRIGGER INSERTAR PARA tb_movimiento
CREATE TRIGGER TR_AuditoriaMV_Insertar
ON tb_movimiento
FOR INSERT
AS
BEGIN
    INSERT INTO AUDITORIA 
    SELECT 'DESCONOCIDO', 'MOVIMIENTO', 'INSERTÓ', 
           CONVERT(NVARCHAR(12), id_movimiento), 
           referencia, 
           'NINGUNA', 
           GETDATE()
    FROM inserted;
END;
GO

-- Ejemplo de inserción en tb_movimiento
INSERT INTO tb_movimiento (referencia, cant_total, sucursal_id, created_at, updated_at, usuario_id, tipo_movimiento_id)
VALUES 
('Venta de productos', 100, 1, GETDATE(), GETDATE(), 2, 1);
GO

-- Verificar auditoría de inserción en tb_movimiento
SELECT * FROM tb_movimiento;
SELECT * FROM AUDITORIA;
GO

-------------------------------------

-- TRIGGER ELIMINAR PARA tb_movimiento
CREATE TRIGGER TR_AuditoriaMV_Eliminar
ON tb_movimiento
FOR DELETE
AS
BEGIN
    INSERT INTO AUDITORIA 
    SELECT 'DESCONOCIDO', 'MOVIMIENTO', 'ELIMINÓ', 
           CONVERT(NVARCHAR(12), id_movimiento), 
           referencia, 
           'NINGUNA', 
           GETDATE()
    FROM deleted;
END;
GO

-- Ejemplo de eliminación en tb_movimiento
DELETE FROM tb_movimiento
WHERE id_movimiento = 2;  
GO

-- Verificar auditoría de eliminación en tb_movimiento
SELECT * FROM tb_movimiento;
SELECT * FROM AUDITORIA;
GO

-------------------------------------

-- TRIGGER ACTUALIZAR PARA tb_movimiento
CREATE TRIGGER TR_AuditoriaMV_Actualizar
ON tb_movimiento
FOR UPDATE
AS
BEGIN
    INSERT INTO AUDITORIA 
    SELECT 'DESCONOCIDO', 'MOVIMIENTO', 'ACTUALIZÓ', 
           CONVERT(NVARCHAR(12), id_movimiento), 
           referencia, 
           (SELECT referencia FROM deleted), 
           GETDATE()
    FROM inserted;
END;
GO

-- Ejemplo de actualización en tb_movimiento
UPDATE tb_movimiento
SET cant_total = 50
WHERE id_movimiento = 3; 
GO

-- Verificar auditoría de actualización en tb_movimiento
SELECT * FROM tb_movimiento;
SELECT * FROM AUDITORIA;
GO


-----------------------------------------------------------------------------------------------------------------------------------
--------------------------------------------------------- TRIGGER TIPO MOVIMIENTO --------------------------------------------------------- 
-----------------------------------------------------------------------------------------------------------------------------------

-- TRIGGER INSERTAR PARA tb_tipo_movimiento
CREATE TRIGGER TR_AuditoriaTM_Insertar
ON tb_tipoMovimiento
FOR INSERT
AS
BEGIN
    INSERT INTO AUDITORIA 
    SELECT 'DESCONOCIDO', 'TIPO MOVIMIENTO', 'INSERTÓ', 
           CONVERT(NVARCHAR(12), id_tipoMovimiento), 
           descripcion, 
           'NINGUNA', 
           GETDATE()
    FROM inserted;
END;
GO

-- Ejemplo de inserción en tb_tipo_movimiento
INSERT INTO tb_tipoMovimiento (descripcion) VALUES
('Retorno');
GO

-- Verificar auditoría de inserción en tb_tipo_movimiento
SELECT * FROM tb_tipoMovimiento;
SELECT * FROM AUDITORIA;
GO

-------------------------------------

-- TRIGGER ELIMINAR PARA tb_tipo_movimiento
CREATE TRIGGER TR_AuditoriaTM_Eliminar
ON tb_tipoMovimiento
FOR DELETE
AS
BEGIN
    INSERT INTO AUDITORIA 
    SELECT 'DESCONOCIDO', 'TIPO MOVIMIENTO', 'ELIMINÓ', 
           CONVERT(NVARCHAR(12), id_tipoMovimiento), 
           descripcion, 
           'NINGUNA', 
           GETDATE()
    FROM deleted;
END;
GO

-- Ejemplo de eliminación en tb_tipo_movimiento
DELETE FROM tb_tipoMovimiento
WHERE id_tipoMovimiento = 2;  
GO

-- Verificar auditoría de eliminación en tb_tipo_movimiento
SELECT * FROM tb_tipoMovimiento;
SELECT * FROM AUDITORIA;
GO

-------------------------------------

-- TRIGGER ACTUALIZAR PARA tb_tipo_movimiento
CREATE TRIGGER TR_AuditoriaTM_Actualizar
ON tb_tipoMovimiento
FOR UPDATE
AS
BEGIN
    INSERT INTO AUDITORIA 
    SELECT 'DESCONOCIDO', 'TIPO MOVIMIENTO', 'ACTUALIZÓ', 
           CONVERT(NVARCHAR(12), id_tipoMovimiento), 
           descripcion, 
           (SELECT descripcion FROM deleted), 
           GETDATE()
    FROM inserted;
END;
GO

-- Ejemplo de actualización en tb_tipo_movimiento
UPDATE tb_tipoMovimiento
SET descripcion = 'Entrada nueva'
WHERE id_tipoMovimiento = 1; 
GO

-- Verificar auditoría de actualización en tb_tipo_movimiento
SELECT * FROM tb_tipoMovimiento;
SELECT * FROM AUDITORIA;
GO


-----------------------------------------------------------------------------------------------------------------------------------
------------------------------------------------------ TRIGGER DETALLE MOVIMIENTO ----------------------------------------------------- 
-----------------------------------------------------------------------------------------------------------------------------------

-- TRIGGER INSERTAR PARA tb_detalle_movimiento
CREATE TRIGGER TR_AuditoriaDM_Insertar
ON tb_detalleMovimiento
FOR INSERT
AS
BEGIN
    INSERT INTO AUDITORIA 
    SELECT 'DESCONOCIDO', 'DETALLE MOVIMIENTO', 'INSERTÓ', 
           CONVERT(NVARCHAR(12), id_detalleMovimiento), 
           CONVERT(NVARCHAR(12), movimiento_id), 
           'NINGUNA', 
           GETDATE()
    FROM inserted;
END;
GO

-- Ejemplo de inserción en tb_detalle_movimiento
INSERT INTO tb_detalleMovimiento (cantidad, detalleComprobante_id, producto_id, movimiento_id)
VALUES 
(200, 1, 2, 1);
GO

-- Verificar auditoría de inserción en tb_detalle_movimiento
SELECT * FROM tb_detalleMovimiento;
SELECT * FROM AUDITORIA;
GO

-------------------------------------

-- TRIGGER ELIMINAR PARA tb_detalle_movimiento
CREATE TRIGGER TR_AuditoriaDM_Eliminar
ON tb_detalleMovimiento
FOR DELETE
AS
BEGIN
    INSERT INTO AUDITORIA 
    SELECT 'DESCONOCIDO', 'DETALLE MOVIMIENTO', 'ELIMINÓ', 
           CONVERT(NVARCHAR(12), id_detalleMovimiento), 
           CONVERT(NVARCHAR(12), movimiento_id), 
           'NINGUNA', 
           GETDATE()
    FROM deleted;
END;
GO

-- Ejemplo de eliminación en tb_detalle_movimiento
DELETE FROM tb_detalleMovimiento
WHERE id_detalleMovimiento = 2;  
GO

-- Verificar auditoría de eliminación en tb_detalle_movimiento
SELECT * FROM tb_detalleMovimiento;
SELECT * FROM AUDITORIA;
GO

-------------------------------------

-- TRIGGER ACTUALIZAR PARA tb_detalle_movimiento
CREATE TRIGGER TR_AuditoriaDM_Actualizar
ON tb_detalleMovimiento
FOR UPDATE
AS
BEGIN
    INSERT INTO AUDITORIA 
    SELECT 'DESCONOCIDO', 'DETALLE MOVIMIENTO', 'ACTUALIZÓ', 
           CONVERT(NVARCHAR(12), id_detalleMovimiento), 
           CONVERT(NVARCHAR(12), movimiento_id), 
           (SELECT CONVERT(NVARCHAR(12), movimiento_id) FROM deleted), 
           GETDATE()
    FROM inserted;
END;
GO

-- Ejemplo de actualización en tb_detalle_movimiento
UPDATE tb_detalleMovimiento
SET cantidad = 40
WHERE id_detalleMovimiento = 2; 
GO

-- Verificar auditoría de actualización en tb_detalle_movimiento
SELECT * FROM tb_detalleMovimiento;
SELECT * FROM AUDITORIA;
GO















--------------------------------------------------------------------
-------------------------DASHBOARD ---------------------------------
--------------------------------------------------------------------
use BD_DARYZA_DJANGO_V5
select * from tb_comprobante

--- Ventas Diarias por Dia de la Semana:

-- 1. Actualizar del id 1 al 4 a la fecha 2024-11-11:
UPDATE tb_comprobante
SET fecha_emision = '2024-11-11'
WHERE id_comprobante BETWEEN 1 AND 4;

-- 2. Actualizar del id 5 al 9 a la fecha 2024-11-12:
UPDATE tb_comprobante
SET fecha_emision = '2024-11-12'
WHERE id_comprobante BETWEEN 5 AND 9;

-- 3. Actualizar del id 10 al 17 a la fecha 2024-11-14:
UPDATE tb_comprobante
SET fecha_emision = '2024-11-14'
WHERE id_comprobante BETWEEN 10 AND 17;

-- 4. Actualizar del id 18 al 21 a la fecha 2024-11-15:
UPDATE tb_comprobante
SET fecha_emision = '2024-11-15'
WHERE id_comprobante BETWEEN 18 AND 21;


