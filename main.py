from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivy.core.window import Window
from kivy.uix.image import Image
from kivymd.uix.list import MDList, OneLineAvatarListItem, ImageLeftWidget
from kivy.clock import Clock
from kivy.graphics.texture import Texture
#from faceDetectorC import FaceDetector
import detect as dt
import time
import os
import PIL
import cv2


Window.size = (350, 900)

Builder.load_file("homescreen.kv")


class Homescreen(MDScreen):
    def __init__(self, **kwargs):
        super(Homescreen, self).__init__(**kwargs)
        print("Starting program")
        if not hasattr(self, 'mycamera'):
            self.mycamera = cv2.VideoCapture(1)
            print('aquí 2')
            self.myimage = Image()
            self.add_widget(self.myimage)
            self.resultbox = self.ids.resultbox
            self.mybox = self.ids.mybox
            self.button = self.ids.HSMd
        print('Starting capture')
        Clock.schedule_interval(self.load_video, 1.0/30.0)

    def load_video(self, *args):
        # print('Capture1')
        frame = dt.headPoints()
        buffer = cv2.flip(frame, 0).tobytes()
        texture = Texture.create(
            size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
        self.myimage.texture = texture
        # print('Capture2')
#

    def captureyouface(self):
        print('self.mycamera', self.mycamera.texture)
        path = "images"
        # Check whether the specified path exists or not
        if not os.path.exists(path):
            os.makedirs(path)
        path = path + "\myimage_" + time.strftime("%Y%m%d_%H%M%S") + ".png"

        # EXPORT CAMERA CAPTURE TO PNG IMAGE
        self.mycamera.export_to_png(path)
        self.myimage.source = path
        self.resultbox.add_widget(
            OneLineAvatarListItem(
                ImageLeftWidget(
                    source=path,
                    size_hint_x=0.3,
                    size_hint_y=1,
                    size=(300, 300)
                ),
                text=self.ids.name.text
            )

        )
        self.mycamera.play = False
        self.clear_widgets()
        texture = self.mycamera.texture
        size = texture.size
        pixels = texture.pixels
        pil_image = PIL.Image.frombytes(mode='RGBA', size=size, data=pixels)

        self.add_widget(ResultScreen(path, pil_image))

    def hidemd(self):
        if dt.hidemd():
            self.ids.HSMd.text = "Hide MD"
        else:
            self.ids.HSMd.text = "Show MD"

    def hidelib(self):
        if dt.hidelib():
            self.ids.HSLib.text = "Hide Lib"
        else:
            self.ids.HSLib.text = "Show Lib"


Builder.load_file("resultScreen.kv")


class ResultScreen(MDScreen):

    def __init__(self, valor, imagen, **kwargs):
        super(ResultScreen, self).__init__(**kwargs)
        # GET SELECTOR FROM KV FILE CAMERA
        print(valor)
        self.val = valor
        self.myimage = self.ids.image
        self.myimage.source = self.val
        print('aquí 4')
        self.mybox = self.ids.name2
        self.mybox1 = self.ids.name3
        self.myimage.texture = FaceDetector(valor)

    def captureyouface(self):
        # CREATE TIMESTAMP NOT FOR YOU FILE IMAGE
        # THIS SCRIPT GET TIME MINUTES AND DAY NOW
        print('vuelve')
        self.clear_widgets()
        self.add_widget(ResultScreen2('última', self.val))


class MyApp(MDApp):
    def build(self):
        return Homescreen()


if __name__ == "__main__":
    MyApp().run()
