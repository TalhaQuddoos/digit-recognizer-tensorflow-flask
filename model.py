import tflite_runtime.interpreter as tflite
from PIL import Image
import numpy as np
import os, io


interpreter = tflite.Interpreter(model_path="model.tflite")
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

def model_predict(img):
    input_data = img.astype(np.float32)
    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()
    output_data = interpreter.get_tensor(output_details[0]['index'])
    return output_data.argmax(), output_data[0][output_data.argmax()]

def preprocess_image(image, img_type="file"):
    if img_type == "file":
        return (image.reshape(1, 28, 28, 1) / 255.).astype(np.float32)
    elif img_type == "df_row":
        return (image.to_numpy().reshape(1, 28, 28, 1) / 255.).astype(np.float32)

def predict(image_data):
    # Import image
    image = Image.open(io.BytesIO(image_data))

    # Convert the RGB image to grayscale image
    image = image.convert("L")

    # Resize the image to 28x28
    image = image.resize((28, 28))

    # Convert the image into numpy array
    image = np.array(image)

    # Reshape the image for the model
    image = image.reshape(1, 28, 28, 1) 

    # Normalize the pixel values in image
    image = image / 255.

    # Set the datatype of image as float32
    image = image.astype(np.float32)

    # Make prediction on the image
    prediction, confidence = model_predict(image)

    return prediction, confidence
    
    


