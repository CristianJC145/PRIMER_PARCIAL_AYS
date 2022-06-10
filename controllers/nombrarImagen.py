from datetime import datetime
def nombrarImagen(imagen):
    now = datetime.now()
    fecha=str(now.hour)+str(now.minute)+str(now.second)
    nomImg = imagen.filename
    return str(fecha) +nomImg