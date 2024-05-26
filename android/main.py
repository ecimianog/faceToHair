import requests
import numpy as np
from io import BytesIO
from PIL import Image
import kivy
from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivy.clock import Clock

Builder.load_file("homescreen.kv")


class Homescreen(MDScreen):
    def __init__(self, **kwargs):
        super(Homescreen, self).__init__(**kwargs)
        # GET SELECTOR FROM KV FILE CAMERA
        print('aquí 1')
        # self.add_widget(Homescreen())
        if not hasattr(self, 'mycamera'):
            self.mycamera = self.ids.camera
            print('aquí 2')
            #self.myimage = Image()
            self.resultbox = self.ids.resultbox
            self.mybox = self.ids.mybox
        self.event = Clock.schedule_interval(self.sendImage, 2.0/1.0)

    def sendImage(self, *args):
        image_texture = self.mycamera.texture  # .export_as_image()
        pixels = image_texture.pixels
        image_array = np.frombuffer(pixels, dtype=np.uint8)
        image_array = image_array.reshape(
            (image_texture.height, image_texture.width, 4))
        pil_image = Image.fromarray(image_array)
        #image_data = imagen.tobytes('jpeg')
        image_bytes = BytesIO(image_array)
        print(1)
        img_bytes = BytesIO()
        print(2)
        pil_image.save(img_bytes, format="PNG")
        print(3)
        img_bytes.seek(0)
        print(4)
        # Abrir imagen
        if False:
            imagen = Image.open("imagen.png")
            # Convertir imagen a formato binario

        # Enviar solicitud POST con la imagen
        url = "http://192.168.1.3:5000/subir_imagen"  # Cambiar la URL según tu servidor
        archivos = {"imagen": img_bytes}
        response = requests.post(url, files=archivos)
        print(response)
        # Verificar respuesta
        if response.status_code == 200:
            print("Imagen enviada correctamente")
            print(response.content)
        elif not response.content:
            # Extract the image data from the response
            image_data = response.content
            print(2)
            # Convert the image data to a PIL Image object
            image = Image.open(BytesIO(image_data))
            print(23)
            # Display the image
            image.show()
            print(234)
        else:
            print("Error al enviar la imagen:", response.status_code)


class MyApp(MDApp):
    def build(self):
        return Homescreen()


if __name__ == "__main__":
    MyApp().run()


# sendImage()
