from PIL import Image
import numpy as np
from threed import vec3

w, h = 512, 512
data = np.zeros((h, w, 3), dtype=np.uint8)
for j in range(0,h) :
    for i in range(0,w) :
        rgb = vec3.Vec(i / w, j / h, 0.2)
        data[i,j] = rgb.asColor()
img = Image.fromarray(data, 'RGB')
img.save('render.png')
img.show()
