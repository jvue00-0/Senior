import tensorflow.keras
from PIL import Image, ImageOps
import numpy as np
from time import sleep
from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import os
import webbrowser

model = tensorflow.keras.models.load_model('Final_Model.h5', compile = False)        
camera = PiCamera()
camera.resolution = (244, 244)
rawCapture = PiRGBArray(camera, size=(1280, 720))

def analyze():
    camera.capture('/home/pi/Desktop/image.jpg')
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

# Replace this with the path to your image
    image = Image.open(r'/home/pi/Desktop/image.jpg')

#resize the image to a 224x224 with the same strategy as in TM2:
#resizing the image to be at least 224x224 and then cropping from the center
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.ANTIALIAS)

#turn the image into a numpy array
    image_array = np.asarray(image)

# Normalize the image
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1

# Load the image into the array
    data[0] = normalized_image_array

# run the inference
    prediction = model.predict(data)

    f = prediction[0]
    result = tensorflow.math.argmax(prediction, axis=1, output_type=tensorflow.int32)
    c = tensorflow.keras.backend.eval(result)
    p = c[0]
    k = f[p]
    
    w = round((k*100),2)
    label_array = ['W 15M Beam', 'G 9M Beam', 'G9 Axle', 'B10 Axle', 'G 7M Beam', 'G 5M Beam', 'LG 11M Beam', 'W 90', 'W 45', 'W Double Angle', 'R 90', 'B Tee', 'G 90', 'G 45', 'LG 45', 'B12 Axle', 'B8 Axle', 'B6 Axle', 'B4 Axle', 'G7 Axle', 'G5 Axle', 'G 4M Axle End', 'Beam 90 Snaps', 'Triangel', 'Beam Snap', 'Double Bush', 'Lever 1x4', 'Steering Arm', 'Axle Ent', 'Angle 0', 'Cross 2x2', 'Cross 90', 'Cross 3x2', 'Double Cross', 'Angle 180', 'Angle 90', '3 Cross Axle', 'Cross Block 3M', 'Cross Block 2x1', 'R V90', '2M Damper', '1x2 Cross Hole', 'G 3M', 'Y 3M', 'R 3M', 'B 3M', 'Bion Eye', 'Y Axis Axle', 'Y 3M Con Peg', 'Tube', 'Snap Crosshole', 'LG 3M', 'Half Bush', 'G Con Peg', 'Cross Axle Knob', 'Bush', 'Black Con Peg', 'B Peg Axle', '8M End', '3M Con Peg', '2M Axle Groove', '5x11 Frame', '5x7 Frame', 'Turntable', 'Tyre', 'Belt Wheel', '16T Gear', '24T Gear', 'Worm Gear', '40T Gear', 'Conical 12', 'Double Concial 12', 'Angular Wheel', 'Double Concical 36', 'Double Concical 20', 'Gear Wheel Z24', 'B 13 Beam']   
    print(label_array[p], "with", str(w) + "% confidence.")
    
    report(label_array, label_array[p])
    

def report(label_array, label):         # Report function
        
    for i in range(0,77): 
        if label == label_array[i]:
            index = i
            num_array[i] = num_array[i] + 1
            
            
    saveFile = open('Report.txt', 'w')
    saveFile.write('Parts Report\n')
    
    for j in range(0,77):
        saveFile.write('\n')
        saveFile.write(label_array[j])
        saveFile.write(': ')
        saveFile.write(str(num_array[j]) + "/")
        saveFile.write(str(amount_array[j]) + "\n")
        
        if num_array[j] < amount_array[j]:
            missing = amount_array[j] - num_array[j]
            saveFile.write("There are " + str(missing) + " missing.")
        
        if num_array[j] > amount_array[j]:
            extra = num_array[j] - amount_array[j]
            saveFile.write("There are " + str(extra) + " extra.")
            
        if num_array[j] == amount_array[j]:
            saveFile.write("There are none missing or extra.")
            
        saveFile.write('\n')
        saveFile.close


num_array = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,] 
amount_array = [6, 6, 2, 2, 4, 4, 4, 6, 6, 4, 6, 4, 2, 4, 4, 2, 2, 4, 4, 5, 6, 2, 4, 4, 6, 4, 2, 2, 6, 4, 4, 8, 6, 8, 4, 2, 14, 8, 4, 2, 4, 4, 4, 4, 4, 2, 4, 8, 6, 4, 22, 4, 10, 10, 2, 10, 60, 20, 2, 30, 10, 1, 3, 2, 4, 4, 4, 4, 2, 2, 2, 2, 4, 2, 2, 2, 6]


while True: 
    username = input("Enter username:")
    print("Username is: " + username)  
    if username == ("a"):
        analyze()
        
    if username == ("q"):
        break
    
webbrowser.open("Report.txt")

