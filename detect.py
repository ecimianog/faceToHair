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
    while cap.isOpened():
        # Se captura la pantalla
        _, frame = cap.read()
        _, frames = cap.read()
        # print('Capture')
        lookFront = hd.lookFront(frames)
        if lookFront[0]:
            points = lookFront[1]
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

        # Se sale con Esc
        key = cv2.waitKey(1)
        if key == 27:
            break

        return frame


def getModel():
    #_, frames = cap.read()
    print(1)
    #lookFront = hd.lookFront(frames)
    print(2)
    models = dt.getDecision(points)
    print(3)
    return models
