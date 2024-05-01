import cv2
import math
import numpy as np
import dlib
import headpose as hd
import mediapipe as mp

print("Head Pose")

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils
drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)


cap = cv2.VideoCapture(1)

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')


def getRatios(marks):
    vAa = np.array([marks[0].x, marks[0].y, marks[0].z])
    vAb = np.array([marks[4].x, marks[4].y, marks[4].z])
    vBa = np.array([marks[1].x, marks[1].y, marks[1].z])
    vBb = np.array([marks[7].x, marks[7].y, marks[7].z])
    vCa = np.array([marks[2].x, marks[2].y, marks[2].z])
    vCb = np.array([marks[6].x, marks[6].y, marks[6].z])
    vDa = np.array([marks[3].x, marks[3].y, marks[3].z])
    vDb = np.array([marks[5].x, marks[5].y, marks[5].z])

    #magA = math.sqrt(sum(pow(element, 2) for element in vA))
    #magB = math.sqrt(sum(pow(element, 2) for element in vB))
    #magC = math.sqrt(sum(pow(element, 2) for element in vC))
    #magD = math.sqrt(sum(pow(element, 2) for element in vD))
    #print(magA,magB,magC, magD)
    resultA = np.inner(vAa, vAb)
    resultB = np.inner(vBa, vBb)
    resultC = np.inner(vCa, vCb)
    resultD = np.inner(vDa, vDb)
    return True


def headPoints():
    while cap.isOpened():
        # Se captura la pantalla
        _, frame = cap.read()
        _, frames = cap.read()
        # print('Capture')
        # Se captura en blanco y negro para facilitar el proceso
        lookFront = hd.lookFront(frames)
        if lookFront:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            getRatios(lookFront)
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
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)

                # Se pasa la imagen y el objeto face al predictor de marcas
                landmarks = predictor(gray, face)
                # Se recorren las marcas para dibujarlas sobre la imagen
                for n in range(0, 28):
                    x = landmarks.part(n).x
                    y = landmarks.part(n).y
                    cv2.circle(frame, (x, y), 1, (255, 0, 0), -1)

                for n in range(29, 68):
                    x = landmarks.part(n).x
                    y = landmarks.part(n).y
                    cv2.circle(frame, (x, y), 1, (255, 255, 0), -1)

                #print(face, landmarks)

        # Se muestra la imagen
        cv2.imshow('Frame', frame)

        # Se sale con Esc
        key = cv2.waitKey(1)
        if key == 27:
            break

        return frame
