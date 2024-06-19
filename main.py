from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
from kivymd.uix.label import MDLabel
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
import cv2

kivysome.enable(kivysome.LATEST, group=kivysome.FontGroup.REGULAR)
Window.size = (350, 600)

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
            self.info = self.ids.info
        print('Starting capture')
        self.event = Clock.schedule_interval(self.load_video, 1.0/30.0)

    def load_video(self, *args):
        # print('Capture1')
        message, frame = dt.headPoints(self.mycamera)
        buffer = cv2.flip(frame, 0).tobytes()
        texture = Texture.create(
            size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
        self.myimage.texture = texture
        self.info.text = message
        if message == 'Calculando...':
            self.ids.capture.disabled = False
        else:
            self.ids.capture.disabled = True
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
        print('Changed camera to ', self.selectedCamera)
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
        self.mycamera.release()

        pathImg = "hairStyles"
        rImgs = dt.getModel()
        pathImgA = os.path.join(pathImg, rImgs[0] + ".jpg")
        pathImgB = os.path.join(pathImg, rImgs[1] + ".jpg")
        pathImgC = os.path.join(pathImg, rImgs[2] + ".jpg")
        pathImgD = os.path.join(pathImg, rImgs[3] + ".jpg")
        pathImgs = [pathImgA, pathImgB, pathImgC, pathImgD]
        self.clear_widgets()
        self.add_widget(ResultScreen(pathImgs, path, rImgs))

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

    def __init__(self, pathImgs, imagen, models, **kwargs):
        super(ResultScreen, self).__init__(**kwargs)
        # GET SELECTOR FROM KV FILE CAMERA
        print(imagen)
        self.val = imagen
        self.models = models
        self.valSelected = False
        self.pathImgs = pathImgs
        self.myimage1 = self.ids.image1
        self.myimage1.source = pathImgs[0]
        self.myimage2 = self.ids.image2
        self.myimage2.source = pathImgs[1]
        self.myimage3 = self.ids.image3
        self.myimage3.source = pathImgs[2]
        self.myimage4 = self.ids.image4
        self.myimage4.source = pathImgs[3]

    def selected(self, valSelected):
        self.valSelected = valSelected
        print('Seleccionado', valSelected)
        self.clear_widgets()
        self.add_widget(FinalScreen(
            self.pathImgs[valSelected], self.models[valSelected], valSelected))

    def callback(self):
        self.ids.backB.text = 'Volviendo'
        self.ids.backB.set_disabled(True)
        print('Volviendo')
        self.clear_widgets()
        self.add_widget(Homescreen())


Builder.load_file("screenFinal.kv")


class FinalScreen(MDScreen):

    def __init__(self, imagen, model, valSelected, **kwargs):
        super(FinalScreen, self).__init__(**kwargs)
        self.val = imagen
        self.model = model
        self.valSelected = valSelected
        self.myimage = self.ids.imageF
        self.myimage.source = self.val

    def saveFinal(self):
        name = self.ids.name.text
        dt.save_decision(self.model, name)
        MyApp().stop()


class MyApp(MDApp):
    def build(self):
        return Homescreen()


if __name__ == "__main__":
    MyApp().run()
