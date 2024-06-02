import cv2
import numpy as np
import dlib
import headpose as hd
import math

print("Head Poses")


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


def getRatios(marks):
    pAr = np.array([marks[0].x, marks[0].y, marks[0].z])
    pAl = np.array([marks[4].x, marks[4].y, marks[4].z])
    pBr = np.array([marks[1].x, marks[1].y, marks[1].z])
    pBl = np.array([marks[7].x, marks[7].y, marks[7].z])
    pCr = np.array([marks[2].x, marks[2].y, marks[2].z])
    pCl = np.array([marks[6].x, marks[6].y, marks[6].z])
    pDr = np.array([marks[3].x, marks[3].y, marks[3].z])
    pDl = np.array([marks[5].x, marks[5].y, marks[5].z])
    vA = np.array([marks[0].x, marks[0].y, marks[0].z,
                  marks[4].x, marks[4].y, marks[4].z])
    #magA = math.sqrt(sum(pow(element, 2) for element in vA))
    horizA = np.linalg.norm(pAr - pAl)
    horizB = np.linalg.norm(pBr - pBl)
    horizC = np.linalg.norm(pCr - pCl)
    horizD = np.linalg.norm(pDr - pDl)
    vertA = np.linalg.norm(pAr - pDr)
    vertB = np.linalg.norm(pAl - pDl)
    vertC = np.linalg.norm(pBr - pCl)
    vertD = np.linalg.norm(pBl - pCr)
    #magB = math.sqrt(sum(pow(element, 2) for element in vB))
    #magC = math.sqrt(sum(pow(element, 2) for element in vC))
    #magD = math.sqrt(sum(pow(element, 2) for element in vD))
    resultA = np.inner(pAr, pAl)
    resultB = np.inner(pBr, pBl)
    resultC = np.inner(pCr, pCl)
    resultD = np.inner(pDr, pDl)
    #print(resultA, resultB, resultC, resultD)
    print(horizA, horizB, horizC, horizD)
    print(vertA, vertB, vertC, vertD)
    return True


def headPoints(cap):
    while cap.isOpened():
        # Se captura la pantalla
        _, frame = cap.read()
        _, frames = cap.read()
        # print('Capture')
        lookFront = hd.lookFront(frames)
        if lookFront[0]:
            # Se captura en escala de grises para facilitar el proceso
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            getRatios(lookFront[1])
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
