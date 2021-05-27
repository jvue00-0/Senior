import io
import time
import picamera
from picamera import PiCamera
from PIL import Image, ImageOps
import numpy as np
from picamera.array import PiRGBArray


camera = PiCamera()

for i in range(250):
    camera.resolution = (244, 244)
    size = (224, 224)
    camera.capture('/home/pi/Pictures/New/image{0:04d}.png'.format(i))
   