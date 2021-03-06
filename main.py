import tensorflow.keras
from PIL import Image, ImageOps
import numpy as np
import glob
import cv2
import os

def func(datadir):
    images = [cv2.imread(file) for file in glob.glob(os.path.join(datadir, '*.jpg'))]
    print(len(images))

    # Disable scientific notation for clarity
    np.set_printoptions(suppress=True)

    # Load the model
    model = tensorflow.keras.models.load_model('keras_model.h5')

    # Create the array of the right shape to feed into the keras model
    # The 'length' or number of images you can put into the array is
    # determined by the first position in the shape tuple, in this case 1.
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

    # Replace this with the path to your image
    for img in images:
        image = Image.fromarray(img)

        # resize the image to a 224x224 with the same strategy as in TM2:
        # resizing the image to be at least 224x224 and then cropping from the center
        size = (224, 224)
        image = ImageOps.fit(image, size, Image.ANTIALIAS)

        # turn the image into a numpy array
        image_array = np.asarray(image)

        # display the resized image
        # image.show()

        # Normalize the image
        normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1

        # Load the image into the array
        data[0] = normalized_image_array

        # run the inference
        prediction = model.predict(data)

        res = np.argmax(prediction[0])

        file1 = open('labels.txt', 'r', encoding='utf-8')
        lines = file1.readlines()
        k = []
        k.append(lines[res].rsplit(' ')[1])
        for i in k:
            print(i ,end='')
func('data')