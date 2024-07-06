import cv2
import numpy as np
import mediapipe as mp
from mediapipe.framework.formats import landmark_pb2

# Configuracion de mediapipe
mpFaceMesh = mp.solutions.face_mesh
faceMesh = mpFaceMesh.FaceMesh(
    min_detection_confidence=0.5, min_tracking_confidence=0.5)
# Configuracion de dibujo de puntos en la imagen
mpDrawing = mp.solutions.drawing_utils
drawingSpecA = mpDrawing.DrawingSpec(
    color=(0, 255, 0), thickness=1, circle_radius=1)
drawingSpecB = mpDrawing.DrawingSpec(
    color=(255, 0, 0), thickness=3, circle_radius=1)
drawingSpecC = mpDrawing.DrawingSpec(
    color=(255, 255, 255), thickness=1, circle_radius=1)
drawingSpecD = mpDrawing.DrawingSpec(
    color=(255, 100, 0), thickness=3, circle_radius=1)
drawingSpec = mpDrawing.DrawingSpec(
    color=(0, 0, 0), thickness=1, circle_radius=0)

# Definicion del identificador para dibujar los puntos según zonas de la cara
EYEBROW_LANDMARKS = [70, 63, 105, 66, 107, 336, 296, 334, 293, 300]
LIPS_LANDMARKS = [61, 146, 91, 181, 84, 17, 314, 405, 405, 321,
                  321, 375, 375, 291, 61, 185, 185, 40, 40, 39, 39, 37, 37, 0, 0, 267, 267,
                  269, 269, 270, 270, 409, 409, 291, 78, 95, 95, 88, 88, 178, 178, 87, 87, 14,
                  14, 317, 317, 402, 402, 318, 318, 324, 324, 308, 78, 191, 191, 80, 80, 81,
                  81, 82, 82, 13, 13, 312, 312, 311, 311, 310, 310, 415, 415, 308]
LEFT_EYE_LANDMARKS = [33, 7, 163, 144, 145, 153, 154, 155, 155, 133,
                      33, 246, 246, 161, 161, 160, 160, 159, 159, 158, 158, 157, 157, 173, 173,
                      133]
LEFT_EYEBROW_LANDMARKS = [46, 53, 52, 65, 55, 70, 63, 105, 66, 107]
LEFT_IRIS_LANDMARKS = [474, 475, 476, 477, 474]
RIGHT_EYE_LANDMARKS = [263, 249, 390, 373, 374, 380, 381, 382, 382,
                       362, 263, 466, 466, 388, 388, 387, 387, 386, 386, 385, 385, 384, 384, 398,
                       398, 362]
RIGHT_EYEBROW_LANDMARKS = [276, 283, 282, 295, 285, 300, 293, 334, 296,
                           336]
RIGHT_IRIS_LANDMARKS = [469, 470, 471, 472, 469]
FACE_OVAL_LANDMARKS = [10, 338, 297, 332, 284, 251, 389, 356, 356,
                       454, 454, 323, 323, 361, 361, 288, 288, 397, 397, 365, 365, 379, 379, 378,
                       378, 400, 400, 377, 377, 152, 152, 148, 148, 176, 176, 149, 149, 150, 150,
                       136, 136, 172, 172, 58, 58, 132, 132, 93, 93, 234, 234, 127, 127, 162, 162,
                       21, 21, 54, 54, 103, 103, 67, 67, 109, 109, 10]
# Definición de puntos de referencia para devovler
FACE_OVAL_PASS = [10, 152, 454, 234, 332, 103, 389, 162, 361, 132, 400, 176]
FACE_OVAL_PASS_ID = ['pTop', 'pDown', 'pMr', 'pMl', 'pAr', 'pAl',
                     'pBr', 'pBl', 'pCr', 'pCl', 'pDr', 'pDl']
CONTROL_POINTS_ORIENTATION = [1, 33, 61, 263, 291, 199]

showThis = True

# Función para mostrar y ocultar ventana


def hidemd():
    global showThis
    showThis = not showThis
    if not showThis:
        cv2.destroyWindow('Imagen con puntos separados')
    return showThis

# Función de la imagen con los puntos de referencia


def lookFront(image):
    faceOvalMarks = {}
    # Se prepara la imagen para procesarla
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    face = faceMesh.process(image)
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    imageHeight, imageWidth, noneC = image.shape
    face3d = []
    face2d = []

    if face.multi_face_landmarks:
        # Si la imagen tiene puntos detectados, se realiza el proceso
        for faceLandmarks in face.multi_face_landmarks:
            # Se itera por los puntos de la cara y se guardan en una lista según el tipo de punto
            # Cejas
            eyebrowLandmarksA = landmark_pb2.NormalizedLandmarkList()
            eyebrowLandmarksA.landmark.extend(
                [faceLandmarks.landmark[id] for id in LEFT_EYEBROW_LANDMARKS])
            eyebrowLandmarksA.landmark.extend(
                [faceLandmarks.landmark[id] for id in RIGHT_EYEBROW_LANDMARKS])
            mpDrawing.draw_landmarks(
                image=image,
                landmark_list=eyebrowLandmarksA,
                connections=[],
                landmark_drawing_spec=drawingSpecA,
                connection_drawing_spec=drawingSpecA
            )
            # Labios
            lipsLandmarksB = landmark_pb2.NormalizedLandmarkList()
            lipsLandmarksB.landmark.extend(
                [faceLandmarks.landmark[id] for id in LIPS_LANDMARKS])
            mpDrawing.draw_landmarks(
                image=image,
                landmark_list=lipsLandmarksB,
                connections=[],
                landmark_drawing_spec=drawingSpecB,
                connection_drawing_spec=drawingSpecB
            )
            # Ojos
            eyeLandmarksC = landmark_pb2.NormalizedLandmarkList()
            eyeLandmarksC.landmark.extend(
                [faceLandmarks.landmark[id] for id in RIGHT_EYE_LANDMARKS])
            eyeLandmarksC.landmark.extend(
                [faceLandmarks.landmark[id] for id in LEFT_EYE_LANDMARKS])
            mpDrawing.draw_landmarks(
                image=image,
                landmark_list=eyeLandmarksC,
                connections=[],
                landmark_drawing_spec=drawingSpecC,
                connection_drawing_spec=drawingSpecC
            )
            # Óvalo de la cara limitando a los puntos de control
            ovalLandmarksD = landmark_pb2.NormalizedLandmarkList()
            ovalLandmarksD.landmark.extend(
                [faceLandmarks.landmark[id] for id in FACE_OVAL_PASS])
            mpDrawing.draw_landmarks(
                image=image,
                landmark_list=ovalLandmarksD,
                connections=[],
                landmark_drawing_spec=drawingSpecD,
                connection_drawing_spec=drawingSpecD
            )
            # Se prepara otra lista para el resto de puntos
            restLandmarks = landmark_pb2.NormalizedLandmarkList()
            for idx, lm in enumerate(faceLandmarks.landmark):
                # Puntos de control para la orientación de la cabeza
                if idx in CONTROL_POINTS_ORIENTATION:
                    x, y = int(lm.x * imageWidth), int(lm.y * imageHeight)
                    face2d.append([x, y])
                    face3d.append([x, y, lm.z])
                # Se agregan a la lista de restantes los correspondientes
                if idx not in LEFT_EYEBROW_LANDMARKS and idx not in RIGHT_EYEBROW_LANDMARKS and idx not in LIPS_LANDMARKS and idx not in LEFT_EYE_LANDMARKS and idx not in LEFT_IRIS_LANDMARKS and idx not in RIGHT_EYE_LANDMARKS and idx not in RIGHT_IRIS_LANDMARKS and idx not in FACE_OVAL_LANDMARKS:
                    restLandmarks.landmark.extend(
                        [faceLandmarks.landmark[idx]])
                # Se agrega a la lista de puntos para el óvalo
                if idx in FACE_OVAL_PASS:
                    ind = FACE_OVAL_PASS.index(idx)
                    faceOvalMarks[FACE_OVAL_PASS_ID[ind]] = lm

            # Conversión a arrays numpy.
            face2d = np.array(face2d, dtype=np.float64)
            face3d = np.array(face3d, dtype=np.float64)
            # Longitud focal estimada. Se ha de calibrar según la cámara.
            focalLength = 1 * imageWidth
            # Matriz de la cámara.
            camMatrix = np.array([[focalLength, 0, imageHeight / 2],
                                  [0, focalLength, imageHeight / 2],
                                  [0, 0, 1]])
            # Matriz de distorsión (asumida como cero).
            distMatrix = np.zeros((4, 1), dtype=np.float64)
            # Calcula los datos de pose para encontrar la rotación y la traslación de la cabeza.
            ss, rotationVector, tv = cv2.solvePnP(
                face3d, face2d, camMatrix, distMatrix)
            # Convierte el vector de rotación a matriz de rotación
            rotationMatrix, jc = cv2.Rodrigues(rotationVector)
            # Descompone la matriz de rotación en ángulos de Euler
            angles, mtxR, mtxQ, Qx, Qy, Qz = cv2.RQDecomp3x3(rotationMatrix)
            # Rotación en grados.
            xGrades = angles[0] * 360
            yGrades = angles[1] * 360
            zGrades = angles[2] * 360

            # Establece un margen de admisión para tomar la orientación como correcta y crea un mensaje
            valid = False
            msg = ' - Mire de frente'
            if yGrades < -10:
                msg = 'Izquierda' + msg
            elif yGrades > 10:
                msg = 'Derecha' + msg
            elif xGrades < -10:
                msg = 'Abajo' + msg
            elif xGrades > 10:
                msg = 'Arriba' + msg
            else:
                msg = ''
                valid = True

            # Si se muestra la ventana, se muestra el texto generado
            if showThis:
                cv2.putText(image, msg, (20, 450),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.1, (0, 0, 255), 2)
                cv2.putText(image, 'x: ' + str(np.round(xGrades, 2)), (500, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
                cv2.putText(image, 'y: ' + str(np.round(yGrades, 2)), (500, 100),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
                cv2.putText(image, 'z: ' + str(np.round(zGrades, 2)), (500, 150),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
                mpDrawing.draw_landmarks(
                    image=image,
                    landmark_list=restLandmarks,
                    connections=[],
                    landmark_drawing_spec=drawingSpec,
                    connection_drawing_spec=drawingSpec
                )
                cv2.imshow('Imagen con puntos separados', image)

            # Se sale con Esc
            key = cv2.waitKey(1)
            if key == 27:
                break
            # Envía resultado
            if valid:
                return [True, faceOvalMarks]
            else:
                return [False, msg]
    # Si la imagen no tiene puntos detectados, se envía respuesta no satisfactoria
    else:
        return [False, 'Colóquese frente a la cámara']
