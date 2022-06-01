from __future__ import print_function
from flask import Flask, render_template, request, redirect, url_for, session,flash
from smtplib import SMTP
from email.message import EmailMessage
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
import hashlib 
from models import cartaModels
from controllers import enviarCorreo
a=URLSafeTimedSerializer('Thisisasecret')
app = Flask(__name__)

@app.route('/')
def inicio():
    return render_template("index.html")

@app.route('/entrar',methods=["GET","POST"])
def entrar():
    if request.method == 'GET':
        return render_template("/homepage/login.html")

    email = request.form.get('email')
    password = request.form.get('password')
    password = hashlib.sha1(password.encode('utf8')).hexdigest()
    usuario = cartaModels.usuario(email, password)

    if usuario is None:
        flash("correo o contraseña incorrectos", 'error')
        return redirect(request.url)

    session['user'] = usuario
    
    return redirect(url_for('index_producto.html'))

   
@app.route('/nu_contra/<token>', methods=["GET", "POST"])
def nu_contra(token):
    email = a.loads(token, salt='recuperarp')
    return email
    return render_template("nu_contra.html")


@app.route('/recuperarp', methods=["GET", "POST"])
def rec_contra():
    if request.method =='GET':
        return render_template('rec_contra.html')

    email = request.form.get('email_form')
    usuario = cartaModels.consultarCorreo(email)
    if usuario is None:
            flash('correo invalido')
            print("no entro")
            return redirect(request.url)

    if email =='':
            flash('Ingrese el correo')

    token = a.dumps(email, salt='recuperarp')
    link = url_for('recuperarpLink', token=token, _external=True)
    enviarCorreo.recuperarContrasenia(email,link)
    flash("REVISA TU CORREO", 'success')   
    return render_template('/homepage/login.html')

@app.route('/recuperarpLink/<token>', methods=['GET', 'POST'])
def recuperarpLink(token):
    try:
        email = a.loads(token, salt='recuperarp')
    except SignatureExpired:
        flash("el token ya expiro")
    link = url_for('nu_contra', token=token, _external=True)
    return '<a href="{}">reestablece tu contraseña aqui</a>'.format(link)

@app.route('/volver', methods=["GET", "POST"])
def volver():
    return render_template("inicio.html")

@app.route('/cerrar', methods=["GET", "POST"])
def cerrar():
    session.clear()
    return render_template("inicio.html")
""" 
@app.route('/registrar', methods=["GET", "POST"])
def registrar():
    if request.method == 'GET':
        
        return render_template("registros.html")
    else:

        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        password_encri = hashlib.sha256(password.encode()).hexdigest()
        imagen = request.form['imagen']
        celular = request.form['celular']
        direccion = request.form['direccion']
        descripcion = request.form['descripcion']

        is_valid = True
    
        if name =="":
            flash("es requerido el nombre")
            is_valid= False
        
        if email =="":
            flash("es requerido el email")
            is_valid= False
        
        if password =="":
            flash("es requerido la contraseña")
            is_valid= False
    
        if imagen =="":
            is_valid= False

        if celular =="":
            flash("es requerido el telefono")
            is_valid= False 

        if direccion =="":
            flash("es requerido la direccion")
            is_valid= False  
        
        if descripcion =="":
            flash("es requerida la descripcion")
            is_valid= False

        if is_valid == False:
            print("los datos no son validos")
            return render_template("registros.html")

        
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (name, email, password, imagen, celular, direccion, descripcion) VALUES (%s,%s,%s,%s,%s,%s,%s)",(name,email,password_encri,imagen,celular,direccion,descripcion,))
        
        mysql.connection.commit()
        session['name'] = request.form['name']
        session['email'] = request.form['email']

        msg = EmailMessage()
        msg.set_content('Señor usuario bienvenido',)

        msg['Subject'] = 'confirmcion correo'
        msg['From'] = "yeinerangulo2020@itp.edu.co"
        msg['To'] = email

         # Reemplaza estos valores con tus credenciales de Google Mail
        username = 'yeinerangulo2020@itp.edu.co'
        password = '1193221281'

        server = SMTP('smtp.gmail.com:587')
        server.starttls()
        server.login(username, password)
        server.send_message(msg)

        server.quit()
        
    return render_template("index_producto.html")
     


@app.get('/mos_pro')
def mos_pro():
    cur=mysql.connection.cursor()
    cur.execute("select * from creacion_productos")
    productos = cur.fetchall()
    cur.close()
        
    return render_template('mos_prod.html',productos=productos)

@app.route('/e_prod', methods=['GET','POST'])
def editarprod():
    

    return render_template("editar_producto.html")

# @app.route('/actu_pro', methods=['GET','POST'])
# def actuprod():
#     cur=mysql.connection.cursor()
#     ute(cur.exec"SELECT * FROM creacion_productos WHERE id = {0}".format(id==1))
#     item=cur.fetchall()
#     cur.close()
#     return render_template('mos_prod.html')

@app.route('/eliminarpro/<int:id>')
def eliminarprod():
    cur=mysql.connection.cursor()
    cur.execute("DELETE from creacion_productos WHERE id={0}".format(id))
    cur.close()
    return render_template('mos_prod.html')

@app.route('/carrito', methods=['GET','POST'])
def carrito():
    return render_template('carrito.html')

@app.route('/actu_usu')
def actual_usua():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password'].encode('utf-8')
        password = hashlib.sha1(password.encode()).hexdigest()
        imagen = request.form['imagen']
        celular = request.form['celular']
        direccion = request.form['direccion']
        descripcion = request.form['descripcion']

        is_valid = True
    
        if name =="":
             flash("es requerido el nombre")
             is_valid= False
        
        if email =="":
             flash("es requerido el email")
             is_valid= False
        
        if password =="":
             flash("es requerido la contraseña")
             is_valid= False
    
        if imagen =="":
             is_valid= False

        if celular =="":
             flash("es requerido el telefono")
             is_valid= False 

        if direccion =="":
             flash("es requerido la direccion")
             is_valid= False  
        
        if descripcion =="":
             flash("es requerida la descripcion")
             is_valid= False

        if is_valid == False:
             print("los datos no son validos")
             return render_template("registros.html")

        
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (name, email, password, imagen, celular, direccion, descripcion) VALUES (%s,%s,%s,%s,%s,%s,%s)",(name,email,password_encri,imagen,celular,direccion,descripcion,))

        #token=s.dumps(correo, salt='email-confirm')
        #link= url_for('confirmarEmail', token=token, _external=True)
                
        mysql.connection.commit()
        session['name'] = request.form['name']
        session['email'] = request.form['email']

        msg = EmailMessage()
        msg.set_content('Señor usuario bienvenido',)

        msg['Subject'] = 'confirmcion correo'
        msg['From'] = "yeinerangulo2020@itp.edu.co"
        msg['To'] = email

         # Reemplaza estos valores con tus credenciales de Google Mail
        username = 'yeinerangulo2020@itp.edu.co'
        password = '1193221281'

        server = SMTP('smtp.gmail.com:587')
        server.starttls()
        server.login(username, password)
        server.send_message(msg)

        server.quit()
        
    return render_template('actua_infor.html')

@app.route('/crea_prod', methods=['GET','POST'])
def crea_prod():
    if request.method == 'GET':
        print("mostrando el formulario")
        return render_template("crea_prod.html")
    else:
        print("no pasa el producto")
        name = request.form.get('name_pro')
        descripcion = request.form.get('des_producto')
        precio = request.form.get('pre_productos')
        imagen = request.form.get('img_producto')

        is_valid = True
    
        if name =="":
            flash("es requerido el nombre para el registro del producto")
            is_valid= False
        
        if descripcion =="":
            flash("es requerido la descripcion para el registro del producto")
            is_valid= False
        
        if precio =="":
            flash("es requerido el precio para el registro del producto")
            is_valid= False
    
        if imagen =="":
            is_valid= False

        if is_valid == False:
            print("los datos no son validos")
            return render_template("crea_prod.html")

        
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO creacion_productos (nombre, descripcion, precio, imagen) VALUES (%s,%s,%s,%s)",(name,descripcion,precio,imagen,))
        mysql.connection.commit()

    return render_template('mos_prod.html')

# @app.route("/entrar/confirmar/<token>")
# def confirmarEmail(token):
#     try:
#         email=a.loads(token, salt='emcof', max_age=60)
#         cur = mysql.connection.cursor()
#         cur.execute("UPDATE users SET estado='1' WHERE email='"+email+"'")
#         cur.close()
#     except SignatureExpired:
#         cur = mysql.connection.cursor()
#         cur.execute("DELETE FROM users WHERE email='"+email+"' AND estado='0'")
#         cur.close()
#         return "<h1>EXPIRO EL TIEMPO VUELVA A INTERNTARLO</h1>"
#     return "<h1>"+email+"  CONFIRMADO BIENVENIDO</h1>"
""" 

if __name__ == '__main__':
    app.secret_key = "kamata16angulo"
    app.run(debug=True)