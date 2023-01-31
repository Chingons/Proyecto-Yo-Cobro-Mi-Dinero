
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
    fecha_creacion date not null
)


create table facturas(
    idfactura serial primary key,
    idfacturador int not null,
    idcliente int not null,
    fecha date not null,
    monto bigint not null,
    estado VARCHAR(50) not null /*el estado es para saber si la factura esta "PAGADA" o "NOPAGADA" */
)

