from PIL import Image
import numpy as np
import math
from threed.vec3 import Vec3
from threed.ray import Ray

def hit_sphere(center: Vec3, radius, r: Ray):
    oc = r.orig - center
    a = r.dir.length_squared()
    half_b = Vec3.dot(oc, r.dir)
    c = oc.length_squared() - radius ** 2
    discriminant = half_b ** 2 - a * c
    if (discriminant < 0):
        return -1.0
    else:
        return (-half_b - math.sqrt(discriminant)) / a

def ray_color(r: Ray):
    t = hit_sphere(Vec3(0,0,-1), 0.5, r)
    if (t > 0.0):
        N = Vec3.normalize(r.at(t) - Vec3(0,0,-1))
        return 0.5 * Vec3(N.x+1, N.y+1, N.z+1)
    unit_direction = Vec3.normalize(r.dir)
    t = 0.5*(unit_direction.y + 1.0)
    return (1.0-t) * Vec3(1.0, 1.0, 1.0) + t * Vec3(0.5, 0.7, 1.0)

def main():
    image_width = 400
    image_height = 200
    data = np.zeros((image_height, image_width, 3), dtype=np.uint8)

    lower_left_corner = Vec3(-2.0, -1.0, -1.0)
    horizontal = Vec3(4.0, 0.0, 0.0)
    vertical = Vec3(0.0, 2.0, 0.0)
    origin = Vec3(0.0, 0.0, 0.0)

    for x in range(0,image_width) :
        for y in range(0,image_height) :
            u = x / image_width
            v = y / image_height
            r = Ray(origin, lower_left_corner + u*horizontal + v*vertical)
            rgb = ray_color(r)

            data[y,x] = rgb.asColor()
    img = Image.fromarray(np.flipud(data), 'RGB')
    img.save('render.png')
    img.show()

main()
