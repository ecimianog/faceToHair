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
from kivy.core.window import Window

Builder.load_file("screenHomeAndroid.kv")
Window.size = (350, 600)


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
            self.label = self.ids.label
        self.event = Clock.schedule_interval(self.sendImage, 2.0/1.0)

    def sendImage(self, *args):
        image_texture = self.mycamera.texture  # .export_as_image()
        pixels = image_texture.pixels
        image_array = np.frombuffer(pixels, dtype=np.uint8)
        image_array = image_array.reshape(
            (image_texture.height, image_texture.width, 4))
        pil_image = Image.fromarray(image_array)
        img_bytes = BytesIO()
        pil_image.save(img_bytes, format="PNG")
        img_bytes.seek(0)
        # Enviar solicitud POST con la imagen
        url = "http://192.168.1.3:5000/subir_imagen"  # Cambiar la URL según tu servidor
        archivos = {"imagen": img_bytes}
        response = requests.post(url, files=archivos)
        # Verificar respuesta
        if response.status_code == 200:
            print("Imagen enviada correctamente")
            returned = response.content.decode(
                "utf-8", errors="replace")
            self.label.text = returned
            print(9, returned)
            if returned == 'Calculando...':
                self.sendedImage()
        else:
            print("Error al enviar la imagen:", response.status_code)

    def sendedImage(self):
        print(99999999999999999999999999999999)
        url = "http://192.168.1.3:5000/get_image/"
        response = requests.post(url+'0', params=0)
        if response.status_code == 200:
            print(response.content)
        response = requests.post(url+'1', params=0)
        if response.status_code == 200:
            print(response.content)
        response = requests.post(url+'2', params=0)
        if response.status_code == 200:
            print(response.content)
        response = requests.post(url+'3', params=0)
        if response.status_code == 200:
            print(response.content)
        elif False:
            # Convert the image data to a PIL Image object
            image = Image.open(BytesIO(image_data))
            # Display the image
            image.show()
            self.clear_widgets()
            self.add_widget(ResultScreen(image))


Builder.load_file("screenResultAndroid.kv")


class ResultScreen(MDScreen):

    def __init__(self, Imgs, **kwargs):
        super(ResultScreen, self).__init__(**kwargs)
        # GET SELECTOR FROM KV FILE CAMERA
        self.Imgs = Imgs
        self.myimage1 = self.ids.image1
        self.myimage1.source = Imgs[0]
        self.myimage2 = self.ids.image2
        self.myimage2.source = Imgs[1]
        self.myimage3 = self.ids.image3
        self.myimage3.source = Imgs[2]
        self.myimage4 = self.ids.image4
        self.myimage4.source = Imgs[3]

    def selected(self, valSelected):
        self.valSelected = valSelected
        print('Seleccionado', valSelected)
        self.clear_widgets()
        self.add_widget(FinalScreen(self.Imgs[valSelected]))

    def callback(self):
        self.ids.backB.text = 'Volviendo'
        self.ids.backB.set_disabled(True)
        print('Volviendo')
        self.clear_widgets()
        self.add_widget(Homescreen())


Builder.load_file("screenFinalAndroid.kv")


class FinalScreen(MDScreen):

    def __init__(self, imagen, **kwargs):
        super(FinalScreen, self).__init__(**kwargs)
        self.val = imagen
        self.myimage = self.ids.imageF
        self.myimage.source = self.val

    def callback(self):
        print("button pressed")


class MyApp(MDApp):
    def build(self):
        return Homescreen()


if __name__ == "__main__":
    MyApp().run()


# sendImage()
