create database bd_daryza_v1;
-- drop database bd_daryza_v1;
USE bd_daryza_v1;

INSERT INTO tb_rol (name_role) VALUES
('Asignar'),
('Administrador'),
('Ventas'),
('Almacen');
select * from tb_rol;

INSERT INTO tb_usuario (username, email, phone_number, password, name_role_id, created, modified, is_superuser, is_staff, is_active, date_joined) VALUES
('juan1', 'juan1@gmail.com', '+51999999991', 'admin', 2, NOW(), NOW(), TRUE, TRUE, TRUE, NOW()),
('juan2', 'juan2@gmail.com', '+51999999992', 'admin', 3, NOW(), NOW(), FALSE, FALSE, TRUE, NOW()),
('juan3', 'juan3@gmail.com', '+51999999993', 'admin', 4, NOW(), NOW(), FALSE, FALSE, TRUE, NOW());
 -- Actualizar la contraseña en admin django y agregar un token.
 
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
