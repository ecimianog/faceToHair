from flask import Flask, request, redirect, url_for, send_from_directory, abort
from werkzeug.utils import secure_filename
import os
import cv2
import numpy as np
from headpose import lookFront
from io import BytesIO
import decisionTree as dt

modelsPath = []
models = []
counter = 0
listPoints = []
app = Flask(__name__)

UPLOAD_FOLDER = os.path.join(app.instance_path, 'imagenes')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Llamada para recibir imagen de la cámara


@app.route('/subir_imagen', methods=['POST'])
def subir_imagen():
    saveImage = False
    # Verificar si se ha enviado un archivo
    if request.method == 'POST':
        global counter
        counter += 1
        archivo = request.files['imagen']
        # Sección no operativa para guardar la imagen en el servidor
        if saveImage and archivo and archivo.filename:
            # Guardar el archivo con un nombre seguro
            nombre_archivo = secure_filename(archivo.filename)
            cStr = str(counter)
            archivo.save(os.path.join(
                UPLOAD_FOLDER, nombre_archivo + cStr + '.png'))
            return cStr
            # return redirect(url_for('index'))
        # Sección operativa que recibe la imagen de la cámara y pide el proceso
        elif not saveImage:
            image_bytes = archivo.read()
            frame = cv2.imdecode(np.frombuffer(
                image_bytes, np.uint8), cv2.IMREAD_COLOR)
            result = lookFront(frame)
            if result and result[0]:
                setModel(result[1])
                return 'Calculando...'
            else:
                return result[1]
        else:
            return "Error al subir la imagen"

# Llamada para obtener la imagen del modelo sugerido


@app.route('/get_image/<id>', methods=['POST'])
def get_image(id):
    if request.method == 'POST':
        # Obtener el archivo de imagen
        return send_from_directory("hairStyles", modelsPath[int(id)])

# Llamada para guardar la decisión del modelo elegido


@app.route('/save_decision/<id>', methods=['POST'])
def save_decision(id):
    if request.method == 'POST':
        name = request.args.get('name')
        dt.insertDecision(listPoints, models[int(id)], name)
        return 'True'


# Mensaje de bienvenida para Index
@app.route('/')
def index():
    return "Servidor para subir imágenes"

# Guarda los modelos y sus rutas


def setModel(points):
    global listPoints
    global modelsPath
    global models
    rImgs = dt.getDecision(points)
    listPoints = points
    models = rImgs
    pathImg = "hairStyles"
    pathImgA = os.path.join(pathImg, rImgs[0] + ".jpg")
    pathImgB = os.path.join(pathImg, rImgs[1] + ".jpg")
    pathImgC = os.path.join(pathImg, rImgs[2] + ".jpg")
    pathImgD = os.path.join(pathImg, rImgs[3] + ".jpg")
    pathImgA = rImgs[0] + ".jpg"
    pathImgB = rImgs[1] + ".jpg"
    pathImgC = rImgs[2] + ".jpg"
    pathImgD = rImgs[3] + ".jpg"
    modelsPath = [pathImgA, pathImgB, pathImgC, pathImgD]


# Servidor en debug para local
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
