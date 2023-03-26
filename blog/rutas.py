from flask import Flask, render_template, request, flash, redirect, url_for, session
from blog import app
import psycopg2
import psycopg2.extras
import re
import time
from werkzeug.security import generate_password_hash, check_password_hash
import random
from email.message import EmailMessage
import ssl
import smtplib
from decouple import config
import json


verificar_cuenta = []
ya_verificado =[]
hora_fecha = time.strftime("%c")
datos_registro ={}
codigo_final = {}
actualizar_ps = []
nuevo_cliente = {}
email_verificar = {}
enviar_datos = {}
datos_recuperar = {}
email_recuperar = {}
formularios_recuperar = {}
imprimir_clientes = {}


mysql_port = config("DATABASE_PORT")
mysql_host = config("DATABASE_HOST")
mysql_user = config("DATABASE_USER")
mysql_password = config("DATABASE_PASSWORD")
mysql_db = config("DATABASE")


conn = psycopg2.connect(dbname=mysql_db, user=mysql_user, password=mysql_password, host=mysql_host, port = mysql_port)

session




@app.route("/login", methods=['GET','POST'])
def login():
    if 'loggedin' in session:
        return redirect(url_for('inicio', id=0, facturarclientes = {"id":0, "nombrecompleto": 'None', "telefono":"0", "identificacion":"0", "ubicacion":"None" }))
    
    else:
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        if request.method == 'POST' and 'user_email' in request.form and 'user_password' in request.form:
            email_login = request.form['user_email']
            password_login = request.form['user_password']

            cursor.execute('SELECT * FROM usuario WHERE email = %s', (email_login,))
            cuenta = cursor.fetchone()

          
            
            if not email_login or not password_login:
                flash('FAVOR RELLENAR TODOS LOS CAMPOS','rellenar')


            elif cuenta:
                log_id = cuenta[0]
                log_nombres = cuenta[1]
                log_apellidos = cuenta[2]
                log_email = cuenta[3]
                log_contraseña = cuenta[4]
                password_rs = log_contraseña
                
                
                if check_password_hash(password_rs, password_login):
                    session['loggedin'] = True
                    session['id'] = log_id
                    session['email'] = log_email
                    session['nombres'] = log_nombres
                    session['apellidos'] = log_apellidos
                    

                    return redirect(url_for('inicio', id=0))

                else:
                    flash('CORREO O CONTRASEÑA INCORRECTA','error')

            elif not cuenta:
                flash('CORREO NO REGISTRADO','error')
        
        elif request.method == 'POST':
            flash ('FAVOR RELLENAR TODOS LOS CAMPOS','rellenar')
    
    return render_template("login.html")


@app.route("/home", methods=['GET','POST'])
def home():
    if 'loggedin' in session:
        
        return render_template('inicio.html',id=0, facturarclientes = {"id":0, "nombrecompleto": 'nombrecliente', "telefono":"000-000-0000", "identificacion":"000-0000000-0", "ubicacion":"Ciudad" })
    else:
        return redirect(url_for('login'))




@app.route("/registro", methods=['GET','POST'])
def registro():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if 'loggedin' in session:
        return redirect(url_for('inicio'))
    elif request.method== 'POST' and 'nombres' in request.form and 'apellidos' in request.form and 'email-registro'in request.form and 'contraseña-registro' in request.form and 'confirmar-contraseña' in request.form:
        datos_registro['nombres']=request.form['nombres']
        datos_registro['apellidos']=request.form['apellidos']
        datos_registro['email']= request.form['email-registro']
        datos_registro['contraseña_registro']=request.form['contraseña-registro']
        datos_registro ['confirmar_contraseña_registro']= request.form['confirmar-contraseña']
        

        cursor.execute('SELECT * FROM usuario WHERE email =%s', (datos_registro['email'],))
        account = cursor.fetchone()
        

        
        if not datos_registro['nombres'] or not datos_registro['apellidos'] or not datos_registro['email'] or not datos_registro['contraseña_registro'] or not datos_registro['confirmar_contraseña_registro']:
            flash ('FAVOR RELLENAR TODOS LOS CAMPOS', 'rellenar')
        elif account =="":
            pass

        elif account:
            flash('CORREO ELECTRONICO REGISTRADO, FAVOR INGRESAR UN CORREO DIFERENTE', 'aprobado')
    
        elif datos_registro['contraseña_registro'] != datos_registro['confirmar_contraseña_registro']:
            flash ('FAVOR INGRESAR CORRECTAMENTE LAS CONTRASEÑAS','error')
        
        
        elif not re.match(r'[^@]+@[^@]+\.[^@]+',datos_registro['email']):
            flash ('CORREO ELECTRONICO INVALIDO', 'error')
        
        
        else:
            
            codigo_otp = random.randint(0000000, 9999999)
            codigo_final[codigo_otp] = datos_registro['email']
            verificar_cuenta.append('verificar')
            email_verificar[datos_registro['email']] = codigo_otp
            hashed_password = generate_password_hash(datos_registro['confirmar_contraseña_registro'])
            enviar_datos[datos_registro['email']] = {'nombres':datos_registro['nombres'], 'apellidos':datos_registro['apellidos'], 'email':datos_registro['email'], 'contraseña':hashed_password}
            
            email_emisor = 'noresponderyocobrotudinero@gmail.com'
            email_password = 'kqwftczwtmxjwoez'
            email_receptor = datos_registro['email']
            
            asunto= 'ACTIVACION DE CUENTA YO COBRO TU DINERO'
           
            cuerpo =  """ 
                <!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title></title>
</head>
<body style="width:100%;">
    <section style="display:flex; justify-content:center; align-items:center;">
        <div>
            <img src="https://drive.google.com/uc?export=download&id=1Pg9dWp_bO4vlVm55cCaHbtoRZwdmWD46" alt="yocobo" width="300px">
            <h2>HOLA! {} {}, GRACIAS POR UTILIZAR NUESTROS SERVICIOS.</h2>
            <h3>EL CODIGO PARA ACTIVAR TU CUENTA <span style="color:#2EC640 ;"> YO COBRO </span> <span style="color: #F3C538;">MI DINERO </span> ES:</h3>
            <h1> {} </h1>

            <h4>MUCHAS GRACIAS, ATENTAMENTE: EL EQUIPO YO COBRO MI DINERO</h4>

        </div>

    </section>
    
    
</body>
</html> """.format(datos_registro['nombres'], datos_registro['apellidos'],(email_verificar[datos_registro['email']]) ) 
                
        
            em = EmailMessage()
            em ['From'] = email_emisor
            em ['To'] = email_receptor
            em['Subject'] = asunto
            em.add_alternative(cuerpo, subtype = "html")
            
            context = ssl.create_default_context()
            
            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                smtp.login(email_emisor,email_password)
                smtp.sendmail(email_emisor,email_receptor, em.as_string())
            
            if 'verificar' in verificar_cuenta:
                flash('HEMOS ENVIADO UN CODIGO DE ACTIVACION A TU EMAIL','aprobado')
                return redirect(url_for('verificar'))
    
    elif request.method == 'POST':
        flash ('FAVOR RELLENAR TODOS LOS CAMPOS', 'rellenar')

    return render_template("registro.html")

@app.route("/")
def inin():
    if 'loggedin' in session:
        return redirect(url_for('inicio',id=0))
    
    return redirect(url_for("login"))


@app.route('/verificar', methods=['GET','POST'])
def verificar():
    if 'loggedin' in session:
        return redirect(url_for('inicio'))
    elif 'verificar' in verificar_cuenta:
        
        if request.method == 'POST' and 'ing-codigo' in request.form:
                codigo = int(request.form['ing-codigo']) 

                if codigo in codigo_final and codigo_final[codigo] in email_verificar:
                    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
                    ya_verificado.append('esta-verificado')
                    
                    cursor.execute("INSERT INTO usuario (nombres, apellidos,email, contraseña, fecha) VALUES (%s,%s,%s,%s,%s)",(enviar_datos[codigo_final[codigo]]['nombres'], enviar_datos[codigo_final[codigo]]['apellidos'], enviar_datos[codigo_final[codigo]]['email'], enviar_datos[codigo_final[codigo]]['contraseña'], hora_fecha))
                    conn.commit()
                    datos_registro.clear()
                    email_verificar.pop(codigo_final[codigo])
                    codigo_final.pop(codigo)
                    flash('TE HAS REGISTRADO CON EXITO, YA PUEDES INGRESAR', 'aprobado')
                    return redirect(url_for('login'))

                elif not codigo:
                    flash('FAVOR INGRESAR UN CODIGO', 'rellenar')
                
                else:
                    flash ('CODIGO INCORRECTO', 'error')
    
    else:
        return redirect(url_for('login')) 
    return render_template("verificar.html")
   
    
    

@app.route('/logout')
def logout():
    session.clear()

    return redirect(url_for('login'))


@app.route('/recuperar', methods=['GET','POST'])
def recuperar():
    if 'loggedin' in session:
        return redirect(url_for('inicio'))
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method== 'POST' and 'recuperacion' in request.form:
      formularios_recuperar['email']=request.form['recuperacion']
      cursor.execute('SELECT * FROM usuario WHERE email =%s', (formularios_recuperar['email'],))
      account = cursor.fetchone()
      if account:
         codigo_otp = random.randint(0000000, 9999999)
         datos_recuperar[formularios_recuperar['email']] = codigo_otp
         datos_recuperar['nombres'] = account[2]
         datos_recuperar['apellidos'] = account[3]
         email_recuperar[codigo_otp] = formularios_recuperar['email']
         email_emisor = 'noresponderyocobrotudinero@gmail.com'
         email_password = 'kqwftczwtmxjwoez'
         email_receptor = formularios_recuperar['email'] 
         asunto= 'CAMBIAR CONTRASEÑA CUENTA YO COBRO TU DINERO'
         cuerpo =  """
                                    <!DOCTYPE html>
                    <html lang="es">
                    <head>
                        <meta charset="UTF-8">
                        <meta http-equiv="X-UA-Compatible" content="IE=edge">
                        <meta name="viewport" content="width=device-width, initial-scale=1.0">
                        <title></title>
                    </head>
                    <body style="margin:0; padding:0;">
                        <section style="display:flex; justify-content:center; align-items:center;">
                            <div>
                                <img src="https://drive.google.com/uc?export=download&id=1Pg9dWp_bO4vlVm55cCaHbtoRZwdmWD46" alt="yocobo" width="300px">
                                <h2>HOLA! {} {}, GRACIAS POR UTILIZAR NUESTROS SERVICIOS.</h2>
                                <h3>EL CODIGO PARA RESTABLECER LA CONTRASEÑA DE TU CUENTA <span style="color:#2EC640 ;"> YO COBRO </span> <span style="color: #F3C538;">MI DINERO </span> ES:</h3>
                                <h1> {} </h1>
                                <h4>MUCHAS GRACIAS, ATENTAMENTE: EL EQUIPO YO COBRO MI DINERO</h4>
                            </div>
                        </section>
                    </body>
                    </html> """.format(datos_recuperar['nombres'], datos_recuperar['apellidos'],datos_recuperar[formularios_recuperar['email']]) 
         em = EmailMessage()
         em ['From'] = email_emisor
         em ['To'] = email_receptor
         em['Subject'] = asunto
         em.add_alternative(cuerpo, subtype = "html")
         context = ssl.create_default_context()
         with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
              smtp.login(email_emisor,email_password)
              smtp.sendmail(email_emisor,email_receptor, em.as_string())
         flash ('HEMOS ENVIADO UN CODIGO A TU CORREO', 'aprobado')
         actualizar_ps.append('confirmado')
         return redirect(url_for('actualizar'))
        
      else:
            flash('CORREO NO REGISTRADO', 'error')
    
    return render_template("recuperar.html")
        
            
@app.route('/actualizar', methods=['GET','POST'])
def actualizar():
    if 'loggedin' in session:
        return redirect(url_for('inicio'))
    
    elif 'confirmado' in actualizar_ps:
         if request.method== 'POST' and 'codigo' in request.form and 'contraseña-actualizar' in request.form and 'confirmar-contraseña' in request.form:
            codigo_actualizar = int(request.form['codigo']) 
            if codigo_actualizar in email_recuperar and email_recuperar[codigo_actualizar] in datos_recuperar and request.form['confirmar-contraseña'] == request.form['contraseña-actualizar']:
                cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
                datos_recuperar['confirmar_contraseña_registro'] = request.form['confirmar-contraseña']
                hashed = generate_password_hash(datos_recuperar['confirmar_contraseña_registro'])
                cursor.execute("UPDATE usuario set contraseña =%s where email = %s",(hashed, email_recuperar[codigo_actualizar]))
                conn.commit()
                datos_recuperar.pop(email_recuperar[codigo_actualizar])
                email_recuperar.pop(codigo_actualizar)
                
                flash('Has cambiado tu contraseña con Exito','aprobado')
                return redirect(url_for('login'))
            
            
            elif request.form['confirmar-contraseña'] != request.form['contraseña-actualizar']:
                flash('Favor Ingresar las mismas contraseñas','error')

            else:
                flash('Codigo Incorrecto','error')
             
    else:
        return redirect(url_for('recuperar'))
    
    return render_template("actualizar.html") 

@app.route('/nuevocliente', methods=['GET', 'POST'])
def nuevocliente():

    if 'loggedin' in session:
        if request.method == 'POST' and 'nombres' in request.form and 'apellidos' in request.form and 'telefono' in request.form and 'identificacion' in request.form and 'direccion' in request.form:
            nuevo_cliente['idcreador'] = session['id']
            nuevo_cliente['nombres'] = request.form['nombres']
            nuevo_cliente['apellidos'] = request.form['apellidos']
            nuevo_cliente['telefono'] = request.form['telefono']
            nuevo_cliente['identificacion'] = request.form['identificacion']
            nuevo_cliente['direccion'] = request.form['direccion']

            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            
            cursor.execute('SELECT * FROM clientes WHERE identificacion =%s and idcreador=%s', (nuevo_cliente['identificacion'], nuevo_cliente['idcreador'],))
            account = cursor.fetchone()

            
            if account:
                flash('Cliente ya Registrado','error')
        

            else:
                cursor.execute("INSERT INTO clientes (idcreador, nombres, apellidos, telefono, identificacion, direccion, fecha_creacion) VALUES (%s,%s,%s,%s,%s,%s,%s)",(nuevo_cliente['idcreador'], nuevo_cliente['nombres'], nuevo_cliente['apellidos'], nuevo_cliente['telefono'],nuevo_cliente['identificacion'],nuevo_cliente['direccion'], hora_fecha))
                conn.commit()
                flash('Cliente registrado con Exito', 'aprobado')
            
            

        
        return render_template('addcliente.html', title="NUEVO CLIENTE")
    else:
            return redirect(url_for('login'))
    

@app.route('/inicio/<int:id>', methods=['GET','POST'])
def inicio(id):
    if 'loggedin' in session:
        conn = psycopg2.connect(dbname=mysql_db, user=mysql_user, password=mysql_password, host=mysql_host, port = mysql_port)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute('SELECT * FROM clientes WHERE idcreador = %s order by id asc', (session['id'],))
        clientes = cursor.fetchall()
        cursor.execute('SELECT idfactura FROM FACTURAS order by idfactura desc')
        
        factura = cursor.fetchall()
        comparacion = len(factura)
        

        if comparacion == 0:
             no_factura = 1
            
           
        
        else:
             no_factura =  factura[0][0] + 1
           
            
        cantidadclientes = len(clientes)
        contador = 0
        facturar_clientes = {}
        
        while cantidadclientes>0:
            facturar_clientes[clientes[contador][0]] = {"id":clientes[contador][0],"nombrecompleto": clientes[contador][2] + " " +clientes[contador][3], "telefono":clientes[contador][4], "identificacion":clientes[contador][5], "ubicacion":clientes[contador][6]}
            contador +=1
            cantidadclientes-=1
            
        
        
        if id>0:
            convertidor = id
            campos_cliente =  facturar_clientes[convertidor]
            
        
        
        else:
            campos_cliente = {"id":0, "nombrecompleto": 'None', "telefono":"0", "identificacion":"0", "ubicacion":"None" }    
            
        
        if request.method == "POST":
            jsonData = request.get_json()
            cursor.execute('INSERT INTO facturas (idfacturador, idcliente, fecha, monto_original, monto_actual, estado, pagada) values (%s, %s, %s, %s,%s,%s,%s)', (session['id'], int(jsonData['factura']['id_cliente']) ,jsonData['factura']['fecha_factura'],jsonData['total_final'],jsonData['total_final'],"ACTIVO", "NO"))
            conn.commit()
           
            for p in jsonData['articulos']:
                if p==None:
                    pass
                else:
                    cursor.execute('INSERT INTO articulos (idfactura,cantidad,descripcion,precio,subtotal, estado) values (%s, %s, %s, %s,%s,%s)', (jsonData['factura']['no_factura'] ,p['cantidad'], p['descripcion'], p['precio_unitario'], p['total'], "ACTIVO"))
                    conn.commit()
            
            return login()
            
            
            
           

        return render_template('inicio.html',nombre=session['nombres'], apellido=session['apellidos'], cliente = clientes, facturarclientes = campos_cliente, factura = no_factura, title="NUEVA FACTURA")

    else:
        return render_template('login.html')



@app.route('/clientes',methods=['GET','POST'])
def clientes():
    if 'loggedin' in session:
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute('SELECT * FROM clientes WHERE idcreador = %s order by id asc', (session['id'],))
        nuestros_clientes = cursor.fetchall()
        return render_template('clientes.html', clientes_usuario=nuestros_clientes, title="EDITAR O ELIMINAR CLIENTES")
    
    else:
        return render_template('login.html')

@app.route('/editar_clientes/<int:idcliente>',methods=['GET','POST'])
def editar_clientes(idcliente):
    if 'loggedin' in session:
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute('SELECT * FROM clientes WHERE idcreador = %s and id=%s', (session['id'],idcliente,))
        cliente_editar = cursor.fetchall()
        if request.method=='POST':
            nombre_edit = request.form['nombre-editado']
            apellido_edit = request.form['apellido-editado']
            telefono_edit = request.form['telefono-editado']
            direccion_edit = request.form['direccion-editado']
            
            return redirect(url_for('clientes'))

        return render_template('editarcliente.html', datos_clientes=cliente_editar, title="EDITAR CLIENTE")
    
    else:
        return render_template('login.html')

@app.route('/guardarcliente',methods=['GET','POST'])
def guardarcliente():
    if 'loggedin' in session:
        if request.method=='POST':
            id_edit = request.form['id-editado']
            nombre_edit = request.form['nombre-editado']
            apellido_edit = request.form['apellido-editado']
            telefono_edit = request.form['telefono-editado']
            direccion_edit = request.form['direccion-editado']
            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cursor.execute('update clientes set nombres = %s where id=%s and idcreador=%s', (nombre_edit, id_edit,session['id'],))
            cursor.execute('update clientes set apellidos = %s where id=%s and idcreador=%s', (apellido_edit, id_edit,session['id'],))
            cursor.execute('update clientes set telefono = %s where id=%s and idcreador=%s', (telefono_edit, id_edit,session['id'],))
            cursor.execute('update clientes set direccion = %s where id=%s and idcreador=%s', (direccion_edit, id_edit,session['id'],))
            conn.commit()
            

        return redirect(url_for('clientes'))
    
    else:
        return render_template('login.html')


@app.route('/eliminar_cliente/<int:ideliminar>',methods=['GET','POST'])
def eliminar_cliente(ideliminar):
     if 'loggedin' in session:
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute('SELECT idfactura FROM facturas WHERE idfacturador = %s and idcliente=%s and estado=%s', (session['id'],ideliminar,"ACTIVO"))
        id_factura = cursor.fetchall()
        if len(id_factura) >0:
            for id in id_factura:
                cursor.execute('update articulos set estado=%s WHERE idfactura = %s ', ("ELIMINADO",id[0],))
                conn.commit()
            cursor.execute('update facturas set estado=%s WHERE idfacturador = %s and idcliente=%s', ("ELIMINADO",session['id'],ideliminar,))
            conn.commit()
        cursor.execute('delete from clientes WHERE idcreador = %s and id=%s', (session['id'],ideliminar,))
        conn.commit()
        return redirect(url_for('clientes'))


@app.route('/estadoscuentas', methods=['GET', 'POST'])
def estadoscuentas():
    if 'loggedin' in session:
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute('SELECT * FROM clientes WHERE idcreador = %s order by id asc', (session['id'],))
        estado_clientes = cursor.fetchall()
        contador = 0
        
        for datos in estado_clientes:
            total_montos = 0
            cursor.execute('SELECT monto_actual from facturas where idcliente =%s and estado=%s and pagada=%s',( str(datos[0]),'ACTIVO','NO'))
            monto = cursor.fetchall()
            for total in monto:
                total_montos += total[0]
            
            insertar = format(total_montos, ',d')
            estado_clientes[contador].append(insertar)
            contador +=1
            
        return render_template('clientes_estados.html', clientes_estado=estado_clientes, title="ESTADOS DE CUENTAS")
    
    
    else:
        return render_template('login.html')
    

@app.route('/facturas/<int:clientedeuda>')
def facturas(clientedeuda):
    if 'loggedin' in session:
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute('SELECT * FROM facturas WHERE idcliente = %s and estado=%s and pagada=%s order by idfactura asc', (clientedeuda, 'ACTIVO', 'NO'))
        deudas= cursor.fetchall()
        facturas_deuda = []
        cambiar = 0
        for tomar in deudas:
            cambiar = format(tomar[4], ',d')
            tomar[4] = cambiar
            cambiar = format(tomar[5], ',d')
            tomar[5] = cambiar
            facturas_deuda.append(tomar)
        
        return render_template('facturas.html', facturas=facturas_deuda, title="FACTURAS")
    
    else:
        return render_template('login.html')



@app.route('/articulos/<int:articulos>')
def articulos(articulos):
    if 'loggedin' in session:
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute('SELECT * FROM articulos WHERE idfactura = %s and estado=%s order by idfactura asc', (articulos, 'ACTIVO'))
        datos_articulos = cursor.fetchall()
        cantidad = 0
        precio = 0
        subtotal = 0
        articulos_finales = []
        for articulo in datos_articulos:
            cantidad = format(articulo[1], ',d')
            articulo[1] = cantidad
            
            precio = format(articulo[3], ',d')
            articulo[3] = precio

            subtotal = format(articulo[4], ',d')
            articulo[4] = subtotal
            articulos_finales.append(articulo)
        
        return render_template('articulos.html', articulos=articulos_finales, title="ARTICULOS")
    
    else:
        return render_template('login.html')

@app.route('/recibo', methods=['GET', 'POST'])
def recibo():
    
    if 'loggedin' in session:
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute('SELECT * FROM clientes WHERE idcreador = %s order by id asc', (session['id'], ))
        clientes_recibo = cursor.fetchall()
        cursor.execute('SELECT idrecibo from recibos order by idrecibo desc')
        ultimo_recibo = cursor.fetchall()
        idrecibo = 0
        comparacion = len(ultimo_recibo)
        if comparacion==0:
            idrecibo = 1
        else:
            idrecibo = ultimo_recibo[0][0] +1
        
        enviar_factura = {}
        formato = 0
        archivo_json = 'recibo.json'
        for recoger in clientes_recibo:
            cursor.execute('SELECT * FROM facturas where idcliente =%s and estado =%s and pagada =%s order by idfactura asc',(recoger[0],'ACTIVO','NO'))
            enviar_factura[formato] = {'idcliente':recoger[0], 'nombre':recoger[2] + " " + recoger[3], 
                                       'telefono':recoger[4], 'identificacion':recoger[5], 'direccion':recoger[6],
                                       'facturas':cursor.fetchall()}
            formato += 1        
           
            
        
        datos = open('blog/static/recibo.json', "w")
        json.dump(enviar_factura, datos)
        datos.close()
        return render_template('recibo.html', id=idrecibo, title="RECIBOS")

   
    else:
        return render_template('login.html')

@app.route('/pagar', methods=['GET','POST'])
def pagar():
    if 'loggedin' in session:
        if request.method=='POST':
            idfacturas =[]
            fechafacturas=[]
            montos_originales=[]
            montos_actuales=[]
            
            pago = request.get_json()
            
            for fc in pago["facturas"]:
                idfacturas.append(pago["facturas"][fc]['idfactura']) 
                fechafacturas.append(pago["facturas"][fc]['fecha'])
                montos_originales.append(pago["facturas"][fc]['monto_original'])
                montos_actuales.append(pago["facturas"][fc]['monto_actual'])
            
            parar = len(idfacturas)
            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            for num in range(0, parar):
                cursor.execute("update facturas set monto_actual=%s, pagada=%s where idfactura=%s",(0,"SI", idfacturas[num]))
            conn.commit()
            cursor.execute("insert into recibos (idcreador_recibo, idcliente_recibo, facturas, fecha_facturas, montos_originales_facturas, monto_pago_facturas, monto_total_recibo, fecha_recibo) values (%s, %s, %s, %s, %s, %s, %s, %s)",(session['id'], int(pago['idcliente']), idfacturas, fechafacturas,montos_originales, montos_actuales, pago['monto_recibo'], pago['fecha_recibo']))
            conn.commit()
        
        time.sleep(3)
        return redirect(url_for('recibo'))
    
    else:
        return render_template('login.html')

@app.route('/abonar', methods=['GET','POST'])
def abonar():
    if 'loggedin' in session:
        if request.method=='POST':
            abonar = request.get_json()
            for id in abonar['factura']:
                idfactura = abonar['factura'][id]['idfactura']
                montoactual = abonar['factura'][id]['monto_actual']
                monto_original = abonar['factura'][id]['monto_original']
                fecha_factura = abonar['factura'][id]['fecha']
            
            abono_final = int(montoactual) - int(abonar['monto_abono'])
            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cursor.execute("update facturas set monto_actual=%s where idfactura =%s",(abono_final, idfactura))
            conn.commit()
            cursor.execute("insert into recibos (idcreador_recibo, idcliente_recibo, facturas, fecha_facturas, montos_originales_facturas, monto_pago_facturas, monto_total_recibo, fecha_recibo) values (%s, %s, %s, %s, %s, %s, %s, %s)",(session['id'], int(abonar['idcliente']), idfactura, fecha_factura,monto_original, abonar['monto_abono'], abonar['monto_abono'], abonar['fecha_abono']))
            conn.commit()
        
        time.sleep(3)
        return redirect(url_for('recibo'))
    
    else:
        return render_template('login.html')