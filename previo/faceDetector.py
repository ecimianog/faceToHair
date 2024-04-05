import tensorflow as tf
import numpy as np

# Load the image
imagen = tf.io.read_file('images\myimage_20231021_162552.png')
imagen = tf.image.decode_jpeg(imagen)

# Convert the image to grayscale
grayscale_image = tf.image.rgb_to_grayscale(imagen)

# Apply a Gaussian blur to the image
blurred_image = tf.image.blur(grayscale_image, (5, 5))

# Apply a Canny edge detector to the image
edged_image = tf.image.canny(blurred_image, 100, 200)

# Find the contours of the face in the image
contours = tf.image.find_contours(edged_image)

# Find the largest contour in the image
largest_contour = tf.reduce_max(contours, axis=0)

# Draw the largest contour on the image
imagen = tf.image.draw_bounding_boxes(imagen, [largest_contour])

# Detect the mouth, nose, ears, eyes, and forehead
mouth_detector = tf.keras.models.load_model('mouth_detector.h5')
nose_detector = tf.keras.models.load_model('nose_detector.h5')
ear_detector_left = tf.keras.models.load_model('ear_detector_left.h5')
ear_detector_right = tf.keras.models.load_model('ear_detector_right.h5')
eye_detector_left = tf.keras.models.load_model('eye_detector_left.h5')
eye_detector_right = tf.keras.models.load_model('eye_detector_right.h5')
forehead_detector = tf.keras.models.load_model('forehead_detector.h5')

# Predict the position and shape of the mouth
mouth_coordinates, mouth_shape = mouth_detector.predict(imagen)

# Predict the position and shape of the nose
nose_coordinates, nose_shape = nose_detector.predict(imagen)

# Predict the position and shape of the left ear
ear_coordinates_left, ear_shape_left = ear_detector_left.predict(imagen)

# Predict the position and shape of the right ear
ear_coordinates_right, ear_shape_right = ear_detector_right.predict(imagen)

# Predict the position and shape of the left eye
eye_coordinates_left, eye_shape_left = eye_detector_left.predict(imagen)

# Predict the position and shape of the right eye
eye_coordinates_right, eye_shape_right = eye_detector_right.predict(imagen)

# Predict the position and shape of the forehead
forehead_coordinates, forehead_shape = forehead_detector.predict(imagen)

# Draw the detected features on the image
imagen = tf.image.draw_bounding_boxes(imagen, [mouth_coordinates])
imagen = tf.image.draw_bounding_boxes(imagen, [nose_coordinates])
imagen = tf.image.draw_bounding_boxes(imagen, [ear_coordinates_left])
imagen = tf.image.draw_bounding_boxes(imagen, [ear_coordinates_right])
imagen = tf.image.draw_bounding_boxes(imagen, [eye_coordinates_left])
imagen = tf.image.draw_bounding_boxes(imagen, [eye_coordinates_right])
imagen = tf.image.draw_bounding_boxes(imagen, [forehead_coordinates])

# Display the image
tf.io.write_file('output.jpg', imagen)