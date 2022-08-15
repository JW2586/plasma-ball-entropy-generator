import picamera
import picamera.array
import numpy
from PIL import Image
import hashlib
import time
import sys
from randomgen import ChaCha
from io import BytesIO

with picamera.PiCamera() as camera:
    with picamera.array.PiRGBArray(camera) as output:
        camera.resolution = (2464, 2464)
        camera.capture(output, 'rgb')
        pil_im = Image.fromarray(output.array, mode="RGB")
        hexStream = BytesIO()
        pil_im.save(hexStream, format="jpeg")
        hex_data = hexStream.getvalue()
        mixedEntropy = str(bin(int.from_bytes(hex_data,byteorder=sys.byteorder))[2:]) + str(bin(time.time_ns())[2:])
        hashHex = hashlib.sha256(str(mixedEntropy).encode('ASCII')).hexdigest()
        hashInt = int(hashHex, 16)
        randomNum = numpy.random.Generator(ChaCha(seed=hashInt))
        randomValue=randomNum.standard_normal()
        print(randomValue)
