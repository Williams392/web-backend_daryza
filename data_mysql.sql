-- -------------------
-- codigo MYSQL:
-- -------------------

create database bd_daryza_v1;
USE bd_daryza_v1;

-- 1. Antes de insertar crear el super user.
INSERT INTO tb_rol (name_role) VALUES
('Asignar'),
('Administrador'),
('Ventas'),
('Almacen');

INSERT INTO tb_usuario (username, email, phone_number, password, name_role_id, created, modified, is_superuser, is_staff, is_active, date_joined) VALUES
('kevin1', 'kevin1@gmail.com', '+51999999991', 'admin123456', 2, NOW(), NOW(), TRUE, TRUE, TRUE, NOW()),
('Sebas2', 'sebas2@gmail.com', '+51999999992', 'admin123456', 3, NOW(), NOW(), FALSE, FALSE, TRUE, NOW());
-- ('juan3', 'juan3@gmail.com', '+51999999993', 'admin123456', 4, NOW(), NOW(), FALSE, FALSE, TRUE, NOW());
 -- Actualizar la contraseña en admin django y agregar un token.
 
INSERT INTO tb_sucursal (nombre_sucursal, descripcion, telf_suc, correo_suc, direccion_sucursal) VALUES
('Daryza S.A.C lurin', 'Panamericana Sur, luirn', '99293948', 'webmaster@daryza.com', 'km30, antigua panamericana Sur, luirn');
 
INSERT INTO tb_categoria (nombre_categoria, estado_categoria, created_at, update_at) VALUES
('Detergente Líquido', TRUE, NOW(), NOW()),
('Desinfectante', TRUE, NOW(), NOW()),
('Jabón Líquido', TRUE, NOW(), NOW()),
('Lejía', TRUE, NOW(), NOW()),
('Suavizante', TRUE, NOW(), NOW()),
('Limpiador Multiusos', TRUE, NOW(), NOW()),
('Desengrasante', TRUE, NOW(), NOW()),
('Aromatizador', TRUE, NOW(), NOW()),
('Cera Líquida', TRUE, NOW(), NOW()),
('Lavavajillas', TRUE, NOW(), NOW());

INSERT INTO tb_marca (nombre_marca, estado_marca, created_at, update_at) VALUES
('Daryza', TRUE, NOW(), NOW()),
('Clorox', TRUE, NOW(), NOW()),
('Lysol', TRUE, NOW(), NOW()),
('Mr. Clean', TRUE, NOW(), NOW()),
('Fabuloso', TRUE, NOW(), NOW()),
('Ajax', TRUE, NOW(), NOW()),
('Pine-Sol', TRUE, NOW(), NOW()),
('Windex', TRUE, NOW(), NOW()),
('Scrubbing Bubbles', TRUE, NOW(), NOW()),
('Seventh Generation', TRUE, NOW(), NOW());

INSERT INTO tb_unidadMedida (nombre_unidad, abreviacion, created_at, update_at) VALUES
('Litro', 'L', NOW(), NOW()),
('Mililitro', 'ml', NOW(), NOW()),
('Galón', 'gal', NOW(), NOW()),
('Onza', 'oz', NOW(), NOW()),
('Kilogramo', 'kg', NOW(), NOW()),
('Gramo', 'g', NOW(), NOW()),
('Unidad', 'u', NOW(), NOW()),
('Paquete', 'paq', NOW(), NOW()),
('Caja', 'caja', NOW(), NOW()),
('Botella', 'bot', NOW(), NOW());

INSERT INTO tb_tipoMovimiento (descripcion) VALUES
('Entrada'),
('Salida');
-- select * from tb_tipoMovimiento

INSERT INTO tb_cliente (nombre_clie, apellido_clie, dni_cliente, ruc_cliente, direccion_clie, razon_socialCliente, tipo_empresa, email_cliente, telefono_cliente, fecha_creacion) VALUES
('Carlos', 'Fernandez', '12345678', '20123456789', 'Av. Siempre Viva 123, Lima', 'Carlos Fernandez S.A.C.', 'Empresa Privada', 'carlos.fernandez@example.com', '+51987654321', '2024-11-01 10:30:00'),
('María', 'Gomez', '87654321', '20234567890', 'Calle Los Pinos 456, Arequipa', 'María Gomez EIRL', 'Pequeña Empresa', 'maria.gomez@example.com', '+51981234567', '2024-11-01 10:30:00'),
('Jorge', 'Ramirez', '23456789', '20345678901', 'Jr. Las Flores 789, Trujillo', 'JR Servicios Generales', 'Mediana Empresa', 'jorge.ramirez@example.com', '+51983456789', '2024-11-01 10:30:00'),
('Lucia', 'Lopez', '34567890', '20456789012', 'Av. El Sol 135, Cusco', 'Lucia Lopez Corp.', 'Empresa Familiar', 'lucia.lopez@example.com', '+51985678901', '2024-11-01 10:30:00');
select * from tb_cliente