CREATE DATABASE IF NOT EXISTS `netflix_upp`;
USE `netflix_upp`;

DROP TABLE IF EXISTS `peliculas`;
DROP TABLE IF EXISTS `token`;
DROP TABLE IF EXISTS `usuarios`;
DROP TABLE IF EXISTS `generos`;
DROP TABLE IF EXISTS `planes`;

CREATE TABLE `usuarios` (
  `idUsuario` INT AUTO_INCREMENT PRIMARY KEY,
  `nombre` VARCHAR(100) NOT NULL,
  `usuario` VARCHAR(50) NOT NULL UNIQUE,
  `correo` VARCHAR(100) NOT NULL UNIQUE,
  `password` VARCHAR(255) NOT NULL,
  `lActivo` TINYINT DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 2. Tabla de Tokens
CREATE TABLE `token` (
  `idToken` INT AUTO_INCREMENT PRIMARY KEY,
  `idUsuario` INT NOT NULL,
  `cToken` VARCHAR(100) NOT NULL,
  `dFecha` DATETIME NOT NULL,
  FOREIGN KEY (`idUsuario`) REFERENCES `usuarios` (`idUsuario`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 3. Tabla de Géneros (Catálogo 2)
CREATE TABLE `generos` (
  `idGenero` INT AUTO_INCREMENT PRIMARY KEY,
  `nombre` VARCHAR(50) NOT NULL UNIQUE,
  `descripcion` TEXT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 4. Tabla de Planes de Suscripción (Catálogo 3)
CREATE TABLE `planes` (
  `idPlan` INT AUTO_INCREMENT PRIMARY KEY,
  `nombre` VARCHAR(50) NOT NULL UNIQUE,
  `precio` DECIMAL(10,2) NOT NULL,
  `calidad` VARCHAR(20) NOT NULL,
  `pantallas` INT NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 5. Tabla de Películas (Catálogo 4)
CREATE TABLE `peliculas` (
  `idPelicula` INT AUTO_INCREMENT PRIMARY KEY,
  `titulo` VARCHAR(150) NOT NULL,
  `sinopsis` TEXT,
  `anio` INT NOT NULL,
  `duracion` VARCHAR(20) NOT NULL,
  `imagen_url` VARCHAR(255),
  `idGenero` INT,
  FOREIGN KEY (`idGenero`) REFERENCES `generos` (`idGenero`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Inserción de datos iniciales / semilla
INSERT INTO `usuarios` (`nombre`, `usuario`, `correo`, `password`, `lActivo`) VALUES
('Oscar', 'Oscar', 'oscar@upp.edu.mx', '7777', 1),
('Nidia Villanueva', 'nidia', 'nidia@upp.edu.mx', '1234', 1);

INSERT INTO `generos` (`nombre`, `descripcion`) VALUES
('Acción', 'Películas de acción intensas con persecuciones, explosiones y mucha adrenalina.'),
('Comedia', 'Películas divertidas con humor para reír en familia o con amigos.'),
('Terror', 'Películas de miedo, suspenso y terror psicológico.'),
('Ciencia Ficción', 'Exploración espacial, viajes en el tiempo y tecnologías del futuro.'),
('Romance', 'Películas que abordan relaciones amorosas y dramas sentimentales.');

INSERT INTO `planes` (`nombre`, `precio`, `calidad`, `pantallas`) VALUES
('Básico', 139.00, 'SD (480p)', 1),
('Estándar', 219.00, 'HD (1080p)', 2),
('Premium', 299.00, 'Ultra HD (4K+HDR)', 4);

INSERT INTO `peliculas` (`titulo`, `sinopsis`, `anio`, `duracion`, `imagen_url`, `idGenero`) VALUES
('El Origen', 'Un ladrón que roba secretos corporativos a través del uso de la tecnología para compartir sueños, recibe la tarea inversa de implantar una idea en la mente de un director ejecutivo.', 2010, '148 min', 'https://images.unsplash.com/photo-1536440136628-849c177e76a1?w=500', 4),
('Matrix', 'Un hacker informático aprende de misteriosos rebeldes sobre la verdadera naturaleza de su realidad y su papel en la guerra contra sus controladores.', 1999, '136 min', 'https://images.unsplash.com/photo-1478760329108-5c3ed9d495a0?w=500', 4),
('¿Qué pasó ayer?', 'Tres amigos se despiertan después de una despedida de soltero en Las Vegas, sin ningún recuerdo de la noche anterior y con el novio desaparecido.', 2009, '100 min', 'https://images.unsplash.com/photo-1517604931442-7e0c8ed2963c?w=500', 2),
('El Conjuro', 'Los investigadores de fenómenos paranormales Ed y Lorraine Warren trabajan para ayudar a una familia aterrorizada por una presencia oscura en su granja.', 2013, '112 min', 'https://images.unsplash.com/photo-1509248961158-e54f6934749c?w=500', 3);
