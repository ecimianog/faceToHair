from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivy.core.window import Window
from kivy.uix.image import Image
from kivymd.uix.list import MDList, OneLineAvatarListItem, ImageLeftWidget
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivy.clock import Clock
from kivy.uix.relativelayout import RelativeLayout
from kivy.graphics.texture import Texture
import kivysome
#from faceDetectorC import FaceDetector
import detect as dt
import time
import os
import PIL
import cv2

kivysome.enable(kivysome.LATEST, group=kivysome.FontGroup.REGULAR)
Window.size = (350, 900)

Builder.load_file("screenHome.kv")


class Homescreen(MDScreen):
    def __init__(self, **kwargs):
        super(Homescreen, self).__init__(**kwargs)
        index = 0
        self.selectedCamera = 0
        self.numberCameras = 0
        while True:
            cap = cv2.VideoCapture(index)
            try:
                if cap.getBackendName() == "MSMF":
                    self.numberCameras += 1
            except:
                break
            cap.release()
            index += 1

        print("Starting program")
        if not hasattr(self, 'mycamera'):
            self.mycamera = cv2.VideoCapture(0)
            print('aquí 2')
            if self.numberCameras > 1:
                self.buttonCamera = MDIconButton(
                    icon='camera-flip-outline', on_release=self.change_camera)
                self.ids.cameraBox.add_widget(self.buttonCamera)
            self.myimage = Image()
            self.ids.cameraBox.add_widget(self.myimage)
            self.resultbox = self.ids.resultbox
        print('Starting capture')
        self.event = Clock.schedule_interval(self.load_video, 1.0/30.0)

    def load_video(self, *args):
        # print('Capture1')
        frame = dt.headPoints(self.mycamera)
        buffer = cv2.flip(frame, 0).tobytes()
        texture = Texture.create(
            size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
        self.myimage.texture = texture
        # print('Capture2')

    def change_camera(self, *args):
        if self.selectedCamera == self.numberCameras - 1:
            self.selectedCamera = 0
        else:
            self.selectedCamera += 1
        # Prevent double click
        self.buttonCamera.icon = "clock-outline"
        self.buttonCamera.set_disabled(True)
        print('Changing camera to ', self.selectedCamera)
        self.mycamera = cv2.VideoCapture(self.selectedCamera)
        print('Change camera to ', self.selectedCamera)
        self.buttonCamera.set_disabled(False)
        self.buttonCamera.icon = "camera-flip-outline"

    def captureyouface(self):
        #print('self.mycamera', self.mycamera.texture)
        path = "images"
        if not os.path.exists(path):
            os.makedirs(path)
        path = path + "\myimage_" + time.strftime("%Y%m%d_%H%M%S") + ".png"

        # Guarda imagen
        self.myimage.export_to_png(path)
        self.event.cancel()
        self.myimage.source = path
        print(0)
        self.mycamera.release()
        print(1)
        self.clear_widgets()
        print(2)
        self.add_widget(ResultScreen(path, self.myimage))
        print(3)

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


Builder.load_file("screenResult.kv")


class ResultScreen(MDScreen):

    def __init__(self, valor, imagen, **kwargs):
        super(ResultScreen, self).__init__(**kwargs)
        # GET SELECTOR FROM KV FILE CAMERA
        print(valor)
        self.val = valor
        self.myimage1 = self.ids.image1
        self.myimage1.background_normal = valor
        self.myimage1.background_down = valor
        self.myimage2 = self.ids.image2
        self.myimage2.background_normal = valor
        self.myimage2.background_down = valor
        self.myimage3 = self.ids.image3
        self.myimage3.background_normal = valor
        self.myimage3.background_down = valor
        print('aquí 4')

    def selected(self, valSelected):
        print('sigue', valSelected)
        self.clear_widgets()
        self.add_widget(FinalScreen(self.val))

    def callback(self):
        print("button pressed")


Builder.load_file("screenFinal.kv")


class FinalScreen(MDScreen):

    def __init__(self, imagen, **kwargs):
        super(FinalScreen, self).__init__(**kwargs)
        self.val = imagen
        self.myimage = self.ids.imageF
        self.myimage.source = self.val
        self.mybutton = self.ids.imageB
        self.mybutton.background_normal = self.val
        self.mybutton.background_down = self.val

    def callback(self):
        print("button pressed")


class MyApp(MDApp):
    def build(self):
        return Homescreen()


if __name__ == "__main__":
    MyApp().run()
