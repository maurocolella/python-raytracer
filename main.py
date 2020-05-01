from PIL import Image
import numpy as np
from threed.vec3 import Vec3
from threed.ray import Ray

def ray_color(r: Ray):
    unit_direction = -Vec3.normalize(r.dir)
    t = 0.5*(unit_direction.y + 1.0)
    return (1.0-t) * Vec3(1.0, 1.0, 1.0) + t * Vec3(0.5, 0.7, 1.0)

def main():
    image_width, image_height = 512, 512
    data = np.zeros((image_height, image_width, 3), dtype=np.uint8)

    lower_left_corner = Vec3(-2.0, -1.0, -1.0)
    horizontal = Vec3(0.0, 4.0, 0.0)
    vertical = Vec3(0.0, 0.0, 2.0)
    origin = Vec3(0.0, 0.0, 0.0)

    for x in range(0,image_width) :
        for y in range(0,image_height) :
            u = x / image_width
            v = y / image_height
            r = Ray(origin, lower_left_corner + u*horizontal + v*vertical)
            rgb = ray_color(r)

            data[x,y] = rgb.asColor()
    img = Image.fromarray(data, 'RGB')
    img.save('render.png')
    img.show()

main()
