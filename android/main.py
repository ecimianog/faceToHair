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
from kivy.core.image import Image as CoreImage

Builder.load_file("screenHomeAndroid.kv")
Window.size = (350, 600)


class Homescreen(MDScreen):
    def __init__(self, **kwargs):
        super(Homescreen, self).__init__(**kwargs)
        if not hasattr(self, 'mycamera'):
            self.mycamera = self.ids.camera
            self.label = self.ids.label
        # Envía imagen en intervalo de 2 segundos
        self.event = Clock.schedule_interval(self.sendImage, 2.0/1.0)

    # Envia imagen a la API
    def sendImage(self, *args):
        image_texture = self.mycamera.texture  # .export_as_image()
        pixels = image_texture.pixels
        # Convierte imagen en array
        image_array = np.frombuffer(pixels, dtype=np.uint8)
        image_array = image_array.reshape(
            (image_texture.height, image_texture.width, 4))
        # Convierte array en imagen Pil
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
            # Si el resultado es 'Calculando...' se ha realizado el cálculo y se pasa a sugerencias
            if returned == 'Calculando...':
                self.event.cancel()
                # self.mycamera.release()
                self.clear_widgets()
                self.add_widget(ResultScreen())
        else:
            print("Error al enviar la imagen:", response.status_code)


Builder.load_file("screenResultAndroid.kv")


class ResultScreen(MDScreen):

    def __init__(self, **kwargs):
        super(ResultScreen, self).__init__(**kwargs)
        self.myimage = []
        self.myimage.append(self.ids.image0)
        self.myimage.append(self.ids.image1)
        self.myimage.append(self.ids.image2)
        self.myimage.append(self.ids.image3)
        self.sendedImage()

    # Función para obtener las imágenes enviadas por el servidor
    def sendedImage(self):
        url = "http://192.168.1.3:5000/get_image/"
        response = requests.post(url+'0', params=0)
        if response.status_code == 200:
            buf = BytesIO(response.content)
            cim = CoreImage(buf, ext='jpg')
            self.myimage[0].texture = cim.texture
        response = requests.post(url+'1', params=0)
        if response.status_code == 200:
            buf = BytesIO(response.content)
            cim = CoreImage(buf, ext='jpg')
            self.myimage[1].texture = cim.texture
        response = requests.post(url+'2', params=0)
        if response.status_code == 200:
            buf = BytesIO(response.content)
            cim = CoreImage(buf, ext='jpg')
            self.myimage[2].texture = cim.texture
        response = requests.post(url+'3', params=0)
        if response.status_code == 200:
            buf = BytesIO(response.content)
            cim = CoreImage(buf, ext='jpg')
            self.myimage[3].texture = cim.texture
        elif False:
            # Convierte la imagen a objeto PIL
            image = Image.open(BytesIO(image_data))
            image.show()
            self.clear_widgets()
            self.add_widget(ResultScreen(image))

    # Si se selecciona imagen se pasa a la pantalla final
    def selected(self, valSelected):
        self.valSelected = valSelected
        print('Seleccionado', valSelected)
        self.clear_widgets()
        self.add_widget(FinalScreen(self.myimage[valSelected], valSelected))

    def callback(self):
        self.ids.backB.text = 'Volviendo'
        self.ids.backB.set_disabled(True)
        print('Volviendo')
        self.clear_widgets()
        self.add_widget(Homescreen())


Builder.load_file("screenFinalAndroid.kv")


class FinalScreen(MDScreen):

    def __init__(self, imagen, valSelected, **kwargs):
        super(FinalScreen, self).__init__(**kwargs)
        self.image = imagen
        self.valSelected = valSelected
        self.myimage = self.ids.imageF
        self.myimage.texture = self.image.texture

    # Se manda al servidor la decisión con el nombre del usuario
    def saveFinal(self):
        name = self.ids.name.text
        payload = {'name': name}
        url = "http://192.168.1.3:5000/save_decision/"
        response = requests.post(url+'0', params=payload)
        MyApp().stop()


class MyApp(MDApp):
    def build(self):
        return Homescreen()


if __name__ == "__main__":
    MyApp().run()


# sendImage()
