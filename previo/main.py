import kivy
print('b')
kivy.require('2.1.0')
print('c')
import cv2
import mediapipe
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
mp_face_mesh = mediapipe.solutions.face_mesh
mp_drawing = mediapipe.solutions.drawing_utils
#face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)
#drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)


class CamApp(App):
	def build(self):
		# GET SELECTOR FROM KV FILE CAMERA 
		print("Starting program")
    	#self.add_widget(Homescreen())
		self.img1 = Image()
		print(1)
		layout = BoxLayout()
		layout.add_widget(self.img1)
		print(2)
		self.capture = cv2.VideoCapture(0)
		print(3)
		Clock.schedule_interval(self.load_video, 1.0/30.0)
		print(4)
		return layout
		
	
	

	def load_video(self, *args):
		print('Capture1')
		cap = self.capture
		with mp_face_mesh.FaceMesh(
			max_num_faces = 3,
			refine_landmarks=True,
			min_detection_confidence=0.5,
			min_tracking_confidence=0.5) as face_mesh:
			ret, image = cap.read()
			image.flags.writeable = False
			image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
			face = face_mesh.process(image)
			image.flags.writeable = True
			image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
			if image.multi_face_landmarks:
				for face_landmarks in face.multi_face_landmarks:
					mp_drawing.draw_landmarks(
						image=image,
						landmark_list=face_landmarks,
						connections=mp_face_mesh.FACEMESH_CONTOURS,
						landmark_drawing_spec=drawing_spec,
						connection_drawing_spec=drawing_spec
					)

			buffer = cv2.flip(image, 0).tobytes()
			texture = Texture.create(size=(image.shape[1], image.shape[0]), colorfmt='bgr')
			texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
			self.img1.texture = texture
		print('Capture2')
    
	
    
        
	

if __name__ == "__main__":
	CamApp().run()

