import cv2
import numpy as np
import dlib

cap = cv2.VideoCapture(0)

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

print("Head Pose")

def headPoints():

    

    _, frame = cap.read()
    #_, frames = cap.read()
    
    # 

    # Se captura la pantalla
    #print('Capture')
    # Se captura en blanco y negro para facilitar el proceso
    #lookFront = hd.lookFront(frames)
    if True: #lookFront:
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
            for n in range(0, 68):
                x = landmarks.part(n).x
                y = landmarks.part(n).y
                cv2.circle(frame, (x,y), 3, (255,0,0), -1)
        return frame    
            #print(face, landmarks)
    
    # Se muestra la imagen
    