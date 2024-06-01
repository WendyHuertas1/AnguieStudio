CREATE DATABASE IF NOT EXISTS AngieStudio;
USE AngieStudio;

CREATE TABLE citas (
  id_cita int(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
  id_cliente int(11) NOT NULL,
  nombre varchar(100) NOT NULL,
  cedula varchar(100) NOT NULL,
  servicio varchar(100) NOT NULL,
  precio decimal(10,2) NOT NULL,
  empleado_nombre varchar(100) NOT NULL,
  fecha date NOT NULL,
  hora time NOT NULL UNIQUE,
  motivo varchar(500) NOT NULL
);

CREATE TABLE entrada_productos (
  Id_Entrada int(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
  Id_Producto int(11) NOT NULL,
  Nombre varchar(100) NOT NULL,
  Cantidad int(11) NOT NULL,
  Precio decimal(10,2) NOT NULL,
  Fecha_Entrada date DEFAULT NULL
);

CREATE TABLE novedades (
  Id_Novedades int(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
  Id_Producto int(11) NOT NULL,
  Fecha_Ingreso date NOT NULL,
  Nombre varchar(100) NOT NULL,
  Marca varchar(200) NOT NULL,
  Precio decimal(10,2) NOT NULL,
  Fecha_Vencimiento date NOT NULL,
  Cantidad int(11) NOT NULL,
  Entrada int(11) NOT NULL,
  Salida int(11) NOT NULL,
  Tipo varchar(50) NOT NULL DEFAULT ''
);

CREATE TABLE product (
  id int(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
  title varchar(80) NOT NULL,
  description text NOT NULL,
  price decimal(10,2) NOT NULL,
  image_path varchar(255) NOT NULL,
  active tinyint(1) NOT NULL DEFAULT 1,
  quantity int(11) NOT NULL
);

CREATE TABLE client (
  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL,
  apellidos VARCHAR(100) NOT NULL,
  direccion VARCHAR(255) NOT NULL,
  telefono VARCHAR(15) NOT NULL,
  correo VARCHAR(100) NOT NULL
);

CREATE TABLE usuarios (
  id int(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
  correo varchar(100) NOT NULL,
  password varchar(100) NOT NULL,
  id_rol int(11) NOT NULL,
  nombre varchar(100) DEFAULT NULL,
  apellido varchar(100) DEFAULT NULL,
  telefono int(20) DEFAULT NULL,
  Dias_trabajo varchar(100) DEFAULT NULL,
  Horario_trabajo varchar(100) DEFAULT NULL,
  num_citas int(11) DEFAULT 0
);

CREATE TABLE cart (
  id int(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
  product_id int(11) NOT NULL,
  title varchar(80) NOT NULL,
  image_path varchar(255) NOT NULL,
  price decimal(10,2) NOT NULL,
  quantity int(11) NOT NULL,
  total float NOT NULL,
  user_id int(11) NOT NULL,
  FOREIGN KEY (product_id) REFERENCES product(id),
  FOREIGN KEY (user_id) REFERENCES usuarios(id)
);

CREATE TABLE order_detail (
  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  client_id INT NOT NULL,
  product_id INT NOT NULL,
  product_name VARCHAR(255) NOT NULL,
  quantity INT NOT NULL,
  total decimal(10,2) NOT NULL,
  FOREIGN KEY (client_id) REFERENCES client(id),
  FOREIGN KEY (product_id) REFERENCES product(id)
);

CREATE TABLE productos (
  Id int(11) NOT NULL PRIMARY KEY,
  Nombre varchar(100) NOT NULL,
  Fecha_Ingreso date DEFAULT NULL,
  Cantidad int(11) NOT NULL,
  Marca varchar(200) NOT NULL,
  precio decimal(10,2) NOT NULL,
  Descripcion varchar(500) NOT NULL,
  Imagen varchar(255) NOT NULL,
  Fecha_vencimiento date DEFAULT NULL
);

CREATE TABLE roles (
  id_rol int(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
  descripcion varchar(30) NOT NULL
);

CREATE TABLE salida_productos (
  Id_Salida int(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
  Id_Producto int(11) NOT NULL,
  Nombre varchar(100) NOT NULL,
  Cantidad int(11) NOT NULL,
  precio decimal(10,2) NOT NULL,
  Fecha_Salida date DEFAULT NULL
);

CREATE TABLE servicios (
  id_servicio int(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
  nombre varchar(100) NOT NULL,
  precio decimal(10,2) NOT NULL,
  empleado varchar(100) NOT NULL
);

-- Insertar datos en las tablas roles y servicios
INSERT INTO roles (id_rol, descripcion) VALUES
(1, 'Admin'),
(2, 'empleado'),
(3, 'cliente');

INSERT INTO servicios (id_servicio, nombre, precio, empleado) VALUES
(1, 'Corte de cabello', 200000, '2'),
(2, 'Manicure', 200000, '2'),
(3, 'Maquillaje', 200000, '1'),
(4, 'Queratina', 200000, 'Dilan');

-- Insertar datos en la tabla usuarios
INSERT INTO usuarios (id, correo, password, id_rol, nombre, apellido, telefono, Dias_trabajo, Horario_trabajo, num_citas) VALUES
(1, 'wendyhuertas2408@gmail.com', '$2b$12$lELqE37evLpLq2efQ80DFOvYObJZQi6EIuvK5grBpb8w1vUhxwx9O', 1, 'Wendy', 'Huertas', 3201234567, NULL, NULL, 0),
(3, 'wendy2408@outlook.es', '$2b$12$yFrOZstwUoL2wk5hjvujiekdjA3BQd.UZTGpTCxMZIePcQ7nJ3eKu', 3, 'Lorena', 'Hernandez', 3109876543, NULL, NULL, 0),
(4, 'alejandro@gmail.com', '$2b$12$znuoUhTG08v7TERtJoQ.K.qKLkOJsWMXW/mDPa4z37Olu26WfszLC', 3, 'Alejandro', 'Martinez', 3008765432, NULL, NULL, 0),
(6, 'dilanjimenez200@gmail.com', '$2b$12$o80mdOiF5GMsO6Bua.VztO1gspIHqSSafy53q0cZRTP9rk3j697ii', 1, 'Dilan', 'Jimenez', 3152345678, NULL, NULL, 0),
(7, 'Yusep@gmail.com', '$2b$12$iErl9376WxZqz/y5fP6mve1YLW7H2w42jXkgP/9iaqBtBhQf61gu2', 2, 'Yusep', 'Yarce', 3043456789, 'Lunes a Viernes', '8:00 - 17:00', 0),
(8, 'dilanjimenez208@gmail.com', '$2b$12$fFOk6B4wndxaaaPfglk5deNBPTiSqZ5Kn.ixTOL.rwQ9sDIBWbMBa', 3, 'Dilan Yusep', 'Jimenez Yarce', 3184567890, NULL, NULL, 0),
(9, 'dronlext@gmail.com', '$2b$12$YVl.gB3PSLHUBNLuez7tfuumypLRsLVAnoMssVYnOL6fziNMdXxy2', 3, 'Oscar', 'Sanabria', 3017890123, NULL, NULL, 0),
(10, 'Diego@gmail.com', '$2b$12$7Gb5ZVviyyWN22bnZUsi/untZo2ywHlXfsbo8DPvVGrFNFFrYa8GK', 2, 'Diego', 'Vargaz', 3198901234, 'Lunes a viernes', '8:00 a 5:00', 0),
(11, 'Johan@gmail.com', '$2b$12$UtzSr.qMOD/jKD4HwvnX/uzqMP.COilrzna6BDKTMhb2az8Uz.9Jy', 2, 'Johan', 'Jimenez', 3115678901, 'Lunes a viernes', '8:00 a 5:00', 0),
(12, 'Carlos@gmail.com', '$2b$12$1xLieR8TIIjePWClcXFc3ebhbnFZPu4TtWrBcqDB4toXGK9uLqdT6', 2, 'Carlos', 'Sanchez', 3136789012, 'Lunes a viernes', '8:00 a 5:00', 0);

-- Crear los triggers
DELIMITER $$
CREATE TRIGGER after_delete_producto AFTER DELETE ON productos FOR EACH ROW 
BEGIN
    INSERT INTO salida_productos (Id_Producto, Nombre, Cantidad, precio, Fecha_Salida)
    VALUES (OLD.Id, OLD.Nombre, OLD.Cantidad, OLD.precio, NOW());
END$$
DELIMITER ;

DELIMITER $$
CREATE TRIGGER after_insert_producto AFTER INSERT ON productos FOR EACH ROW 
BEGIN
    INSERT INTO entrada_productos (Id_Producto, Nombre, Cantidad, precio, Fecha_Entrada)
    VALUES (NEW.Id, NEW.Nombre, NEW.Cantidad, NEW.precio, NOW());

    INSERT INTO Novedades (Id_Producto, Fecha_Ingreso, Nombre, Marca, Precio, Fecha_Vencimiento, Cantidad, Entrada, Salida, Tipo)
    VALUES (NEW.Id, NEW.Fecha_Ingreso, NEW.Nombre, NEW.Marca, NEW.Precio, NEW.Fecha_Vencimiento, NEW.Cantidad, NEW.Cantidad, 0, 'Entrada');
END$$
DELIMITER ;

DELIMITER $$
CREATE TRIGGER after_update_producto AFTER UPDATE ON productos FOR EACH ROW 
BEGIN
    DECLARE cantidad_anterior INT;
    DECLARE diferencia_cantidad INT;
    
    SET cantidad_anterior = OLD.Cantidad;
    SET diferencia_cantidad = NEW.Cantidad - cantidad_anterior;

    IF diferencia_cantidad < 0 THEN
        INSERT INTO Novedades (Id_Producto, Fecha_Ingreso, Nombre, Marca, Precio, Fecha_Vencimiento, Cantidad, Entrada, Salida, Tipo)
        VALUES (NEW.Id, NEW.Fecha_Ingreso, NEW.Nombre, NEW.Marca, NEW.Precio, NEW.Fecha_Vencimiento, ABS(diferencia_cantidad), OLD.Cantidad, ABS(diferencia_cantidad), 'Salida');
    END IF;
END$$
DELIMITER ;