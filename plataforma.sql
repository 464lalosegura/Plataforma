-- phpMyAdmin SQL Dump
-- version 3.5.1
-- http://www.phpmyadmin.net
--
-- Servidor: localhost
-- Tiempo de generación: 06-12-2024 a las 00:30:30
-- Versión del servidor: 5.5.24-log
-- Versión de PHP: 5.4.3

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Base de datos: `plataforma`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `almacen`
--

CREATE TABLE IF NOT EXISTS `almacen` (
  `ID_Almacen` int(11) NOT NULL AUTO_INCREMENT,
  `Reporte` text NOT NULL,
  PRIMARY KEY (`ID_Almacen`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=2 ;

--
-- Volcado de datos para la tabla `almacen`
--

INSERT INTO `almacen` (`ID_Almacen`, `Reporte`) VALUES
(1, 'ALMACEN_PRINCIPAL');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `categoria`
--

CREATE TABLE IF NOT EXISTS `categoria` (
  `ID_Categoria` int(11) NOT NULL AUTO_INCREMENT,
  `Nombre` varchar(255) NOT NULL,
  PRIMARY KEY (`ID_Categoria`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=9 ;

--
-- Volcado de datos para la tabla `categoria`
--

INSERT INTO `categoria` (`ID_Categoria`, `Nombre`) VALUES
(1, 'Granos y cereales'),
(2, 'Conservas y enlatados'),
(3, 'Lacteos'),
(4, 'Bebidas'),
(5, 'Higiene Personal'),
(6, 'Detergentes'),
(7, 'Desinfectantes'),
(8, 'Insecticidas');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `direccion`
--

CREATE TABLE IF NOT EXISTS `direccion` (
  `ID_Direccion` int(11) NOT NULL AUTO_INCREMENT,
  `Calle` varchar(255) NOT NULL,
  `Numero` varchar(50) NOT NULL,
  `Colonia` varchar(255) NOT NULL,
  `Localidad` varchar(255) NOT NULL,
  `CP` varchar(10) NOT NULL,
  PRIMARY KEY (`ID_Direccion`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=7 ;

--
-- Volcado de datos para la tabla `direccion`
--

INSERT INTO `direccion` (`ID_Direccion`, `Calle`, `Numero`, `Colonia`, `Localidad`, `CP`) VALUES
(1, 'las piedras', '23', 'san jeronimo', 'zoquiapan', '56'),
(2, 'las piedras', '23', 'san jeronimo', 'zoquiapan', '56'),
(3, 'arboledas', 's/n', 'el temazcal', 'vigastepec', '59'),
(6, 'arboledas', 's/n', 'el temazcal', 'vigastepec', '59');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `entrada_salida`
--

CREATE TABLE IF NOT EXISTS `entrada_salida` (
  `ID_EntradaSalida` int(11) NOT NULL AUTO_INCREMENT,
  `Tipo` enum('entrada','salida') NOT NULL,
  `Fecha` date NOT NULL,
  `Cantidad` int(11) NOT NULL,
  `ID_Producto` int(11) NOT NULL,
  `ID_Almacen` int(11) NOT NULL,
  PRIMARY KEY (`ID_EntradaSalida`),
  KEY `ID_Producto` (`ID_Producto`),
  KEY `ID_Almacen` (`ID_Almacen`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `pedido`
--

CREATE TABLE IF NOT EXISTS `pedido` (
  `ID_Pedido` int(11) NOT NULL AUTO_INCREMENT,
  `Fecha` date NOT NULL,
  `Estado` varchar(50) NOT NULL,
  `Tipo` varchar(50) NOT NULL,
  `ID_Usuario` int(11) NOT NULL,
  PRIMARY KEY (`ID_Pedido`),
  KEY `ID_Usuario` (`ID_Usuario`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=5 ;

--
-- Volcado de datos para la tabla `pedido`
--

INSERT INTO `pedido` (`ID_Pedido`, `Fecha`, `Estado`, `Tipo`, `ID_Usuario`) VALUES
(3, '2024-10-10', 'pendiente', 'envio', 6),
(4, '2024-10-02', 'pendiente', 'envio', 6);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `pedido_producto`
--

CREATE TABLE IF NOT EXISTS `pedido_producto` (
  `ID_Pedido` int(11) NOT NULL,
  `ID_Producto` int(11) NOT NULL,
  `Cantidad` int(11) NOT NULL,
  PRIMARY KEY (`ID_Pedido`,`ID_Producto`),
  KEY `ID_Producto` (`ID_Producto`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `producto`
--

CREATE TABLE IF NOT EXISTS `producto` (
  `ID_Producto` int(11) NOT NULL AUTO_INCREMENT,
  `Descripcion` varchar(255) NOT NULL,
  `Precio` decimal(10,2) NOT NULL,
  `Cantidad` int(11) NOT NULL,
  `ID_Categoria` int(11) NOT NULL,
  `ID_Tienda` int(11) NOT NULL,
  PRIMARY KEY (`ID_Producto`),
  KEY `ID_Categoria` (`ID_Categoria`),
  KEY `ID_Tienda` (`ID_Tienda`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=69 ;

--
-- Volcado de datos para la tabla `producto`
--

INSERT INTO `producto` (`ID_Producto`, `Descripcion`, `Precio`, `Cantidad`, `ID_Categoria`, `ID_Tienda`) VALUES
(6, 'Aceite vegetal comestible "Patrona" de 1 lt ', '35.00', 150, 2, 3),
(7, 'Agua purificada "Pascual" de 1.5lt ', '12.00', 100, 4, 2),
(8, 'Arroz Envasado bolsa con 1kg ', '38.00', 89, 1, 3),
(9, 'Atún en aceite "El Dorado" contenido 130gr ', '13.00', 26, 2, 3),
(10, 'Avena natural en bolsa "El Granvita" 400gr', '12.00', 43, 1, 3),
(11, 'Azúcar Estándar Envasado 1kg ', '17.50', 23, 1, 3),
(12, 'Blanqueador "Cloralex" 950ml ', '13.50', 25, 7, 3),
(13, 'Café soluble "Nescafé Clásico" 120gr', '70.00', 56, 4, 2),
(14, 'Chiles jalapeños Enteros "La Costeña" 220gr ', '14.50', 63, 2, 3),
(15, 'Chocolate de mesa en polvo bolsa "Chocomilk" 540gr ', '80.00', 56, 3, 3),
(16, 'Crema Dental "Colgate" 50ml', '19.30', 89, 5, 3),
(17, 'Detergente en polvo bolsa "Foca" 1kg', '33.00', 25, 6, 2),
(18, 'Ensalada de Verduras "La Costeña" 220gr ', '12.70', 66, 2, 3),
(39, 'Frijol Envasado 1kg', '60.00', 59, 1, 3),
(40, 'Galletas de animalitos "Cuétara" 800gr ', '53.50', 46, 3, 2),
(41, 'Galletas Marías "Cuétara" 160gr ', '10.50', 20, 3, 3),
(42, 'Gelatinas "D´gari" 120gr ', '13.50', 32, 3, 2),
(43, 'Harina de Trigo "Selecta" 1kg', '15.90', 15, 1, 3),
(44, 'Hojuela de Maíz Azucarada "Golden Foods" 500gr ', '18.50', 74, 3, 3),
(45, 'Insecticida Aerosol Multiusos "Oko" 230ml ', '54.50', 30, 8, 3),
(46, 'Jabón de Lavandería "Zote" 400gr ', '42.90', 34, 6, 3),
(47, 'Jabón de tocador "Rosa Venus" 150gr', '10.50', 58, 6, 3),
(48, 'Jugo Tetrabrik "Jumex" 1lt', '28.50', 46, 4, 3),
(49, 'Leche Entera Natural "Alpura" 1lt ', '33.90', 16, 3, 3),
(50, 'Leche Evaporada "Carnation" 360gr', '20.50', 85, 3, 2),
(51, 'Lenteja Envasada 500gr ', '29.50', 45, 1, 3),
(52, 'Limpiador Líquido "Pinol" 1lt', '31.50', 64, 7, 3),
(53, 'Maíz blanco envasado 1kg ', '35.00', 75, 1, 3),
(54, 'Pañales desechables "KKBB Absorsec" paquete con 14 piezas ', '54.90', 45, 5, 3),
(55, 'Papel Higiénico "Premier" paquete con 4 rollos ', '26.80', 78, 5, 2),
(56, 'Pasta para sopa "Italpasta" 200gr', '9.50', 56, 2, 2),
(57, 'Puré de tomate "La Costeña" 220gr', '9.93', 110, 2, 3),
(58, 'Sal de mesa "La Fina" 1kg ', '18.20', 32, 1, 3),
(64, 'Sardina enlatada "Fresh Label" 425gr', '39.90', 46, 2, 2),
(65, 'Servilletas "Pétalo" Contenido con 100 piezas', '18.90', 60, 5, 3),
(66, 'Soya texturizada "Nutricasa" 330gr', '15.50', 23, 2, 3),
(67, 'Suavizante de telas "Ensueño" 850ml ', '25.40', 78, 6, 3),
(68, 'Toallas sanitarias "Saba" paquete con 8 piezas', '28.30', 100, 5, 2);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `reclamo`
--

CREATE TABLE IF NOT EXISTS `reclamo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `usuario_id` int(11) NOT NULL,
  `producto_id` int(11) NOT NULL,
  `fecha` date NOT NULL,
  `descripcion` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=3 ;

--
-- Volcado de datos para la tabla `reclamo`
--

INSERT INTO `reclamo` (`id`, `usuario_id`, `producto_id`, `fecha`, `descripcion`) VALUES
(1, 3, 10, '2024-12-05', 'su tapa se cayo'),
(2, 3, 13, '2024-12-05', 'al parececer el cafe se le paso la caducidad\r\n');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tienda`
--

CREATE TABLE IF NOT EXISTS `tienda` (
  `ID_Tienda` int(11) NOT NULL AUTO_INCREMENT,
  `Nombre` varchar(255) NOT NULL,
  `Direccion` varchar(255) NOT NULL,
  `Telefono` varchar(20) NOT NULL,
  PRIMARY KEY (`ID_Tienda`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=4 ;

--
-- Volcado de datos para la tabla `tienda`
--

INSERT INTO `tienda` (`ID_Tienda`, `Nombre`, `Direccion`, `Telefono`) VALUES
(2, 'zoquiapam', 'las arboledas ', '235648971'),
(3, 'vigastepec', 'vigastepecx', '2364568789');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuario`
--

CREATE TABLE IF NOT EXISTS `usuario` (
  `ID_Usuario` int(11) NOT NULL AUTO_INCREMENT,
  `Nombre` varchar(255) NOT NULL,
  `Correo` varchar(255) NOT NULL,
  `Contraseña` varchar(255) NOT NULL,
  `ID_Direccion` int(11) NOT NULL,
  PRIMARY KEY (`ID_Usuario`),
  UNIQUE KEY `Correo` (`Correo`),
  KEY `ID_Direccion` (`ID_Direccion`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=7 ;

--
-- Volcado de datos para la tabla `usuario`
--

INSERT INTO `usuario` (`ID_Usuario`, `Nombre`, `Correo`, `Contraseña`, `ID_Direccion`) VALUES
(2, 'pedro martinez rodriguez', 'pedro.21@gmail.com', 'scrypt:32768:8:1$y5PZJhzAK4NaYvPs$c8d1e3c592abec980c0d57c8dcf884446ed5759c447981f0d6deabe92c8553cc001292d044592cf7c239400037fd4cc5f4ce5aeac85c03a3fa1018a0d07b9eaf', 6),
(3, 'romel perez perez', 'rom@gmail.com', 'scrypt:32768:8:1$n52UcMl8GyBppFy9$b57329e21af0253e11f30214499058b8f143e45b0ecfcd0b8ed761aad5ccc2e650fdfc4284d46ed2665baedf199d3fbfd043481a2ec73681ccbc3d6183dc997a', 3),
(6, 'javier solis ', 'javiX.p@outlook.com', 'scrypt:32768:8:1$lHyxuywYctQOJ8Hb$f4d02c07c7b6a28a23724a0ec632e0b1ea80c8f1802ffb29fce93f555091b5aafb3ce6dd14c2bfdf0c7c2fb1f9d15110f2d4cefb197ad48009b5e098ca1e58d8', 3);

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `entrada_salida`
--
ALTER TABLE `entrada_salida`
  ADD CONSTRAINT `entrada_salida_ibfk_1` FOREIGN KEY (`ID_Producto`) REFERENCES `producto` (`ID_Producto`) ON DELETE CASCADE,
  ADD CONSTRAINT `entrada_salida_ibfk_2` FOREIGN KEY (`ID_Almacen`) REFERENCES `almacen` (`ID_Almacen`) ON DELETE CASCADE;

--
-- Filtros para la tabla `pedido`
--
ALTER TABLE `pedido`
  ADD CONSTRAINT `pedido_ibfk_1` FOREIGN KEY (`ID_Usuario`) REFERENCES `usuario` (`ID_Usuario`) ON DELETE CASCADE;

--
-- Filtros para la tabla `pedido_producto`
--
ALTER TABLE `pedido_producto`
  ADD CONSTRAINT `pedido_producto_ibfk_1` FOREIGN KEY (`ID_Pedido`) REFERENCES `pedido` (`ID_Pedido`) ON DELETE CASCADE,
  ADD CONSTRAINT `pedido_producto_ibfk_2` FOREIGN KEY (`ID_Producto`) REFERENCES `producto` (`ID_Producto`) ON DELETE CASCADE;

--
-- Filtros para la tabla `producto`
--
ALTER TABLE `producto`
  ADD CONSTRAINT `producto_ibfk_1` FOREIGN KEY (`ID_Categoria`) REFERENCES `categoria` (`ID_Categoria`) ON DELETE CASCADE,
  ADD CONSTRAINT `producto_ibfk_2` FOREIGN KEY (`ID_Tienda`) REFERENCES `tienda` (`ID_Tienda`) ON DELETE CASCADE;

--
-- Filtros para la tabla `usuario`
--
ALTER TABLE `usuario`
  ADD CONSTRAINT `usuario_ibfk_1` FOREIGN KEY (`ID_Direccion`) REFERENCES `direccion` (`ID_Direccion`) ON DELETE CASCADE;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
