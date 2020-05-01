from PIL import Image
import numpy as np
from threed.vec3 import Vec3
from threed.ray import Ray

def hit_sphere(center: Vec3, radius, r: Ray):
    oc = r.orig - center
    a = Vec3.dot(r.dir, r.dir)
    b = 2.0 * Vec3.dot(oc, r.dir)
    c = Vec3.dot(oc, oc) - radius * radius
    discriminant = b * b - 4 * a * c
    return (discriminant > 0)

def ray_color(r: Ray):
    if hit_sphere(Vec3(0,0,-1), 0.5, r):
        return Vec3(1, 0, 0)
    unit_direction = Vec3.normalize(r.dir)
    t = 0.5*(unit_direction.y + 1.0)
    return (1.0-t) * Vec3(1.0, 1.0, 1.0) + t * Vec3(0.5, 0.7, 1.0)

def main():
    image_width = 512
    image_height = 256
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
    img = Image.fromarray(data, 'RGB')
    img.save('render.png')
    img.show()

main()
