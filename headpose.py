import cv2
import numpy as np
import mediapipe as mp
from mediapipe.framework.formats import landmark_pb2

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils
drawing_specA = mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=1, circle_radius=1)
drawing_specB = mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=3, circle_radius=1)
drawing_spec = mp_drawing.DrawingSpec(color=(0, 0, 0), thickness=1, circle_radius=0)

EYEBROW_LANDMARKS = [70, 63, 105, 66, 107, 336, 296, 334, 293, 300]
LIPS_LANDMARKS = [61, 146, 146, 91, 91, 181, 181, 84, 84, 17, 17, 314, 314, 405, 405, 321,
321, 375, 375, 291, 61, 185, 185, 40, 40, 39, 39, 37, 37, 0, 0, 267, 267,
269, 269, 270, 270, 409, 409, 291, 78, 95, 95, 88, 88, 178, 178, 87, 87, 14,
14, 317, 317, 402, 402, 318, 318, 324, 324, 308, 78, 191, 191, 80, 80, 81,
81, 82, 82, 13, 13, 312, 312, 311, 311, 310, 310, 415, 415, 308]
LEFT_EYE_LANDMARKS = [33, 7, 7, 163, 163, 144, 144, 145, 145, 153, 153, 154, 154, 155, 155, 133,
33, 246, 246, 161, 161, 160, 160, 159, 159, 158, 158, 157, 157, 173, 173,
133]
LEFT_EYEBROW_LANDMARKS = [46, 53, 53, 52, 52, 65, 65, 55, 70, 63, 63, 105, 105, 66, 66, 107]
LEFT_IRIS_LANDMARKS = [474, 475, 475, 476, 476, 477, 477, 474]
RIGHT_EYE_LANDMARKS = [263, 249, 249, 390, 390, 373, 373, 374, 374, 380, 380, 381, 381, 382, 382,
362, 263, 466, 466, 388, 388, 387, 387, 386, 386, 385, 385, 384, 384, 398,
398, 362]
RIGHT_EYEBROW_LANDMARKS = [276, 283, 283, 282, 282, 295, 295, 285, 300, 293, 293, 334, 334, 296, 296,
336]
RIGHT_IRIS_LANDMARKS = [469, 470, 470, 471, 471, 472, 472, 469]
FACE_OVAL_LANDMARKS = [10, 338, 338, 297, 297, 332, 332, 284, 284, 251, 251, 389, 389, 356, 356,
454, 454, 323, 323, 361, 361, 288, 288, 397, 397, 365, 365, 379, 379, 378,
378, 400, 400, 377, 377, 152, 152, 148, 148, 176, 176, 149, 149, 150, 150,
136, 136, 172, 172, 58, 58, 132, 132, 93, 93, 234, 234, 127, 127, 162, 162,
21, 21, 54, 54, 103, 103, 67, 67, 109, 109, 10]

def took():
    print('took')

def lookFront(image):
    #print("Head Pose")
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    face = face_mesh.process(image)
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    
    img_h, img_w, img_c = image.shape
    face_3d = []
    face_2d = []
    
    if face.multi_face_landmarks:
        for face_landmarks in face.multi_face_landmarks:
            for id in EYEBROW_LANDMARKS:
                lm=face_landmarks.landmark[id]
                #writer.writerow({'frame_num':frame_num,'landmark_x':lm.x,'landmark_y':lm.y})

            for id in LIPS_LANDMARKS:
                lm=face_landmarks.landmark[id]
                #writer.writerow({'frame_num':frame_num,'landmark_x':lm.x,'landmark_y':lm.y})

                # Draw only eyebrow landmarks on video output
                # Draw only eyebrow landmarks on video output
            eyebrow_landmarksA = landmark_pb2.NormalizedLandmarkList()
            eyebrow_landmarksA.landmark.extend([face_landmarks.landmark[id] for id in LEFT_EYEBROW_LANDMARKS])
            eyebrow_landmarksA.landmark.extend([face_landmarks.landmark[id] for id in RIGHT_EYEBROW_LANDMARKS])
            mp_drawing.draw_landmarks(
                    image=image,
                    landmark_list=eyebrow_landmarksA,
                    connections=[],
                    landmark_drawing_spec=drawing_specA,
                    connection_drawing_spec=drawing_specA
            )
            
            eyebrow_landmarksB = landmark_pb2.NormalizedLandmarkList()
            eyebrow_landmarksB.landmark.extend([face_landmarks.landmark[id] for id in LIPS_LANDMARKS])
            mp_drawing.draw_landmarks(
                    image=image,
                    landmark_list=eyebrow_landmarksB,
                    connections=[],
                    landmark_drawing_spec=drawing_specB,
                    connection_drawing_spec=drawing_specB
            )
            
            eyebrow_landmarks = landmark_pb2.NormalizedLandmarkList()
            for idx, lm in enumerate(face_landmarks.landmark):
                if idx == 33 or idx == 263 or idx == 1 or idx == 61 or idx == 291 or idx == 199:
                    if idx == 1:
                        nose_2d = (lm.x * img_w, lm.y * img_h)
                        nose_3d = (lm.x * img_w, lm.y * img_h, lm.z * 3000)
                        
                    x, y = int(lm.x * img_w), int(lm.y * img_h)
                    
                    face_2d.append([x, y])
                    
                    face_3d.append([x, y, lm.z])
                
                if idx not in LEFT_EYEBROW_LANDMARKS:
                    if idx not in RIGHT_EYEBROW_LANDMARKS:
                        if idx not in LIPS_LANDMARKS:    
                            eyebrow_landmarks.landmark.extend([face_landmarks.landmark[idx]])
                
                    
            face_2d = np.array(face_2d, dtype=np.float64)
            face_3d = np.array(face_3d, dtype=np.float64)
            
            focal_length = 1 * img_w
            
            cam_matrix = np.array([ [focal_length, 0, img_h / 2],
                                   [0, focal_length, img_h / 2],
                                   [0, 0, 1]])
            
            dist_matrix = np.zeros((4, 1), dtype=np.float64)
            
            success, rot_vec, trans_vec = cv2.solvePnP(face_3d, face_2d, cam_matrix, dist_matrix)
            
            rmat, jac = cv2.Rodrigues(rot_vec)
            
            angles, mtxR, mtxQ, Qx, Qy, Qz = cv2.RQDecomp3x3(rmat)
            
            x = angles[0] * 360
            y = angles[1] * 360
            z = angles[2] * 360
            
            text = ' - Mire de frente'
            if y < -10:
                text = 'Izquierda' + text
            elif y > 10:
                text = 'Derecha' + text
            elif x < -10:
                text = 'Abajo' + text
            elif x > 10:
                text = 'Arriba' + text
            else:
                text = ''
                
            #print(text, x, y)
            
            nose_3d_projection, jacobian = cv2.projectPoints(nose_3d, rot_vec, trans_vec, cam_matrix, dist_matrix)
            
            p1 = (int(nose_2d[0]), int(nose_2d[1]))
            p2 = (int(nose_2d[0] + y * 10), int(nose_2d[1] - x * 10))
            
            #cv2.line(image, p1, p2, (255, 0, 0), 3)
            #print(face_landmarks)
            cv2.putText(image, text, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)
            cv2.putText(image, 'x: ' + str(np.round(x, 2)), (500, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.putText(image, 'y: ' + str(np.round(y, 2)), (500, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.putText(image, 'z: ' + str(np.round(z, 2)), (500, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            mp_drawing.draw_landmarks(
                image=image,
                landmark_list=eyebrow_landmarks,
                connections=[],
                landmark_drawing_spec=drawing_spec,
                connection_drawing_spec=drawing_spec
            )
            cv2.imshow('image', image)
    
            # Se sale con Esc
            key = cv2.waitKey(1)
            if key == 27:
                break
            return True