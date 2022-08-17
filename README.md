# 🔮 Plasma ball entropy generator
*This is a proof of concept inspired by Cloudflare's implementation of Lavarand*

<img src="https://github.com/JW2586/Plasma-ball-entropy-generator/blob/e45cb5215a0c4632ddd4b8947a264bf6d1db87db/Images/Hardware%20setup.jpg" alt="alt text" width="400" height="whatever">

# Using a chaotic Plasma globe as an entropy source for random number generation
Extracts binary data from an image captured by a Raspberry Pi camera. Mixes the entropy with the number of nanoseconds since epoch. Seeds the entropy pool into a ChaCha20 CSPRNG.
```python
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
```
Alternative method adds up the RGB values for each pixel, creating an overall total. Mixes the value with the number of nanoseconds since epoch. Seeds the entropy pool into a ChaCha20 CSPRNG.
```python
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
```

## References
- [Lavarand](https://blog.cloudflare.com/lavarand-in-production-the-nitty-gritty-technical-details/)
- [Patent US5732138A](https://patents.google.com/patent/US5732138)
