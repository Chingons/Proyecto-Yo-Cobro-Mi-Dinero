
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
para crear la facturacion. En esta parte a la derecha de nuestra pantalla aparecera
un cuadro en el cual cuando damos click se nos desplegaran nuestros clientes
que tengamos registrado, en donde seleccionaremos al cliente 
que le deseamos adorsar la factura con un click, pero antes de 
que nos aparezcan los clientes en este apartado, tenemos que agregarlo.

Luego de que la factura este completa podemos dar clik en el boton guardar que estara debajo de la pagina de color azul.


El apartado de nuevo cliente lo
utilizaremos para agregar un cliente nuevo, cada cliente se 
diferencia por el numero de identificacion (ya que en cada persona
es un numero unico), si ya hemos registrado una persona e intentamos
agregarla como cliente nuevamente, si el no. de identificacion
o el documento de identificacion es el mismo que ya esta registrado,
entonces no se nos permitira registrar un cliente 2 veces.

En el apartado de clientes es el área donde nos apareceran
los clientes que ya tenemos registrados, en donde nos aparecera un
espacio en el inicio de la pantalla, en donde podemos ingresar
algun dato del cliente que deseemos editar o eliminar, 
esta funcion sirve para cuando tengamos muchos clientes
registrados, se nos sea mas facil hacer un filtro
del cliente en especifico.

Al final de los datos del cliente, aparecen 2 botones, editar y eliminar,
si queremos editar algun dato del cliente, presionamos editar,
nos dirigira a otra pagina en donde estan los datos del cliente
editables, menos el id, que es unico y el no. de identificacion
que es unico tambien.

De lo contrario si precionamos eliminar, primero tendremos
que asegurarnos de que este cliente no tenga ninguna deuda
ya que si tiene alguna deuda y eliminamos el cliente
ya no sera posible recuperar las facturas o las 
deudas que este cliente tenga o tenía.

En el apartado de Estado de cuentas, es otra área 
donde nos apareceran los clientes, de igual modo
tenemos un espacio arriba en donde podemos escribir
algun dato de nuestro cliente para crear un filtro y encontrar
el especifico, nos aparece el balance actual del cliente,
y atras un boton en donde podemos ver las facturas, 
si le damos click aqui nos enviara a otra pagina
en donde aparecen las facturas que este cliente debe,
aparecen datos como id factura, fecha factura,
monto original y el monto actual, también 
al final de cada factura, hay un boton que dice
mostrar en el cual si precionamos, podemos ver que articulos
son los que componen esta factura.

Por último pero no menos importante, el apartado de
recibos, en el cual cuando ingresamos, nos aparecera
un espacio arriba en donde dice click aqui para
mostrar clientes, en donde se nos desplegaran los clientes
de igual modo podemos filtrar clientes buscandolo por su 
nombre o algun dato de este cliente, cuando lo seleccionemos
dandole click, se nos desplegaran las facturas que este cliente deba,
al final de cada factura, se nos mostrara un boton que dice seleccionar
en donde cuando precionamos este boton, las facturas se procesaran, a
la tabla de facturas procesadas, las cuales estas son las facturas
que seran pagadas o la factura a abonar.

En caso de que el cliente pague la facturas, seleccionamos cuales son,
debajo nos aparecera un espacio que dice total y se nos mostrara
el total sumado de las facturas que hayamos seleccionado, luego
debajo de esto nos aparecera un boton azul el cual dice grabar pago,
cuando precionemos este boton, nos aparecera un mensaje verificando
que hayamos recibido la cantidad total de la suma de la factura antes
de grabar el recibo, nos apareceran 2 botones en este mensaje, en donde
uno se llama pagar, el cual si hemos recibido la cantidad correcta,
precionaremos este boton para saldar las facturas, de lo contrario
precionamos cancelar.

En esta misma pagina mas abajo a la derecha esta un boton llamado, 
activar abono, el cual funcionara para ingresar la cantidad
de dinero que vayamos a abonar a una factura, de hecho, solo 
podemos abonar dinero a 1 sola factura, asi que tenemos que 
tener en cuenta que si queremos abonar a varias facturas
tenemos que seleccionar 1 por una para especificar
a que factura abonar y cuanta cantidad le abonaremos.

Debajo de donde ingresemos la cantidad, nos aparecera un boton 
nombrado guardar abono, en el cual si precionamos, nos aparecera
un mensaje mencionando la cantidad que deseamos abonar, si
no deseamos abonar precionaremos el boton de cancelar, 
si la cantidad que muestra el mensaje es la misma cantidad
que el cliente nos entrego para abonar, le daremos click
al boton abonar, esta cantidad se nos restará al monto
original de la factura.

Luego para salir de nuestra cuenta, podemos dar click en cerrar sessión.


Muchas Gracias.

Se despide, Edwin Magarin.