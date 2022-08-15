import picamera
import picamera.array
import numpy
from PIL import Image
import hashlib
import time
from randomgen import ChaCha

with picamera.PiCamera() as camera:
    with picamera.array.PiRGBArray(camera) as output:
        camera.resolution = (2464, 2464)
        camera.capture(output, 'rgb')
        pixelTotal = numpy.sum(output.array)
        pixelTotal = int(str(pixelTotal)[1:])
        mixedEntropy = str(bin(pixelTotal)[2:]) + str(bin(time.time_ns())[2:])
        hashHex = hashlib.sha256(mixedEntropy.encode('ASCII')).hexdigest()
        hashInt = int(hashHex, 16)
        randomNum = numpy.random.Generator(ChaCha(seed = hashInt))
        randomValue = randomNum.standard_normal()
        print(randomValue)

