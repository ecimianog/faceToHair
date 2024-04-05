import tensorflow as tf
import tensorflow.keras.layers as layers
import openface

def build_eye_detector_left(input_shape=(100, 100, 3)):
  """
  Crea un modelo de detección de ojos izquierdo.

  Args:
    input_shape: La forma de la entrada del modelo.

  Returns:
    Un modelo de detección de ojos izquierdo.
  """

  face_detector = openface.TorchFaceDetector('models/dlib/shape_predictor_68_face_landmarks.dat')

  model = tf.keras.models.Sequential([
    layers.Conv2D(16, (3, 3), activation='relu', input_shape=input_shape),
    layers.Conv2D(32, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dense(1, activation='sigmoid')
  ])

  return model


def build_eye_detector_right(input_shape=(100, 100, 3)):
  """
  Crea un modelo de detección de ojos derecho.

  Args:
    input_shape: La forma de la entrada del modelo.

  Returns:
    Un modelo de detección de ojos derecho.
  """

  face_detector = openface.TorchFaceDetector('models/dlib/shape_predictor_68_face_landmarks.dat')

  model = tf.keras.models.Sequential([
    layers.Conv2D(16, (3, 3), activation='relu', input_shape=input_shape),
    layers.Conv2D(32, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dense(1, activation='sigmoid')
  ])

  return model


def build_ear_detector_left(input_shape=(100, 100, 3)):
  """
  Crea un modelo de detección de oído izquierdo.

  Args:
    input_shape: La forma de la entrada del modelo.

  Returns:
    Un modelo de detección de oído izquierdo.
  """

  face_detector = openface.TorchFaceDetector('models/dlib/shape_predictor_68_face_landmarks.dat')

  model = tf.keras.models.Sequential([
    layers.Conv2D(16, (3, 3), activation='relu', input_shape=input_shape),
    layers.Conv2D(32, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dense(1, activation='sigmoid')
  ])

  return model


def build_ear_detector_right(input_shape=(100, 100, 3)):
  """
  Crea un modelo de detección de oído derecho.

  Args:
    input_shape: La forma de la entrada del modelo.

  Returns:
    Un modelo de detección de oído derecho.
  """

  face_detector = openface.TorchFaceDetector('models/dlib/shape_predictor_68_face_landmarks.dat')

  model = tf.keras.models.Sequential([
    layers.Conv2D(16, (3, 3), activation='relu', input_shape=input_shape),
    layers.Conv2D(32, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dense(1, activation='sigmoid')
  ])

  return model

def build_mouth_detector(input_shape=(100, 100, 3)):
  """
  Crea un modelo de detección de boca.

  Args:
    input_shape: La forma de la entrada del modelo.

  Returns:
    Un modelo de detección de boca.
  """

  face_detector = openface.TorchFaceDetector('models/dlib/shape_predictor_68_face_landmarks.dat')

  model = tf.keras.models.Sequential([
    layers.Conv2D(16, (3, 3), activation='relu', input_shape=input_shape),
    layers.Conv2D(32, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dense(1, activation='sigmoid')
  ])

  return model


def build_nose_detector(input_shape=(100, 100, 3)):
  """
  Crea un modelo de detección de nariz.

  Args:
    input_shape: La forma de la entrada del modelo.

  Returns:
    Un modelo de detección de nariz.
  """

  face_detector = openface.TorchFaceDetector('models/dlib/shape_predictor_68_face_landmarks.dat')

  model = tf.keras.models.Sequential([
    layers.Conv2D(16, (3, 3), activation='relu', input_shape=input_shape),
    layers.Conv2D(32, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dense(1, activation='sigmoid')
  ])

  return model


def build_forehead_detector(input_shape=(100, 100, 3)):
  """
  Crea un modelo de detección de frente.

  Args:
    input_shape: La forma de la entrada del modelo.

  Returns:
    Un modelo de detección de frente.
  """

  face_detector = openface.TorchFaceDetector('models/dlib/shape_predictor_68_face_landmarks.dat')

  model = tf.keras.models.Sequential([
    layers.Conv2D(16, (3, 3), activation='relu', input_shape=input_shape),
    layers.Conv2D(32, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dense(1, activation='sigmoid')
  ])

  return model


def main():
  # Carga el conjunto de datos
  dataset = openface.load_dataset('eyes_right')
  #dataset = openface.get_dataset('eyes_left')
  #dataset = openface.get_dataset('ears_right')
  #dataset = openface.get_dataset('ears_left')
  #dataset = openface.get_dataset('mouths')
  #dataset = openface.get_dataset('noses')
  #dataset = openface.get_dataset('foreheads')
  (x_train, y_train), (x_test, y_test) = dataset.load_data()

  # Convierte las etiquetas a formato one-hot
  y_train = tf.keras.utils.to_categorical(y_train)
  y_test = tf.keras.utils.to_categorical(y_test)

  # Crea los modelos
  mouth_detector = build_mouth_detector()
  nose_detector = build_nose_detector()
  forehead_detector = build_forehead_detector()
  eye_detector_left = build_eye_detector_left()
  eye_detector_right = build_eye_detector_right()
  ear_detector_left = build_ear_detector_left()
  ear_detector_right = build_ear_detector_right()

  # Entrena los modelos
  eye_detector_left.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
  eye_detector_left.fit(x_train, y_train, epochs=10)

  eye_detector_right.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
  eye_detector_right.fit(x_train, y_train, epochs=10)

  ear_detector_left.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
  ear_detector_left.fit(x_train, y_train, epochs=10)

  ear_detector_right.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
  ear_detector_right.fit(x_train, y_train, epochs=10)

  mouth_detector.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
  mouth_detector.fit(x_train, y_train, epochs=10)

  nose_detector.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
  nose_detector.fit(x_train, y_train, epochs=10)

  forehead_detector.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
  forehead_detector.fit(x_train, y_train, epochs=10)

  # Evalúa los modelos
  eye_score_left = eye_detector_left.evaluate(x_test, y_test, verbose=0)
  eye_score_right = eye_detector_right.evaluate(x_test, y_test, verbose=0)
  ear_score_left = ear_detector_left.evaluate(x_test, y_test, verbose=0)
  ear_score_right = ear_detector_right.evaluate(x_test, y_test, verbose=0)
  mouth_score_right = mouth_detector.evaluate(x_test, y_test, verbose=0)
  nose_score_right = nose_detector.evaluate(x_test, y_test, verbose=0)
  forehead_score_right = forehead_detector.evaluate(x_test, y_test, verbose=0)

  # Imprime las puntuaciones
  print('Puntuación de ojo izquierdo:', eye_score_left[1])
  print('Puntuación de ojo derecho:', eye_score_right[1])
  print('Puntuación de oído izquierdo:', ear_score_left[1])
  print('Puntuación de oído derecho:', ear_score_right[1])
  print('Puntuación de boca:', mouth_score_right[1])
  print('Puntuación de nariz:', nose_score_right[1])
  print('Puntuación de frente:', forehead_score_right[1])

  # Guarda los modelos
  eye_detector_left.save('eye_detector_left.h5')
  eye_detector_right.save('eye_detector_right.h5')
  ear_detector_left.save('ear_detector_left.h5')
  ear_detector_right.save('ear_detector_right.h5')
  mouth_detector.save('mouth_detector.h5')
  nose_detector.save('nose_detector.h5')
  forehead_detector.save('forehead_detector.h5')


if __name__ == '__main__':
  main()

