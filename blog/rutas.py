from http import client
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

mysql_port = 5432
mysql_host='ec2-52-73-155-171.compute-1.amazonaws.com'
mysql_user='blzjwmyrgcmrwg'
mysql_password='4b5834567c7d373ce638d622d2f01b1272101596a8b4f72def193084f092c77d'
mysql_db='dbqh2islt96mva'

conn = psycopg2.connect(dbname=mysql_db, user=mysql_user, password=mysql_password, host=mysql_host, port = mysql_port)

session




@app.route("/login", methods=['GET','POST'])
def login():
    if 'loggedin' in session:
        return redirect(url_for('inicio', id=0, facturarclientes = {"id":0, "nombrecompleto": 'nombrecliente', "telefono":"000-000-0000", "identificacion":"000-0000000-0", "ubicacion":"Ciudad" }))
    
    else:
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        if request.method == 'POST' and 'user_email' in request.form and 'user_password' in request.form:
            email_login = request.form['user_email']
            password_login = request.form['user_password']

            cursor.execute('SELECT * FROM usuarios WHERE email = %s', (email_login,))
            cuenta = cursor.fetchone()

          
            
            if not email_login or not password_login:
                flash('FAVOR RELLENAR TODOS LOS CAMPOS','rellenar')


            elif cuenta:
                log_id = cuenta[0]
                log_email = cuenta[1]
                log_nombres = cuenta[2]
                log_apellidos = cuenta[3]
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
        #return redirect(url_for('inicio',id))
        return render_template('inicio.html',id=0, nombre=session['nombres'], apellido=session['apellidos'], facturarclientes = {"id":0, "nombrecompleto": 'nombrecliente', "telefono":"000-000-0000", "identificacion":"000-0000000-0", "ubicacion":"Ciudad" })
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
        

        cursor.execute('SELECT * FROM usuarios WHERE email =%s', (datos_registro['email'],))
        account = cursor.fetchone()
        print(account)

        
        if not datos_registro['nombres'] or not datos_registro['apellidos'] or not datos_registro['email'] or not datos_registro['contraseña_registro'] or not datos_registro['confirmar_contraseña_registro']:
            flash ('FAVOR RELLENAR TODOS LOS CAMPOS', 'rellenar')
        
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
            email_password = 'qilppvviqicvxmhk'
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
                    
                    cursor.execute("INSERT INTO usuarios (nombres, apellidos,email, contraseña, fecha) VALUES (%s,%s,%s,%s,%s)",(enviar_datos[codigo_final[codigo]]['nombres'], enviar_datos[codigo_final[codigo]]['apellidos'], enviar_datos[codigo_final[codigo]]['email'], enviar_datos[codigo_final[codigo]]['contraseña'], hora_fecha))
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
      cursor.execute('SELECT * FROM usuarios WHERE email =%s', (formularios_recuperar['email'],))
      account = cursor.fetchone()
      if account:
         codigo_otp = random.randint(0000000, 9999999)
         datos_recuperar[formularios_recuperar['email']] = codigo_otp
         datos_recuperar['nombres'] = account[2]
         datos_recuperar['apellidos'] = account[3]
         email_recuperar[codigo_otp] = formularios_recuperar['email']
         email_emisor = 'noresponderyocobrotudinero@gmail.com'
         email_password = 'qilppvviqicvxmhk'
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
                cursor.execute("UPDATE usuarios set contraseña =%s where email = %s",(hashed, email_recuperar[codigo_actualizar]))
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
            cursor.execute('SELECT * FROM clientes WHERE identificacion =%s and idcreador=%s', (nuevo_cliente['identificacion'], nuevo_cliente['idcreador']))
            account = cursor.fetchone()

            if account:
                print (account)
                flash('Cliente ya Registrado','error')

            else:
                cursor.execute("INSERT INTO clientes (idcreador, nombres, apellidos, telefono, identificacion, direccion, fecha_creacion) VALUES (%s,%s,%s,%s,%s,%s,%s)",(nuevo_cliente['idcreador'], nuevo_cliente['nombres'], nuevo_cliente['apellidos'], nuevo_cliente['telefono'],nuevo_cliente['identificacion'],nuevo_cliente['direccion'], hora_fecha))
                conn.commit()
                flash('Cliente registrado con Exito', 'aprobado')
            
            

        
        return render_template('addcliente.html', title="Nuevo Cliente", nombre=session['nombres'], apellido=session['apellidos'])
    else:
            return redirect(url_for('login'))
    

@app.route('/inicio/<int:id>', methods=['GET','POST'])
def inicio(id):
    if 'loggedin' in session:
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute('SELECT * FROM clientes WHERE idcreador = %s', (session['id'],))
        clientes = cursor.fetchall()
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
            campos_cliente = {"id":0, "nombrecompleto": 'nombrecliente', "telefono":"000-000-0000", "identificacion":"000-0000000-0", "ubicacion":"Ciudad" }    
            
        

        return render_template('inicio.html',nombre=session['nombres'], apellido=session['apellidos'], cliente = clientes, facturarclientes = campos_cliente)

    else:
        return render_template('login.html')


