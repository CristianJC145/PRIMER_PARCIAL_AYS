from config.database import db
def usuario(email, password):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE email = %s and password= %s and estado='1'", (email,password,))
    usuario = cursor.fetchone()
    return usuario

def consultarCorreo(email):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE email = %s and estado='1'", (email,))
    usuario = cursor.fetchone()
    return usuario
def nuevaContrasenia(email, passwordEncriptada):
    cursor = db.cursor()
    cursor.execute("update users set password = %s where email= %s", (passwordEncriptada, email,))
    db.commit()