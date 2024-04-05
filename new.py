# coding:utf-8
from kivymd.app import MDApp
from kivy.uix.image import Image
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import cv2
import numpy as np

class MainApp(MDApp):
    
    def build(self):
        layout = MDBoxLayout(orientation='vertical')
        self.image = Image()
        layout.add_widget(self.image)
        layout.add_widget(MDRaisedButton(
            text='click',
            pos_hint={'center_x': .5, 'center_y': .5},
            size_hint=(None, None)
        ))
        self.capture = cv2.VideoCapture(0)
        Clock.schedule_interval(self.load_video, 1.0/30.0)
        return layout
    
    def load_video(self, *args):
        ret, frame = self.capture.read()
        self.image_frame = frame
        buffer = cv2.flip(frame, 0).tostring()
        texture =Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
        self.image.texture = texture





if __name__ == '__main__':
    MainApp().run()