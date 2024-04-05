import tensorflow as tf
import numpy as np
from tensorflow.keras.utils import img_to_array as ia
import tensorflow_addons as tfa
import matplotlib.pyplot as plt


def FaceDetector(imagenp):
    # Carga la imagen
    imagenp = 'images\myimage_20231021_162552.png'
    
    # Carga la imagen PNG con TensorFlow
    image_path = 'images\myimage_20231021_162552.png'
    image = tf.io.read_file(image_path)
    image = tf.image.decode_png(image, channels=3)  # Decode as RGB
    # image = tf.image.decode_image(image)
    print(11111111111111111)
    # Convertir en escala de grises
    image_gray = tf.image.rgb_to_grayscale(image)
    blurred_image = tf.image.gaussian_filter2d (image, kernel_size=(3, 3), sigma=(1.0, 1.0))
    
    # Display the original and grayscale images
    plt.figure(figsize=(8, 4))
    plt.subplot(1, 2, 1)
    plt.imshow(image)
    plt.title('Original Image')
    plt.axis('off')

    plt.subplot(1, 2, 2)
    plt.imshow(tf.squeeze(blurred_image, axis=-1), cmap='gray')
    plt.title('Grayscale Image')
    plt.axis('off')

    plt.show()

    # Save the grayscale image
    output_path = 'grayscale_image.png'
    tf.io.write_file(output_path, tf.image.encode_png(tf.cast(image_gray, tf.uint8)))

    imagen = tf.io.read_file(imagenp)
    imagen2 = tf.io.read_file(imagenp)
    # imagen = tf.image.decode_jpeg(imagen)
    imagen = tf.image.decode_png(imagen)
    #imagen2 = tf.keras.utils.load_img(imagenp)
    #image = tf.keras.utils.load_img(imagen2)
    input_arr = ia(imagen)
    print('FACEDETECTORRRRRRRRRRRRR1')
    input_arr = np.array([input_arr])  # Convert single image to a batch.
    print('FACEDETECTORRRRRRRRRRRRR2')
    print(input_arr)
    #imagen2 = tf.image.img_to_array(imagen)
    input_arr = input_arr/255
    print('FACEDETECTORRRRRRRRRRRRR3')
    grayscale_image = tf.image.rgb_to_grayscale(input_arr)
    print('FACEDETECTORRRRRRRRRRRRR4')
    # Convert the image to grayscale
    grayscale_image = tf.image.rgb_to_grayscale(imagen)
    print('RRRRRRRRRRRRFACEDETECTOR')
    # return grayscale_image

    # Apply a Gaussian blur to the image
    blurred_image = tf.image.blur(grayscale_image, (5, 5))
    return blurred_image

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