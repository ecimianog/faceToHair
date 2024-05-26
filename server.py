from flask import Flask, request, redirect, url_for, send_from_directory, abort
from werkzeug.utils import secure_filename
import os
import cv2
import numpy as np
from headpose import lookFront
from io import BytesIO

counter = 0
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
            return get_image(nombre_archivo)
            # Devolver una respuesta de éxito
            return redirect(url_for('index'))
        elif not saveImage:
            image_bytes = archivo.read()

            # Read the image data from BytesIO
            #image = cv2.imread(img_io)
            frame = cv2.imdecode(np.frombuffer(
                image_bytes, np.uint8), cv2.IMREAD_COLOR)
            result = lookFront(frame)
            if result and result[0]:
                return 'Calculando...'
            else:
                return result[1]
        else:
            # Devolver una respuesta de error
            return "Error al subir la imagen"


@app.route('/get_image/<filename>')
def get_image(filename):
    # Get the image path from the upload directory
    image_path = os.path.join(UPLOAD_FOLDER, filename)
    print(1)
    # Check if the image file exists
    if os.path.exists(image_path):
        # Send the image file as a response
        return send_from_directory(UPLOAD_FOLDER, filename)
    else:
        # Return a 404 error if the image is not found
        return abort(404)


@app.route('/')
def index():
    # Mostrar un mensaje de bienvenida
    return "Servidor para subir imágenes"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
