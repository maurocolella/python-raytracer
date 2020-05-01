from PIL import Image
import numpy as np

w, h = 512, 512
data = np.zeros((h, w, 3), dtype=np.uint8)
for j in range(0,h) :
    for i in range(0,w) :
        r = i / w
        g = j / h
        b = 0.2
        data[i,j] = [int(255 * r), int(255 * g), int(255 * b)]
# data[0:512, 0:512] = [255, 0, 0] # red patch in upper left
img = Image.fromarray(data, 'RGB')
img.save('render.png')
img.show()
