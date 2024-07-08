import cv2
import decisionTree as dt
import dlib
import headpose as hd
import math

print("Head Poses")

points = []
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(
    'requiredFiles\shape_predictor_68_face_landmarks.dat')

showThis = True


def hidemd():
    return hd.hidemd()


def hidelib():
    global showThis
    showThis = not showThis
    if not showThis:
        cv2.destroyWindow('Imagen para mandar')
    return showThis


def headPoints(cap):
    global points
    message = ''
    while cap.isOpened():
        # Se captura la pantalla
        _, frame = cap.read()
        _, frames = cap.read()
        # Se procesa en headpose
        result = hd.lookFront(frames)
        if result and result[0]:
            message = 'Calculando...'
            points = result[1]
        else:
            message = result[1]
        if result[0]:
            # Se captura en escala de grises para facilitar el proceso
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
        if showThis:
            cv2.imshow('Imagen para mandar', frame)

        return message, frame


def getModel():
    models = dt.getDecision(points)
    return models


def save_decision(model, name):
    dt.insertDecision(points, model, name)
