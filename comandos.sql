

create table usuario (
    id serial primary key,
    nombres VARCHAR(100) not null,
    apellidos VARCHAR(100) not null,
    email varchar (500) not null,
    contraseña varchar not null,
    fecha date not null
)


create table clientes (
    id serial primary key,
    idcreador int not null,
    nombres VARCHAR(100) not null,
    apellidos varchar (100) not NULL,
    telefono VARCHAR(50) not null,
    identificacion VARCHAR(50) not null,
    direccion varchar not null,
    fecha_creacion date not null,
)


create table facturas(
    idfactura serial primary key,
    idfacturador int not null,
    idcliente int not null,
    fecha varchar not null,
    monto_original bigint not null,
    monto_actual bigint not null,
    estado VARCHAR not null,
    pagada VARCHAR not null
)


create table articulos(
idfactura int not null,
	cantidad bigint not null,
	descripcion varchar(150) not null,
	precio bigint not null,
	subtotal bigint not null,
    estado varchar not null
)


create table usuario (
    id serial primary key,
    nombres VARCHAR(100) not null,
    apellidos VARCHAR(100) not null,
    email varchar (500) not null,
    contraseña varchar not null,
    fecha date not null
)


create table clientes (
    id serial primary key,
    idcreador int not null,
    nombres VARCHAR(100) not null,
    apellidos varchar (100) not NULL,
    telefono VARCHAR(50) not null,
    identificacion VARCHAR(50) not null,
    direccion varchar not null,
    fecha_creacion date not null,
)


create table facturas(
    idfactura serial primary key,
    idfacturador int not null,
    idcliente int not null,
    fecha varchar not null,
    monto bigint not null,
    estado VARCHAR not null,
    pagada VARCHAR not null
)


create table articulos(
idfactura int not null,
	cantidad bigint not null,
	descripcion varchar(150) not null,
	precio bigint not null,
	subtotal bigint not null,
    estado varchar not null
)
