import cv2
import numpy as np
import dlib
import headpose as hd
import mediapipe as mp

print("Head Pose")

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils
drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)


cap = cv2.VideoCapture(0)

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

# 
while cap.isOpened():
    # Se captura la pantalla
    _, frame = cap.read()
    _, frames = cap.read()
    #print('Capture')
    # Se captura en blanco y negro para facilitar el proceso
    lookFront = hd.lookFront(frames)
    if lookFront:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # La imagen se pasa al detector de la librería
        faces = detector(gray)
        # Se devuelven varios objetos
        for face in faces:
            # Se toma un objeto devuelto del que se toman las coordenadas
            #print('Detect face')
            x1 = face.left()
            y1 = face.top()
            x2 = face.right()
            y2 = face.bottom()
            # Se dibuja un rectángulo con las coordenadas
            cv2.rectangle(frame, (x1,y1), (x2,y2), (0, 255, 0), 3)
            
            # Se pasa la imagen y el objeto face al predictor de marcas
            landmarks = predictor(gray, face)
            # Se recorren las marcas para dibujarlas sobre la imagen
            for n in range(0, 28):
                x = landmarks.part(n).x
                y = landmarks.part(n).y
                cv2.circle(frame, (x,y), 1, (255,0,0), -1)
                
            for n in range(29, 68):
                x = landmarks.part(n).x
                y = landmarks.part(n).y
                cv2.circle(frame, (x,y), 1, (255,255,0), -1)
            
            #print(face, landmarks)
    
    # Se muestra la imagen
    cv2.imshow('Frame', frame)
    
    # Se sale con Esc
    key = cv2.waitKey(1)
    if key == 27:
        break