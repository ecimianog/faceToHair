# faceToHair

COLOCAR CÁMARA A 0
Aplicación de inteligencia artificial para reconocimiento y análisis de facciones de cabeza con recomendaciones de mejoramiento.

Primero realiza un reconocimiento de las facciones del rostro.
Después sugiere un patrón de mejoras estéticas.

Instalación:
python 3.10
download https://github.com/z-mahmud22/Dlib_Windows_Python3.x
download https://github.com/tzutalin/dlib-android/blob/master/data/shape_predictor_68_face_landmarks.dat
pip install -r requirements.txt

python3.10 -m virtualenv v
v\Scripts\activate
python3.10 -m pip install "kivy[base,media]" kivy_examples
python3.10 -m pip install kivymd
python3.10 -m pip install opencv-python
python3.10 -m pip install mediapipe
python3.10 -m pip install dlib-19.22.99-cp310-cp310-win_amd64.whl
python3.10 -m pip install "kivy[sdl2]"
cd faceToHair
python3.10 main.py
