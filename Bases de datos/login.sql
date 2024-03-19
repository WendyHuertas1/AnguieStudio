CREATE DATABASE login;
USE login;


CREATE TABLE `entrada_productos` (
  `Id_Entrada` int(11) NOT NULL,
  `Id_Producto` int(11) NOT NULL,
  `Nombre` varchar(100) NOT NULL,
  `Cantidad` int(11) NOT NULL,
  `precio` float NOT NULL,
  `Fecha_Entrada` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `entrada_productos`
--

INSERT INTO `entrada_productos` (`Id_Entrada`, `Id_Producto`, `Nombre`, `Cantidad`, `precio`, `Fecha_Entrada`) VALUES
(1, 1, 'asd', 12, 1232, '2024-03-18'),
(2, 2, 'Uñas', 100, 1000, '2024-03-18'),
(3, 3, 'Dilan', 100, 100, '2024-03-18');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `novedades`
--

CREATE TABLE `novedades` (
  `Id_Novedades` int(11) NOT NULL,
  `Id_Producto` int(11) NOT NULL,
  `fecha` date NOT NULL,
  `Nombre` varchar(100) NOT NULL,
  `Cantidad` int(11) NOT NULL,
  `Entrada` int(11) NOT NULL,
  `Salida` int(11) NOT NULL,
  `Tipo` varchar(50) NOT NULL DEFAULT ''
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `novedades`
--

INSERT INTO `novedades` (`Id_Novedades`, `Id_Producto`, `fecha`, `Nombre`, `Cantidad`, `Entrada`, `Salida`, `Tipo`) VALUES
(1, 1, '2024-03-18', 'asd', 12, 12, 0, 'Entrada'),
(2, 1, '2024-03-18', 'asd', 7, 0, 7, 'Salida'),
(3, 2, '2024-03-18', 'Uñas', 100, 100, 0, 'Entrada'),
(4, 2, '2024-03-18', 'Uñas', 50, 0, 50, 'Salida'),
(5, 2, '2024-03-18', 'Uñas', 25, 0, 25, 'Salida'),
(6, 3, '2024-03-18', 'Dilan', 100, 100, 0, 'Entrada'),
(7, 3, '2024-03-18', 'Dilan', 10, 0, 10, 'Salida');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `productos`
--

CREATE TABLE `productos` (
  `Id` int(11) NOT NULL,
  `Nombre` varchar(100) NOT NULL,
  `Cantidad` int(11) NOT NULL,
  `Marca` varchar(200) NOT NULL,
  `precio` float NOT NULL,
  `Descripcion` varchar(500) NOT NULL,
  `Fecha_vencimiento` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `productos`
--

INSERT INTO `productos` (`Id`, `Nombre`, `Cantidad`, `Marca`, `precio`, `Descripcion`, `Fecha_vencimiento`) VALUES
(3, 'Dilan', 90, 'esika', 1345, 'ad', '2024-03-20');

--
-- Disparadores `productos`
--
DELIMITER $$
CREATE TRIGGER `after_delete_producto` AFTER DELETE ON `productos` FOR EACH ROW BEGIN
    INSERT INTO salida_productos (Id_Producto, Nombre, Cantidad, precio, Fecha_Salida)
    VALUES (OLD.Id, OLD.Nombre, OLD.Cantidad, OLD.precio, NOW());
END
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `after_insert_producto` AFTER INSERT ON `productos` FOR EACH ROW BEGIN
    INSERT INTO entrada_productos (Id_Producto, Nombre, Cantidad, precio, Fecha_Entrada)
    VALUES (NEW.Id, NEW.Nombre, NEW.Cantidad, NEW.precio, NOW());

    INSERT INTO Novedades (Id_Producto, fecha, Nombre, Cantidad, Entrada, Salida, Tipo)
    VALUES (NEW.Id, NOW(), NEW.Nombre, NEW.Cantidad, NEW.Cantidad, 0, 'Entrada');
END
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `after_update_producto` AFTER UPDATE ON `productos` FOR EACH ROW BEGIN
    DECLARE cantidad_anterior INT;
    DECLARE diferencia_cantidad INT;
    
    SET cantidad_anterior = OLD.Cantidad;
    SET diferencia_cantidad = NEW.Cantidad - cantidad_anterior;

    IF diferencia_cantidad < 0 THEN
        INSERT INTO Novedades (Id_Producto, fecha, Nombre, Cantidad, Entrada, Salida, Tipo)
        VALUES (NEW.Id, NOW(), NEW.Nombre, ABS(diferencia_cantidad), 0, ABS(diferencia_cantidad), 'Salida');
    END IF;
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `roles`
--

CREATE TABLE `roles` (
  `id_rol` int(11) NOT NULL,
  `descripcion` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `roles`
--

INSERT INTO `roles` (`id_rol`, `descripcion`) VALUES
(1, 'Admin'),
(2, 'empleado'),
(3, 'cliente');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `salida_productos`
--

CREATE TABLE `salida_productos` (
  `Id_Salida` int(11) NOT NULL,
  `Id_Producto` int(11) NOT NULL,
  `Nombre` varchar(100) NOT NULL,
  `Cantidad` int(11) NOT NULL,
  `precio` float NOT NULL,
  `Fecha_Salida` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `salida_productos`
--

INSERT INTO `salida_productos` (`Id_Salida`, `Id_Producto`, `Nombre`, `Cantidad`, `precio`, `Fecha_Salida`) VALUES
(1, 1, 'asd', 5, 166, '2024-03-18'),
(2, 2, 'Uñas', 25, 123, '2024-03-18');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id` int(11) NOT NULL,
  `correo` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL,
  `id_rol` int(11) NOT NULL,
  `nombre` varchar(100) DEFAULT NULL,
  `apellido` varchar(100) DEFAULT NULL,
  `telefono` int(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id`, `correo`, `password`, `id_rol`, `nombre`, `apellido`, `telefono`) VALUES
(1, 'wendyhuertas2408@gmail.com', '12', 1, NULL, NULL, NULL),
(2, 'dilanjimenez208@gmail.com', '123', 2, NULL, NULL, NULL),
(3, 'wendy2408@outlook.es', '1234', 3, NULL, NULL, NULL),
(5, 'alejandro@gmail.com', '456', 3, 'Alejandro', 'Martinez', 2147483647),
(6, 'alejandro@gmail.com', '456', 3, 'Alejandro', 'Martinez', 2147483647);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `entrada_productos`
--
ALTER TABLE `entrada_productos`
  ADD PRIMARY KEY (`Id_Entrada`);

--
-- Indices de la tabla `novedades`
--
ALTER TABLE `novedades`
  ADD PRIMARY KEY (`Id_Novedades`);

--
-- Indices de la tabla `productos`
--
ALTER TABLE `productos`
  ADD PRIMARY KEY (`Id`);

--
-- Indices de la tabla `roles`
--
ALTER TABLE `roles`
  ADD PRIMARY KEY (`id_rol`);

--
-- Indices de la tabla `salida_productos`
--
ALTER TABLE `salida_productos`
  ADD PRIMARY KEY (`Id_Salida`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_rol` (`id_rol`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `entrada_productos`
--
ALTER TABLE `entrada_productos`
  MODIFY `Id_Entrada` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `novedades`
--
ALTER TABLE `novedades`
  MODIFY `Id_Novedades` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT de la tabla `productos`
--
ALTER TABLE `productos`
  MODIFY `Id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `roles`
--
ALTER TABLE `roles`
  MODIFY `id_rol` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `salida_productos`
--
ALTER TABLE `salida_productos`
  MODIFY `Id_Salida` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;
