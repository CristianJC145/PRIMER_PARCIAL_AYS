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
def productos(id):
    cursor=db.cursor()
    cursor.execute("""SELECT `creacion_productos`.`id_producto`, `imagen`, `nombre`, `precio`, `estado`.`estado`
	FROM `creacion_productos`
	INNER JOIN `estado`ON `creacion_productos`.`id_estado` = `estado`.`id`
	WHERE id_empresa = %s
	GROUP BY `creacion_productos`.`id_producto`""", (id,))
    productos = cursor.fetchall()
    return productos
def empresa(id):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE id = %s", (id,))
    empresa = cursor.fetchone()
    return empresa
def creaProd(idEmpresa, estado, name,descripcion,precio,imagen):
    cursor = db.cursor()
    cursor.execute("""insert into creacion_productos(
                id_empresa,
                id_estado,
                nombre,
                precio,
                descripcion,
                imagen
            )values (%s,%s,%s,%s,%s,%s)
        """, (idEmpresa,estado,name, precio, descripcion, imagen,))
    db.commit()

def estado():
    cursor = db.cursor()
    cursor.execute("select * from estado")
    estado = cursor.fetchall()
    return estado

def eliminarprod(id):
    cursor=db.cursor()
    cursor.execute("DELETE from creacion_productos WHERE id_producto=%s",(id,))
    db.commit()
def edicionProducto(id):
    cursor=db.cursor()
    cursor.execute("""SELECT `creacion_productos`.`id_producto`,`nombre`,`precio`, `estado`.`estado`, `descripcion`
	FROM `creacion_productos`
	INNER JOIN `estado`ON `creacion_productos`.`id_estado` = `estado`.`id`
	WHERE id_producto = %s
	GROUP BY `creacion_productos`.`id_producto`""", (id,))
    edicionProducto= cursor.fetchone()
    return edicionProducto