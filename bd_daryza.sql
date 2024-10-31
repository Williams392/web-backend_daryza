-- -------------------
-- codigo SQL SERVER:
-- -------------------

create database BD_DARYZA_T3;
use BD_DARYZA_T3;

-- 1. Crear tabla tb_rol (usada como FK en tb_usuario)
CREATE TABLE tb_rol (
    id_rol INT IDENTITY(1,1) PRIMARY KEY,
    name_role NVARCHAR(50) UNIQUE NOT NULL
);

-- 2. Crear tabla tb_usuario (usa FK de tb_rol)
CREATE TABLE tb_usuario (
    id_user INT IDENTITY(1,1) PRIMARY KEY,
    username NVARCHAR(50) UNIQUE NOT NULL,
	password NVARCHAR(128) NOT NULL,
    email NVARCHAR(150) UNIQUE NOT NULL,
    phone_number NVARCHAR(15) NOT NULL,
    created DATETIME DEFAULT GETDATE(),
    modified DATETIME DEFAULT GETDATE(),
    name_role INT NULL,
    first_name NVARCHAR(50) NULL,
    last_name NVARCHAR(50) NULL,
    CONSTRAINT FK_Rol FOREIGN KEY (name_role) REFERENCES tb_rol(id_rol)
);

-- 3. Crear tabla tb_categoria (usada como FK en tb_producto)
CREATE TABLE tb_categoria (
    id_categoria INT IDENTITY(1,1) PRIMARY KEY,
    nombre_categoria NVARCHAR(100) NOT NULL,
    estado_categoria BIT DEFAULT 1,
    created_at DATETIME DEFAULT GETDATE(),
    update_at DATETIME DEFAULT GETDATE()
);

-- 4. Crear tabla tb_marca (usada como FK en tb_producto)
CREATE TABLE tb_marca (
    id_marca INT IDENTITY(1,1) PRIMARY KEY,
    nombre_marca NVARCHAR(100) NOT NULL,
    estado_marca BIT DEFAULT 1,
    created_at DATETIME DEFAULT GETDATE(),
    update_at DATETIME DEFAULT GETDATE()
);

-- 5. Crear tabla tb_unidadMedida (usada como FK en tb_producto)
CREATE TABLE tb_unidadMedida (
    id_unidadMedida INT IDENTITY(1,1) PRIMARY KEY,
    nombre_unidad NVARCHAR(100) NOT NULL,
    abreviacion NVARCHAR(100) NOT NULL,
    created_at DATETIME DEFAULT GETDATE(),
    update_at DATETIME DEFAULT GETDATE()
);

-- 6. Crear tabla tb_producto (usa FK de tb_marca, tb_categoria, tb_unidadMedida)
CREATE TABLE tb_producto (
    id_producto INT IDENTITY(1,1) PRIMARY KEY,
    nombre_prod NVARCHAR(100) NOT NULL,
    descripcion_pro NVARCHAR(MAX) NULL,
    precio_compra DECIMAL(10, 2) NOT NULL,
    precio_venta DECIMAL(10, 2) NOT NULL,
    codigo NVARCHAR(100) NOT NULL,
    estado BIT DEFAULT 1,
    estock INT NOT NULL,
    estock_minimo INT NOT NULL,
    imagen NVARCHAR(MAX) NULL,
    marca INT NOT NULL,
    categoria INT NOT NULL,
    unidad_medida INT NOT NULL,
    created_at DATETIME DEFAULT GETDATE(),
    update_at DATETIME DEFAULT GETDATE(),
    CONSTRAINT FK_Marca FOREIGN KEY (marca) REFERENCES tb_marca(id_marca),
    CONSTRAINT FK_Categoria FOREIGN KEY (categoria) REFERENCES tb_categoria(id_categoria),
    CONSTRAINT FK_UnidadMedida FOREIGN KEY (unidad_medida) REFERENCES tb_unidadMedida(id_unidadMedida)
);

-- 7. Crear tabla tb_paciente
CREATE TABLE tb_cliente (
    id_cliente INT IDENTITY(1,1) PRIMARY KEY,
    nombre_clie NVARCHAR(255) NULL,
    apellido_clie NVARCHAR(255) NULL,
    direccion_clie NVARCHAR(255) NULL,

    dni_cliente NVARCHAR(8) UNIQUE NOT NULL,
	ruc_cliente NVARCHAR(11) UNIQUE NOT NULL,
	
	tipo_empresa NVARCHAR(255) NULL,
    email_cliente NVARCHAR(50) NULL,
    telefono_cliente NVARCHAR(20) NULL
);

-- 8. Tabla: tb_legend
CREATE TABLE tb_legend (
    id_legend INT IDENTITY(1,1) PRIMARY KEY,
    legend_code NVARCHAR(4) NOT NULL,
    legend_value NVARCHAR(MAX) NOT NULL
);

-- 9. Tabla: tb_forma_pago
CREATE TABLE tb_forma_pago (
    id_formaPago INT IDENTITY(1,1) PRIMARY KEY,
    tipo NVARCHAR(10) NOT NULL,
    monto DECIMAL(10, 2) DEFAULT 0.00,
    cuota INT DEFAULT 0,
    fecha_emision DATE DEFAULT GETDATE(),
    fecha_vencimiento DATE DEFAULT GETDATE()
);

-- 10. Crear tabla tb_sucursal (usada como FK en tb_comprobante y tb_movimiento)
CREATE TABLE tb_sucursal (
    id_sucursal INT IDENTITY(1,1) PRIMARY KEY,
    nombre NVARCHAR(50) NOT NULL,
    descripcion NVARCHAR(50) NULL,
    telf_suc NVARCHAR(20) NOT NULL,
    correo_suc NVARCHAR(25) NOT NULL,
    direccion NVARCHAR(50) NOT NULL
);

-- 11. Crear tabla tb_comprobante (usa FK de tb_empresa, tb_paciente, tb_impuesto, tb_estado_comprobante, tb_sucursal, tb_tipo_comprobante, tb_usuario, tb_movimiento)
CREATE TABLE tb_comprobante (
    id_comprobante INT IDENTITY(1,1) PRIMARY KEY,
    tipo_operacion NVARCHAR(4) NOT NULL,
    tipo_doc NVARCHAR(3) NOT NULL,
    numero_serie NVARCHAR(4) NOT NULL,
    correlativo NVARCHAR(25) NOT NULL,
    tipo_moneda NVARCHAR(3) NOT NULL,
    fecha_emision DATE DEFAULT GETDATE(),
    hora_emision TIME DEFAULT GETDATE(),
    empresa_ruc NVARCHAR(11) NOT NULL,
    razon_social NVARCHAR(50) NOT NULL,
    nombre_comercial NVARCHAR(200) NULL,
    urbanizacion NVARCHAR(200) NULL,
    distrito NVARCHAR(100) NULL,
    departamento NVARCHAR(100) NULL,
    email_empresa NVARCHAR(50) NULL,
    telefono_emp NVARCHAR(50) NULL,
    cliente_tipo_doc NVARCHAR(11) NOT NULL,
    monto_Oper_Gravadas DECIMAL(10, 2) DEFAULT 0.00 NULL,
    monto_Igv DECIMAL(10, 2) DEFAULT 0.00 NULL,
    valor_venta DECIMAL(10, 2) DEFAULT 0.00 NULL,
    sub_Total DECIMAL(10, 2) DEFAULT 0.00 NULL,
    monto_Imp_Venta DECIMAL(10, 2) DEFAULT 0.00 NULL,
    estado_Documento NVARCHAR(1) DEFAULT '0',
    manual BIT DEFAULT 0,
    pdf_url NVARCHAR(255) NULL,
    forma_pago INT NULL,
    legend_comprobante INT NULL,
    cliente INT NULL,
    usuario INT NULL,
    CONSTRAINT FK_tb_comprobante_forma_pago FOREIGN KEY (forma_pago) REFERENCES tb_forma_pago(id_formaPago) ON DELETE CASCADE,
    CONSTRAINT FK_tb_comprobante_legend FOREIGN KEY (legend_comprobante) REFERENCES tb_legend(id_legend) ON DELETE CASCADE,
    CONSTRAINT FK_tb_comprobante_cliente FOREIGN KEY (cliente) REFERENCES tb_cliente(id_cliente) ON DELETE CASCADE,
    CONSTRAINT FK_tb_comprobante_usuario FOREIGN KEY (usuario) REFERENCES tb_usuario(id_user) ON DELETE CASCADE
);




-- 12. Tabla: tb_detalle_comprobante
CREATE TABLE tb_detalle_comprobante (
    id_detalleComprobante INT IDENTITY(1,1) PRIMARY KEY,
    unidad NVARCHAR(6) NOT NULL,
    cantidad INT NOT NULL CHECK (cantidad >= 0),
    id_producto NVARCHAR(10) NOT NULL,
    descripcion NVARCHAR(255) NOT NULL,
    monto_valorUnitario FLOAT DEFAULT 0,
    igv_detalle FLOAT DEFAULT 0,
    fecha_emision DATE DEFAULT GETDATE(),
    hora_emision TIME DEFAULT GETDATE(),
    monto_Precio_Unitario DECIMAL(10, 2) DEFAULT 0,
    monto_Valor_Venta DECIMAL(10, 2) DEFAULT 0,
    comprobante INT NULL,
    producto INT NULL,
    CONSTRAINT FK_tb_detalle_comprobante_comprobante FOREIGN KEY (comprobante) REFERENCES tb_comprobante(id_comprobante) ON DELETE CASCADE,
    CONSTRAINT FK_tb_detalle_comprobante_producto FOREIGN KEY (producto) REFERENCES tb_producto(id_producto) ON DELETE CASCADE
);


-- 13. Crear tabla tb_tipoMovimiento
CREATE TABLE tb_tipoMovimiento (
    id_tipoMovimiento INT IDENTITY(1,1) PRIMARY KEY,
    descripcion NVARCHAR(50) NOT NULL
);

-- 14. Crear tabla tb_movimiento (usa FK de tb_sucursal, tb_usuario, tb_tipoMovimiento)
CREATE TABLE tb_movimiento (
    id_movimiento INT IDENTITY(1,1) PRIMARY KEY,
    referencia NVARCHAR(50) NULL,
    cant_total INT NOT NULL CHECK (cant_total >= 0),
    created_at DATETIME DEFAULT GETDATE(),
    updated_at DATETIME DEFAULT GETDATE(),
    sucursal INT NOT NULL,
    usuario INT NOT NULL,
    tipo_movimiento INT NOT NULL,
    CONSTRAINT FK_tb_movimiento_sucursal FOREIGN KEY (sucursal) REFERENCES tb_sucursal(id_sucursal) ON DELETE CASCADE,
    CONSTRAINT FK_tb_movimiento_usuario FOREIGN KEY (usuario) REFERENCES tb_usuario(id_user) ON DELETE CASCADE,
    CONSTRAINT FK_tb_movimiento_tipoMovimiento FOREIGN KEY (tipo_movimiento) REFERENCES tb_tipoMovimiento(id_tipoMovimiento) ON DELETE CASCADE
);


-- 15. Crear tabla tb_detalleMovimiento (usa FK de tb_detalle_comprobante, tb_producto y tb_movimiento)
CREATE TABLE tb_detalleMovimiento (
    id_detalleMovimiento INT IDENTITY(1,1) PRIMARY KEY,
    cantidad INT NOT NULL CHECK (cantidad >= 0),
    detalleComprobante INT NOT NULL,
    producto INT NOT NULL,
    movimiento INT NOT NULL,
    CONSTRAINT FK_tb_detalleMovimiento_detalleComprobante FOREIGN KEY (detalleComprobante) REFERENCES tb_detalle_comprobante(id_detalleComprobante) ON DELETE NO ACTION ON UPDATE NO ACTION,
    CONSTRAINT FK_tb_detalleMovimiento_producto FOREIGN KEY (producto) REFERENCES tb_producto(id_producto) ON DELETE NO ACTION ON UPDATE NO ACTION,
    CONSTRAINT FK_tb_detalleMovimiento_movimiento FOREIGN KEY (movimiento) REFERENCES tb_movimiento(id_movimiento) ON DELETE NO ACTION ON UPDATE NO ACTION
);



-- -----------------------
-- DATA INSERT SQL SERVER:
-- -----------------------

-- 1. Antes de insertar crear el super user.
INSERT INTO tb_rol (name_role) VALUES
('Asignar'),
('Administrador'),
('Ventas'),
('Almacen');

INSERT INTO tb_usuario (username, email, phone_number, password, name_role_id, created, modified, is_superuser, is_staff, is_active, date_joined) VALUES
('kevin1', 'kevin1@gmail.com', '+51999999991', 'admin123456', 2, GETDATE(), GETDATE(), 1, 1, 1, GETDATE()),
('Sebas2', 'sebas2@gmail.com', '+51999999992', 'admin123456', 3, GETDATE(), GETDATE(), 0, 0, 1, GETDATE());
-- Actualizar la contraseña en admin django y agregar un token.

INSERT INTO tb_sucursal (nombre, descripcion, telf_suc, correo_suc, direccion) VALUES
('Daryza S.A.C lurin', 'Panamericana Sur, luirn', '99293948', 'webmaster@daryza.com', 'km30, antigua panamericana Sur, luirn');

INSERT INTO tb_categoria (nombre_categoria, estado_categoria, created_at, update_at) VALUES
('Detergente Líquido', 1, GETDATE(), GETDATE()),
('Desinfectante', 1, GETDATE(), GETDATE()),
('Jabón Líquido', 1, GETDATE(), GETDATE()),
('Lejía', 1, GETDATE(), GETDATE()),
('Suavizante', 1, GETDATE(), GETDATE()),
('Limpiador Multiusos', 1, GETDATE(), GETDATE()),
('Desengrasante', 1, GETDATE(), GETDATE()),
('Aromatizador', 1, GETDATE(), GETDATE()),
('Cera Líquida', 1, GETDATE(), GETDATE()),
('Lavavajillas', 1, GETDATE(), GETDATE());

INSERT INTO tb_marca (nombre_marca, estado_marca, created_at, update_at) VALUES
('Daryza', 1, GETDATE(), GETDATE()),
('Clorox', 1, GETDATE(), GETDATE()),
('Lysol', 1, GETDATE(), GETDATE()),
('Mr. Clean', 1, GETDATE(), GETDATE()),
('Fabuloso', 1, GETDATE(), GETDATE()),
('Ajax', 1, GETDATE(), GETDATE()),
('Pine-Sol', 1, GETDATE(), GETDATE()),
('Windex', 1, GETDATE(), GETDATE()),
('Scrubbing Bubbles', 1, GETDATE(), GETDATE()),
('Seventh Generation', 1, GETDATE(), GETDATE());

INSERT INTO tb_unidadMedida (nombre_unidad, abreviacion, created_at, update_at) VALUES
('Litro', 'L', GETDATE(), GETDATE()),
('Mililitro', 'ml', GETDATE(), GETDATE()),
('Galón', 'gal', GETDATE(), GETDATE()),
('Onza', 'oz', GETDATE(), GETDATE()),
('Kilogramo', 'kg', GETDATE(), GETDATE()),
('Gramo', 'g', GETDATE(), GETDATE()),
('Unidad', 'u', GETDATE(), GETDATE()),
('Paquete', 'paq', GETDATE(), GETDATE()),
('Caja', 'caja', GETDATE(), GETDATE()),
('Botella', 'bot', GETDATE(), GETDATE());

INSERT INTO tb_tipoMovimiento (descripcion) VALUES
('Entrada'),
('Salida');
-- select * from tb_tipoMovimiento

INSERT INTO tb_cliente (nombre_clie, apellido_clie, dni_cliente, ruc_cliente, direccion_clie, razon_socialCliente, tipo_empresa, email_cliente, telefono_cliente) VALUES
('Carlos', 'Fernandez', '12345678', '20123456789', 'Av. Siempre Viva 123, Lima', 'Carlos Fernandez S.A.C.', 'Empresa Privada', 'carlos.fernandez@example.com', '+51987654321'),
('María', 'Gomez', '87654321', '20234567890', 'Calle Los Pinos 456, Arequipa', 'María Gomez EIRL', 'Pequeña Empresa', 'maria.gomez@example.com', '+51981234567'),
('Jorge', 'Ramirez', '23456789', '20345678901', 'Jr. Las Flores 789, Trujillo', 'JR Servicios Generales', 'Mediana Empresa', 'jorge.ramirez@example.com', '+51983456789'),
('Lucia', 'Lopez', '34567890', '20456789012', 'Av. El Sol 135, Cusco', 'Lucia Lopez Corp.', 'Empresa Familiar', 'lucia.lopez@example.com', '+51985678901');
-- select * from tb_cliente
