create database angiestudio;
use angiestudio;

create table roles (
  id_rol INT NOT NULL PRIMARY  KEY,
  nombre VARCHAR(50)
);

CREATE TABLE usuarios (
  Id_usuario int(11) DEFAULT NULL,
  Nombre varchar(60) DEFAULT NULL,
  Apellido varchar(60) DEFAULT NULL,
  Cedula int(11) DEFAULT NULL,
  Telefono varchar(60) DEFAULT NULL,
  Correo varchar(60) DEFAULT NULL,
  rol_id int NOT NULL,
  password varchar(60) DEFAULT NULL,
  PRIMARY KEY (Id_usuario),
  FOREIGN KEY(rol_id) REFERENCES roles(id_rol)
);

CREATE TABLE citas (
  Idservicio int(11) DEFAULT NULL,
  TipoServicio varchar(30) DEFAULT NULL,
  IdAgendamiento int(11) NOT NULL,
  EstadoCita tinyint(1) DEFAULT NULL,
  HoraFecha date DEFAULT NULL,
  rol_id int NOT NULL,,
  PRIMARY KEY (IdAgendamiento),
  FOREIGN KEY (rol_id) REFERENCES roles (rol_id);
);

CREATE TABLE agendamiento (
  IdAgendamiento int(11) DEFAULT NULL AUTO_INCREMENT,
  FechaHora date DEFAULT NULL,
  NombreServicio varchar(30) DEFAULT NULL,
  DocumentoCliente int(20) DEFAULT NULL,
  Precio int(11) DEFAULT NULL,
  ServicioCodigo int(11) DEFAULT NULL,
  IdEmpleado int(11) DEFAULT NULL,
  PRIMARY KEY
);

CREATE TABLE apartarproducto (
  DocumentoCliente int(11) DEFAULT NULL,
  NombreCliente varchar(50) DEFAULT NULL,
  NombreProducto varchar(50) DEFAULT NULL,
  IDProducto int(11) DEFAULT NULL,
  Codigo int(11) NOT NULL,
  PRIMARY KEY (Codigo)
);

CREATE TABLE catálogo (
  NombreProducto varchar(20) DEFAULT NULL,
  IDCatalogo int(11) NOT NULL,
  CodigoProducto int(11) DEFAULT NULL,
  DescripcionProductos varchar(100) DEFAULT NULL,
  CantidadDeProductos varchar(20) DEFAULT NULL,
  CodigoServicio int(11) DEFAULT NULL,
  Precio varchar(10) DEFAULT NULL,
  NombreServicio varchar(50) DEFAULT NULL,
  DescripcionDelServicio varchar(100) DEFAULT NULL,
  CatalogoCliente int(11) DEFAULT NULL,
  PRIMARY KEY (IDCatalogo)
);

CREATE TABLE novedades (
  CodigoNovedades int(11) DEFAULT NULL,
  Nombre varchar(50) NOT NULL,
  Cantidad int(11) NOT NULL,
  FechaEntrada date DEFAULT NULL,
  FechaSalida date DEFAULT NULL,
  FechaVencimiento date DEFAULT NULL,
  CodigoProducto int(11) NOT NULL,
  PRIMARY KEY (CodigoNovedades)
);

CREATE TABLE proveedores (
  IdProveedor int(11) NOT NULL,
  ProveedorNombre varchar(100) NOT NULL,
  ProveedorApellido varchar(100) NOT NULL,
  ProveedorDireccion varchar(100) NOT NULL,
  ProveedorTelefono varchar(100) NOT NULL,
  PRIMARY KEY (Idproveedor)
);

-- Evaluar tabla para ver si es valida dejarla o no
CREATE TABLE registros (
  Nombre varchar(50) DEFAULT NULL,
  Apellido varchar(50) DEFAULT NULL,
  TipoDeDocumento varchar(50) DEFAULT NULL,
  NumeroDeDocumento int(11) DEFAULT NULL,
  Correo varchar(100) DEFAULT NULL,
  EmpleadoCedula int(11) NOT NULL,
  ClienteCedula int(11) NOT NULL
);

CREATE TABLE tblalmacen (
  AlmacenCodigo int(11) NOT NULL,
  AlmacenNombre varchar(20) NOT NULL,
  EntCodigoProducto int(11) NOT NULL,
  PRIMARY KEY (AlmacenCodigo)
);

CREATE TABLE tblentradaproductos (
  EntradaCodigo int(11) NOT NULL,
  EntradaNombreProducto char(15) NOT NULL,
  EntradaCantidad int(11) NOT NULL,
  EntradaMarca char(15) NOT NULL,
  EntradaFechaHora datetime NOT NULL,
  EntradaFechaVencimiento date NOT NULL,
  EntradaCodigoProducto int(11) NOT NULL,
  EntradaDescripcion varchar(230) NOT NULL,
  IdProveedor int(11) DEFAULT NULL,
  PRIMARY KEY (EntradaCodigo)
);

CREATE TABLE tblproductos (
  ProductoCodigo int(11) NOT NULL,
  ProductoNombre char(15) NOT NULL,
  ProductoCantidad int(11) NOT NULL,
  ProductoMarca char(15) NOT NULL,
  ProductoDescripcion varchar(230) DEFAULT NULL,
  ProductoCategoria varchar(100) DEFAULT NULL,
  ProductoFechaVencimiento date NOT NULL,
  PRIMARY KEY (ProductoCodigo)
);

CREATE TABLE tblsalidaproductos (
  SalidaCodigo int(11) NOT NULL,
  SalidaNombreProducto char(15) NOT NULL,
  SalidaCantidad int(11) NOT NULL,
  SalidaMarca char(15) NOT NULL,
  SalidaFechaHora datetime NOT NULL,
  SalidaCodigoProducto int(11) NOT NULL,
  SalidaDescripcion varchar(230) NOT NULL,
  Idproveedor int(11) NOT NULL,
  PRIMARY KEY (SalidaCodigo)
);

CREATE TABLE tblservicios (
  ServicioCodigo int(11) NOT NULL,
  ServicioNombre char(50) NOT NULL,
  ServicioPrecios varchar(100) DEFAULT NULL,
  PRIMARY KEY (ServicioCodigo)
);
