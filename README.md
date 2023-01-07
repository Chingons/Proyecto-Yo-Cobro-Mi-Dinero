
# Proyecto Yo Cobro Mi Dinero

El Proyecto Yo Cobro Mi Dinero es es una app web, realizada con: 
HTML, Css, Python utilizando framework Flask y Javascript, diseñada para la gestión y deuda de 
nuestros clientes (pensada para comerciantes), en donde elegí 
crearla en la web ya que el motivo de esta es que sea compatible 
con tablets, teléfonos y computadoras, primero esta app web la 
nombre “Yo Cobro Mi Dinero”, la cual esta pensada con las siguientes 
funciones: 


-Registro de Usuario (El cual solo permite registrarte con un solo email – envía código de activación al correo electrónico). 

-Recuperación de Contraseña (Recuperada con un Código). 

-Registro de Clientes. 

-Editar y Eliminar datos de los Clientes. 

-Registro de Factura o Deuda. 

-Recibo de Ingreso. 


Pero solo están creadas las siguientes funciones: 

-Registro de Usuario. 

-Recuperación de Contraseña.

-Registro de Clientes


En el inicio he estado trabajando en el apartado de la Factura
tengo listo un buscador en donde cuando le das click al input
de buscar ingresar nombre de cliente, te aparece una tabla en donde 
estan los clientes
que hemos registrado, en donde seleccionaremos a cual cliente
deseamos facturarle.

CONFIGURAR EL PROYECTO

PRIMERO
Nos iremos al archivo comandos.sql en donde copiaremos los comandos sql para la creacion de las bases de datos que se encuentran en ese proyecto.


SEGUNDO
Crearemos un archivo de configuracion ".env" en esta misma ubicacion en donde crearemos las siguientes variables:

DATABASE_PORT = 5432
DATABASE_HOST ='localhost'
DATABASE_USER = 'postgres'
DATABASE_PASSWORD = '0000'
DATABASE = 'postgres'

puede utilizar las credenciales de su gusto


COMO EJECUTAR EL Proyecto

Ejecutamos el archivo llamado Run.py, el cual tengo como archivo
ejecutador del codigo.

Tengo configurado el puerto en donde podemos visualizar nuestro Proyecto
el puerto que he puesto manualmente es el puerto 5000.

Luego de ejecutar el proyecto con el archivo Run.py, entraremos
a nuestro navegador favorito y entramos con la direccion
localhost:5000.

Lo primero que va a aparecer es la pagina de login, en donde
si no tenemos una cuenta nos podemos registrar (Si nos vamos a 
registrar, necesitamos un correo electronico que exista y al cual
podemos acceder ya que cuando registramos nuestra cuenta 
necesitaremos un codigo para activarla, el cual nos llegara en un 
mensaje  a nuestro correo, por eso necesitamos un correo real al cual
podamos acceder al mensaje para escribir el codigo).


También si hemos creado una cuenta y se nos olvida la Contraseña
podemos dar click en "Olvidaste tu contraseña", en donde 
cuando ingresamos nuestro correo, si no existe una cuenta 
registrada con ese correo electronico, mostrara un error, Pero
si existe una cuenta, nos enviara un codigo en un mensaje a nuestro
correo electronico, para verificar que es el titular de la cuenta
quien quiere recuperar la contraseña. Luego ingresamos el codigo
y escribimos la nueva contraseña que nos se nos olvidara.

Despues de registrarnos o recuperado la cuenta, al ingresar nuestros datos,
luego al entrar con una cuenta ya activada, lo primero que nos aparecera
es la pagina home o pagina de inicio el cual esta pensada 
para crear la facturacion.

Tengo tambien en funcionamiento el apartado de nuevo cliente, el cual
utilizaremos para agregar un cliente nuevo, cada cliente se 
diferencia por el numero de identificacion (ya que en cada persona
es un numero unico), si ya hemos registrado una persona e intentamos
agregarla como cliente nuevamente, si el no. de identificacion
o el documento de identificacion es el mismo que ya esta registrado,
entonces no se nos permitira registrar un cliente 2 veces.

Luego para salir de nuestra cuenta, podemos dar click en cerrar sessión.

Todo, menos el menu de inicio, es responsive, es adaptativa para 
dispositivos moviles.

Muchas Gracias.

Se despide, Edwin Magarin.