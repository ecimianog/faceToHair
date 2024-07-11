# faceToHair

Aplicación de inteligencia artificial para reconocimiento y análisis de facciones de cabeza con recomendaciones de mejoramiento.

Primero realiza un reconocimiento de las facciones del rostro.
Después sugiere un patrón de mejoras estéticas.

Consta de 3 partes.

- Programa principal utilizado desde el lugar donde residen los recursos.
- Servidor.
- Cliente.

## Servidor en docker

docker pull ecimianog/fthserver

Creado:

- docker build --tag server-docker .
- docker tag server-docker ecimianog/fthserver
- docker push ecimianog/fthserver

## Instalación Principal y Servidor:

### Primero instalar python 3.10

- python 3.10

### Seguir los siguientes pasos para hacerlo funcionar desde un entorno virtual:

Primero instalar virtualenv

- pip install virtualenv

Luego crear el entorno virtual y activarlo

- python3.10 -m virtualenv v
- v\Scripts\activate

### Se sigue instalando las librerias necesarias:

Se pueden instalar las librerias con el comando:

- pip install -r requirements.txt

O se pueden seguir los siguientes pasos:

- python3.10 -m pip install "kivy[base,media]" kivy_examples
- python3.10 -m pip install kivymd
- python3.10 -m pip install opencv-python
- python3.10 -m pip install mediapipe
- python3.10 -m pip install "kivy[sdl2]"
- python3.10 -m pip install kivysome
- python3.10 -m pip install flask
- python3.10 -m pip install scikit-learn
- Descargar desde https://github.com/z-mahmud22/Dlib_Windows_Python3.x el siguiente archivo:
- python3.10 -m pip install dlib-19.22.99-cp310-cp310-win_amd64.whl

### Puesta en funcionamiento del principal:

Entrar a la carpeta donde se encuentra el proyecto.

- cd faceToHair

  Luego ejecutar el comando desde línea de comandos:

- python3.10 main.py

  O ejecutar el bat:

- r.bat

### Puesta en funcionamiento del servidor:

Luego ejecutar el comando desde línea de comandos:

- python3.10 server.py

  O ejecutar el bat:

- s.bat

En la carpeta requiredFiles se encuentra el archivo necesario para el reconocimiento facial con dlib. Se puede descargar de:

- download https://github.com/tzutalin/dlib-android/blob/master/data/shape_predictor_68_face_landmarks.dat

Se utilizan iconos Material Design de
https://pictogrammers.com/library/mdi/

## Instalación Android:

Habiendo instalado Python 3.10 en el paso anterior, se entra en la carpeta Android.

### Se sigue instalando las librerias necesarias:

Se puede crear una venv particular.

- pip install -r requirements.txt

Se debe poner en funcionamiento el servidor como se detalló en la sección anterior.

Se puede utilizar desde otro dispositivo en la misma red local ejecutando el main.py.

### Puesta en funcionamiento del cliente:

Dentro de la carpeta Android, ejecutar el comando desde línea de comandos:

- python3.10 main.py

O ejecutar el bat:

- r.bat

En la carpeta Android se encuentra un notebook para transformar la aplicación en APK.
