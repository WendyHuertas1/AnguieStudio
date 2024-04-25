CREATE DATABASE AngieStudio;
use AngieStudio;


CREATE TABLE cart_item (
  id int(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
  product_id int(11) NOT NULL,
  quantity int(11) NOT NULL
);

CREATE TABLE citas (
  id_cita int(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
  id_cliente int(11) NOT NULL,
  nombre varchar(100) NOT NULL,
  servicio varchar(100) NOT NULL,
  empleado_nombre varchar(100) NOT NULL,
  fecha date NOT NULL,
  hora time NOT NULL UNIQUE,
  motivo varchar(500) NOT NULL
) ;

CREATE TABLE entrada_productos (
  Id_Entrada int(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
  Id_Producto int(11) NOT NULL,
  Nombre varchar(100) NOT NULL,
  Cantidad int(11) NOT NULL,
  precio float NOT NULL,
  Fecha_Entrada date DEFAULT NULL
);

CREATE TABLE novedades (
  Id_Novedades int(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
  Id_Producto int(11) NOT NULL,
  Fecha_Ingreso date NOT NULL,
  Nombre varchar(100) NOT NULL,
  Marca varchar(200) NOT NULL,
  Precio decimal(10,2) NOT NULL,
  Fecha_Vencimiento date not null,
  Cantidad int(11) NOT NULL,
  Entrada int(11) NOT NULL,
  Salida int(11) NOT NULL,
  Tipo varchar(50) NOT NULL DEFAULT ''
);

CREATE TABLE product (
  id int(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
  title varchar(80) NOT NULL,
  description text NOT NULL,
  price float NOT NULL,
  image_path varchar(255) NOT NULL,
  active tinyint(1) NOT NULL DEFAULT 1,
  quantity int(11) NOT NULL
);


CREATE TABLE productos (
  Id int(11) NOT NULL PRIMARY KEY,
  Nombre varchar(100) NOT NULL,
  Fecha_Ingreso date DEFAULT NULL,
  Cantidad int(11) NOT NULL,
  Marca varchar(200) NOT NULL,
  precio float NOT NULL,
  Descripcion varchar(500) NOT NULL,
  Imagen varchar(255) NOT NULL,
  Fecha_vencimiento date DEFAULT NULL
);

DELIMITER $$
CREATE TRIGGER after_delete_producto AFTER DELETE ON productos FOR EACH ROW BEGIN
    INSERT INTO salida_productos (Id_Producto, Nombre, Cantidad, precio, Fecha_Salida)
    VALUES (OLD.Id, OLD.Nombre, OLD.Cantidad, OLD.precio, NOW());
END
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER after_insert_producto AFTER INSERT ON productos FOR EACH ROW BEGIN
    INSERT INTO entrada_productos (Id_Producto, Nombre, Cantidad, precio, Fecha_Entrada)
    VALUES (NEW.Id, NEW.Nombre, NEW.Cantidad, NEW.precio, NOW());

    INSERT INTO Novedades (Id_Producto, Fecha_Ingreso, Nombre, Marca, Precio, Fecha_Vencimiento, Cantidad, Entrada, Salida, Tipo)
    VALUES (NEW.Id, NEW.Fecha_Ingreso,NEW.Nombre, NEW.Marca, NEW.Precio, NEW.Fecha_Vencimiento,NEW.Cantidad, NEW.Cantidad, 0, 'Entrada');
END
$$
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

CREATE TABLE roles (
  id_rol int(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
  descripcion varchar(30) NOT NULL
);

INSERT INTO roles (id_rol, descripcion) VALUES
(1, 'Admin'),
(2, 'empleado'),
(3, 'cliente');

CREATE TABLE salida_productos (
  Id_Salida int(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
  Id_Producto int(11) NOT NULL,
  Nombre varchar(100) NOT NULL,
  Cantidad int(11) NOT NULL,
  precio float NOT NULL,
  Fecha_Salida date DEFAULT NULL
);

CREATE TABLE servicios (
  id_servicio int(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
  nombre varchar(100) NOT NULL,
  empleado varchar(100) NOT NULL
) ;

INSERT INTO servicios (id_servicio, nombre, empleado) VALUES
(1, 'Corte de cabello', '2'),
(2, 'Manicure', '2'),
(3, 'Maquillaje', '1'),
(4, 'Queratina', 'Dilan');

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
) ;

INSERT INTO usuarios (id, correo, password, id_rol, nombre, apellido, telefono, Dias_trabajo, Horario_trabajo, num_citas) VALUES
(1, 'wendyhuertas2408@gmail.com', '12', 1, 'Wendy', 'Huertas', 123123, NULL, NULL, 0),
(3, 'wendy2408@outlook.es', '1234', 3, 'Lorena', 'Hernandez', 423423, NULL, NULL, 0),
(4, 'alejandro@gmail.com', '456', 3, 'Alejandro', 'Martinez', 2147483647, NULL, NULL, 0),
(5, 'alejandro@gmail.com', '456', 3, 'Alejandro', 'Martinez', 2147483647, NULL, NULL, 0),
(6, 'dilanjimenez200@gmail.com', '1234567', 1, 'Dilan', 'Jimenez', 123124, NULL, NULL, 0),
(7, 'Yusep@gmail.com', '123', 2, 'Yusep', 'Yarce', 123123, 'Lunes a Viernes', '8:00 - 17:00', 0),
(8, 'dilanjimenez208@gmail.com', 'Dilan1', 3, 'Dilan Yusep', 'Jimenez Yarce', 1231, NULL, NULL, 0),
(9, 'dronlext@gmail.com', 'Oscar1', 3, 'Oscar', 'Sanabria', 312312, NULL, NULL, 0);


ALTER TABLE cart_item
  ADD CONSTRAINT fk_cart_item_product FOREIGN KEY (product_id) REFERENCES product (id) ON DELETE CASCADE;