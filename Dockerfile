# Un archivo docker (dockerfile) comienza siempre importanto la imagen base. 
# Utilizamos la palabra clave 'FROM' para hacerlo.
# En nuestro ejemplo, queremos importar la imagen de python.
# Así que escribimos 'python' para el nombre de la imagen y 'latest' para la versión.
FROM python:3.10

RUN pip install "kivy[base,media]" kivy_examples
RUN pip install kivymd
RUN pip install opencv-python
RUN pip install mediapipe
RUN pip install "kivy[sdl2]"
RUN pip install kivysome
RUN pip install flask
RUN pip install *.whl
# Para lanzar nuestro código python, debemos importarlo a nuestra imagen.
# Utilizamos la palabra clave 'COPY' para hacerlo.
# El primer parámetro 'main.py' es el nombre del archivo en el host.
# El segundo parámetro '/' es la ruta donde poner el archivo en la imagen.
# Aquí ponemos el archivo en la carpeta raíz de la imagen. 
COPY server.py /

# Necesitamos definir el comando a lanzar cuando vayamos a ejecutar la imagen.
# Utilizamos la palabra clave 'CMD' para hacerlo.
# El siguiente comando ejecutará "python ./main.py".
CMD [ "python", "./server.py" ]