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

# Definir directorio para guardar imágenes
UPLOAD_FOLDER = os.path.join(app.instance_path, 'imagenes')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
print(UPLOAD_FOLDER)


@app.route('/subir_imagen', methods=['POST'])
def subir_imagen():
    saveImage = False
    # Verificar si se ha enviado un archivo
    if request.method == 'POST':
        global counter
        counter += 1
        # Obtener el archivo de imagen
        archivo = request.files['imagen']
        # Verificar si el archivo es válido
        if saveImage and archivo and archivo.filename:
            # Guardar el archivo con un nombre seguro
            nombre_archivo = secure_filename(archivo.filename)
            cStr = str(counter)
            archivo.save(os.path.join(
                UPLOAD_FOLDER, nombre_archivo + cStr + '.png'))
            return cStr
            return redirect(url_for('index'))
        elif not saveImage:
            image_bytes = archivo.read()

            # Read the image data from BytesIO
            #image = cv2.imread(img_io)
            frame = cv2.imdecode(np.frombuffer(
                image_bytes, np.uint8), cv2.IMREAD_COLOR)
            result = lookFront(frame)
            if result and result[0]:
                setModel(result[1])
                return 'Calculando...'
            else:
                return result[1]
        else:
            # Devolver una respuesta de error
            return "Error al subir la imagen"


@app.route('/get_image/<id>', methods=['POST'])
def get_image(id):
    if request.method == 'POST':
        # Obtener el archivo de imagen
        qqq = request.args.get('params')
    # Get the image path from the upload directory
        print(qqq)
        print(modelsPath[int(id)])
        return send_from_directory("hairStyles", modelsPath[int(id)])


@app.route('/save_decision/<id>', methods=['POST'])
def save_decision(id):
    if request.method == 'POST':
        # Obtener el archivo de imagen
        name = request.args.get('name')
        print(1, modelsPath[int(id)])
        print(2, name)
        dt.insertDecision(listPoints, models[int(id)], name)
        # sendDecision(id)
        return 'True'


@app.route('/')
def index():
    # Mensaje de bienvenida para Index
    return "Servidor para subir imágenes"


def setModel(points):
    global listPoints
    global modelsPath
    global models
    #_, frames = cap.read()
    print(1)
    #lookFront = hd.lookFront(frames)
    print(2)
    rImgs = dt.getDecision(points)
    listPoints = points
    models = rImgs
    print(3)
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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
