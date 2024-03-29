from __future__ import print_function
from flask import Flask, render_template, request, redirect, url_for, session,flash
from smtplib import SMTP
from email.message import EmailMessage
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
import hashlib 
from models import cartaModels
from controllers import enviarCorreo, validarContraseña, nombrarImagen
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
    return redirect(url_for('mos_pro'))

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
    return redirect(url_for('nu_contra', token=token)) 

@app.route('/nu_contra/<token>', methods=["GET", "POST"])
def nu_contra(token):
    if request.method == 'GET':
        return render_template("nu_contra.html")
    else:
        email = a.loads(token, salt='recuperarp')
        password = request.form.get('password')
        passwordEncriptada = hashlib.sha1(password.encode()).hexdigest()
        if (password == ""):
            flash('La contrasenia no puede ir vacia', 'error')
            return redirect(request.url)
        if (not validarContraseña.main(password)):
            flash('Esta contrasenia es invalida', 'error')
            return redirect(request.url)
        cartaModels.nuevaContrasenia(email,passwordEncriptada)
        flash('Se ha restablecido correctamente su contraseña', 'success')
        return redirect(url_for('entrar'))

@app.route('/registrar', methods=["GET", "POST"])
def registrar():
    if request.method == 'GET':
        return render_template("/homepage/registros.html")

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
        
    return render_template("index_producto.html")
     


@app.get('/mos_pro')
def mos_pro():
    id=str(session['user'][0])
    productos = cartaModels.productos(id)
    return render_template('/empresas/mos_prod.html',productos=productos)

@app.route('/cerrar') 
def cerrar():
    session.clear()

    return redirect(url_for('entrar'))


@app.route('/crea_prod', methods=['GET','POST'])
def crea_prod():
    if request.method == 'GET':
        estado= cartaModels.estado()
        return render_template("/empresas/crea_prod.html", estado = estado)

    idEmpresa= str(session['user'][0])
    name= request.form.get('name_pro')
    estado = request.form.get('est_productos')
    descripcion = request.form.get('des_producto')
    precio = request.form.get('pre_productos')
    imagen = request.files['img_producto']

    try:
        img =nombrarImagen.nombrarImagen(imagen)
        cartaModels.creaProd(idEmpresa= idEmpresa, estado= estado, name=name,descripcion=descripcion,precio=precio,imagen= '/static/resources/productos/'+img)
    except:
        flash('Error al crear el producto', 'error')
    imagen.save('./static/resources/productos/'+str(img))
    flash('Producto creado con exito', 'success')

    return redirect(url_for('mos_pro'))

@app.route('/eliminarpro/<int:id>')
def eliminarprod(id):
    cartaModels.eliminarprod(id)

    return redirect(url_for('mos_pro'))

@app.route('/e_prod/<int:id>', methods=['GET','POST'])
def editarprod(id):
    if request.method == 'GET':
        productos=cartaModels.edicionProducto(id)
        estado= cartaModels.estado()
        return render_template("/empresas/editar_producto.html", productos=productos, estado=estado)

""" 
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
""" 

if __name__ == '__main__':
    app.secret_key = "kamata16angulo"
    app.run(debug=True)