-- =============================================================
-- Base de Datos: FlyMetrics
-- Sistema de Agendamiento de Servicios con Drones Agrícolas
-- Roles: cliente, tecnico, admin
-- =============================================================

CREATE DATABASE IF NOT EXISTS flymetrics_project
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE flymetrics_project;

-- =============================================================
-- 1. USUARIOS
-- =============================================================

CREATE TABLE usuarios (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    nombre VARCHAR(80) NOT NULL,
    apellido VARCHAR(80) NOT NULL,
    email VARCHAR(150) NOT NULL,
    telefono VARCHAR(20) DEFAULT NULL,
    password_hash VARCHAR(255) NOT NULL,
    rol ENUM('cliente', 'tecnico', 'admin') NOT NULL DEFAULT 'cliente',
    activo TINYINT(1) NOT NULL DEFAULT 1,
    creado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    actualizado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    PRIMARY KEY (id),
    UNIQUE KEY uq_usuarios_email (email)
) ENGINE = InnoDB;

-- =============================================================
-- 2. TECNICOS
-- =============================================================

CREATE TABLE tecnicos (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    usuario_id INT UNSIGNED NOT NULL,
    especialidad VARCHAR(120) DEFAULT NULL,
    bio TEXT DEFAULT NULL,
    tarifa_hora DECIMAL(10, 2) DEFAULT NULL,
    disponible TINYINT(1) NOT NULL DEFAULT 1,

    PRIMARY KEY (id),
    UNIQUE KEY uq_tecnico_usuario (usuario_id),

    CONSTRAINT fk_tecnico_usuario
        FOREIGN KEY (usuario_id)
        REFERENCES usuarios(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE = InnoDB;

-- =============================================================
-- 3. CULTIVOS
-- =============================================================

CREATE TABLE cultivos (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    usuario_id INT UNSIGNED NOT NULL,
    nombre_cultivo VARCHAR(120) NOT NULL,

    tipo_cultivo ENUM(
        'arroz',
        'maiz',
        'cafe',
        'cana',
        'palma',
        'hortalizas',
        'frutales',
        'otro'
    ) NOT NULL DEFAULT 'otro',

    hectareas DECIMAL(10, 2) DEFAULT NULL,
    ubicacion VARCHAR(255) DEFAULT NULL,
    latitud DECIMAL(10, 7) DEFAULT NULL,
    longitud DECIMAL(10, 7) DEFAULT NULL,
    notas TEXT DEFAULT NULL,

    PRIMARY KEY (id),

    CONSTRAINT fk_cultivo_usuario
        FOREIGN KEY (usuario_id)
        REFERENCES usuarios(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE = InnoDB;

-- =============================================================
-- 4. DRONES
-- =============================================================

CREATE TABLE drones (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    modelo VARCHAR(100) NOT NULL,
    matricula VARCHAR(60) NOT NULL,
    capacidad_lt DECIMAL(6, 2) DEFAULT NULL COMMENT 'Capacidad del tanque en litros',

    estado ENUM(
        'disponible',
        'en_uso',
        'mantenimiento',
        'inactivo'
    ) NOT NULL DEFAULT 'disponible',

    ultimo_mantenimiento DATE DEFAULT NULL,

    PRIMARY KEY (id),
    UNIQUE KEY uq_dron_matricula (matricula)
) ENGINE = InnoDB;

-- =============================================================
-- 5. SERVICIOS
-- =============================================================

CREATE TABLE servicios (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    nombre VARCHAR(120) NOT NULL,
    descripcion TEXT DEFAULT NULL,
    precio_base DECIMAL(12, 2) NOT NULL DEFAULT 0.00,
    duracion_min INT UNSIGNED DEFAULT 60
        COMMENT 'Duración estimada en minutos',
    activo TINYINT(1) NOT NULL DEFAULT 1,

    PRIMARY KEY (id)
) ENGINE = InnoDB;

-- =============================================================
-- 6. DISPONIBILIDAD
-- =============================================================

CREATE TABLE disponibilidad (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    tecnico_id INT UNSIGNED NOT NULL,
    fecha DATE NOT NULL,
    hora_inicio TIME NOT NULL,
    hora_fin TIME NOT NULL,
    disponible TINYINT(1) NOT NULL DEFAULT 1,

    PRIMARY KEY (id),

    CONSTRAINT fk_disponibilidad_tecnico
        FOREIGN KEY (tecnico_id)
        REFERENCES tecnicos(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE = InnoDB;

-- =============================================================
-- 7. CITAS
-- =============================================================

CREATE TABLE citas (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,

    usuario_id INT UNSIGNED NOT NULL
        COMMENT 'Cliente que agenda',

    tecnico_id INT UNSIGNED NOT NULL,
    cultivo_id INT UNSIGNED NOT NULL,
    drone_id INT UNSIGNED DEFAULT NULL,
    servicio_id INT UNSIGNED NOT NULL,

    fecha DATE NOT NULL,
    hora_inicio TIME NOT NULL,
    hora_fin TIME NOT NULL,

    estado ENUM(
        'pendiente',
        'confirmada',
        'en_curso',
        'completada',
        'cancelada',
        'no_asistio'
    ) NOT NULL DEFAULT 'pendiente',

    notas_cliente TEXT DEFAULT NULL,
    notas_tecnico TEXT DEFAULT NULL,
    creado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (id),

    CONSTRAINT fk_cita_usuario
        FOREIGN KEY (usuario_id)
        REFERENCES usuarios(id),

    CONSTRAINT fk_cita_tecnico
        FOREIGN KEY (tecnico_id)
        REFERENCES tecnicos(id),

    CONSTRAINT fk_cita_cultivo
        FOREIGN KEY (cultivo_id)
        REFERENCES cultivos(id),

    CONSTRAINT fk_cita_drone
        FOREIGN KEY (drone_id)
        REFERENCES drones(id),

    CONSTRAINT fk_cita_servicio
        FOREIGN KEY (servicio_id)
        REFERENCES servicios(id)
) ENGINE = InnoDB;

-- =============================================================
-- 8. PAGOS
-- =============================================================

CREATE TABLE pagos (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    cita_id INT UNSIGNED NOT NULL,
    monto DECIMAL(12, 2) NOT NULL,

    metodo_pago ENUM(
        'efectivo',
        'transferencia',
        'tarjeta',
        'nequi',
        'daviplata',
        'otro'
    ) NOT NULL DEFAULT 'efectivo',

    estado_pago ENUM(
        'pendiente',
        'pagado',
        'reembolsado',
        'fallido'
    ) NOT NULL DEFAULT 'pendiente',

    referencia VARCHAR(120) DEFAULT NULL
        COMMENT 'Número de comprobante',

    pagado_en TIMESTAMP DEFAULT NULL,

    PRIMARY KEY (id),

    CONSTRAINT fk_pago_cita
        FOREIGN KEY (cita_id)
        REFERENCES citas(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
) ENGINE = InnoDB;