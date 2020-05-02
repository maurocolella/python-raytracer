import math
import random
import numpy as np
# import multiprocessing as mp
import pygame
from PIL import Image
from threed.vec3 import Vec3
from threed.ray import Ray
from threed.sphere import Sphere
from threed.hittable import Hittable, HitRecord
from threed.hittable_list import HittableList
from threed.camera import Camera

pygame.init()

def random_in_hemisphere(normal: Vec3):
    in_unit_sphere = random_in_unit_sphere()
    if Vec3.dot(in_unit_sphere, normal) > 0.0: # In the same hemisphere as the normal
        return in_unit_sphere
    return -in_unit_sphere

def random_unit_vector():
    a = random.uniform(0, 2*math.pi)
    z = random.uniform(-1, 1)
    r = math.sqrt(1 - z ** 2)
    return Vec3(r*math.cos(a), r*math.sin(a), z)

def random_in_unit_sphere():
    while True:
        p = Vec3.random(-1, 1)
        if p.length_squared() < 1:
            return p

def ray_color(r: Ray, world: Hittable, depth: int):
    rec = HitRecord()
    if depth <= 0:
        return Vec3(0, 0, 0)

    did_hit, rec = world.hit(r, 0.001, float("inf"), rec)
    if did_hit:
        target = rec.p + rec.normal + random_unit_vector()
        return 0.5 * ray_color(Ray(rec.p, target - rec.p), world, depth-1)
        # return 0.5 * (rec.normal + Vec3(1, 1, 1))
    unit_direction = Vec3.normalize(r.dir)
    t = 0.5*(unit_direction.y + 1.0)
    return (1.0-t) * Vec3(1.0, 1.0, 1.0) + t * Vec3(0.5, 0.7, 1.0)

def main():
    window_width = 2400
    window_height = 1200

    image_width = 1000
    image_height = 500

    data = np.empty((image_width, image_height, 3), dtype=np.uint8)

    window_size = (window_width, window_height)
    screen = pygame.display.set_mode(window_size)
    pygame.display.set_caption("Raytracer")

    render_buffer = pygame.Surface((data.shape[0], data.shape[1]))
    screen_buffer = pygame.Surface(window_size)

    live_render = True

    samples_per_pixel = 100

    world = HittableList()
    world.add(Sphere(Vec3(0, 0, -1), 0.5))
    world.add(Sphere(Vec3(0, -100.5, -1), 100))

    cam = Camera()

    max_depth = 10

    for x in range(0, image_width):
        for y in range(0, image_height):
            pixel = Vec3(0, 0, 0)
            for s in range(0,samples_per_pixel):
                u = (x + random.uniform(0, 0.999)) / image_width
                v = (y + random.uniform(0, 0.999)) / image_height
                r = cam.get_ray(u, v)
                sample = ray_color(r, world, max_depth)
                pixel += sample

            data[x, y] = pixel.asColor(samples_per_pixel)
        if live_render:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
            pygame.surfarray.blit_array(render_buffer, np.fliplr(data))

            # transform the surface (scale)
            screen.fill((0, 0, 0))
            screen_buffer = pygame.transform.scale(render_buffer, window_size)
            # blit onto the screen
            screen.blit(screen_buffer, (0, 0))
            pygame.display.update()

    img = Image.fromarray(np.rot90(data), 'RGB')
    img.save('render.png')

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

main()
