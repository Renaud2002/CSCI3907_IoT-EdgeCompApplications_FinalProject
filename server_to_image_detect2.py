import socket
from keras.models import load_model  # TensorFlow is required for Keras to work
import cv2  # Install opencv-python
import numpy as np

# to open the image localy
from PIL import Image
import csv
import datetime
import os
import os.path

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('161.253.124.12', 1025))

while True:

    server.listen()

    client_socket, client_address = server.accept()


    file = open('server_image.jpg', "wb")
    image_chunk  = client_socket.recv(2048)

    while image_chunk:
        file.write(image_chunk)
        image_chunk  = client_socket.recv(2048)





    # Disable scientific notation for clarity
    np.set_printoptions(suppress=True)

    # Load the model
    model = load_model("converted_keras/keras_Model.h5", compile=False)

    # Load the labels
    class_names = open("converted_keras/labels.txt", "r").readlines()

    # # CAMERA can be 0 or 1 based on default camera of your computer
    # camera = cv2.VideoCapture(0)

    # im = Image.open(r"IMG_3290.jpg")
    img = cv2.imread("server_image.jpg", cv2.IMREAD_COLOR)

    # while True:
    #     # Grab the webcamera's image.
    #     ret, image = camera.read()

        # Resize the raw image into (224-height,224-width) pixels
    image = cv2.resize(img, (224,224), interpolation=cv2.INTER_AREA)

    # # Show the image in a window
    # cv2.imshow("Webcam Image", image)

    # Make the image a numpy array and reshape it to the models input shape.
    image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)

    # Normalize the image array
    image = (image / 127.5) - 1

    # Predicts the model
    prediction = model.predict(image)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]

    # Print prediction and confidence score
    print("Class:", class_name[2:], end="")
    print("Confidence Score:", str(np.round(confidence_score * 100))[:-2], "%")


    # Putting the data into a csv file 
    e = datetime.datetime.now()
    today = datetime.date.today()

    # File name will be base on day so a new file for every day of class
    filename = "attendance_data_" + str(today) + ".csv"

    # Checking if the file already exist if not create new one else just append to it
    if not os.path.isfile(filename):
        file = open(filename, 'w', newline='')
        writer = csv.writer(file)
        field = ['name', 'date: '+ str(today)]
        writer.writerow(field)  
    else:
        file = open(filename, 'a', newline='')
        writer = csv.writer(file)

    # Adding the student name to the attendance list for the day
    writer.writerow([class_name[2:].strip(), e])

file.close()
client_socket.close()