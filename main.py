import random
import pygame
import numpy as np
# import multiprocessing as mp
from PIL import Image
from threed.vec3 import Vec3
from threed.ray import Ray
from threed.sphere import Sphere
from threed.hittable import Hittable, HitRecord
from threed.hittable_list import HittableList
from threed.camera import Camera
from threed.renderer import Renderer

from threed.lambert_material import Lambertian
from threed.metal_material import Metal

pygame.init()

def main():
    window_width = 800
    window_height = 400

    image_width = 800
    image_height = 400

    data = np.empty((image_width, image_height, 3), dtype=np.uint8)

    window_size = (window_width, window_height)
    screen = pygame.display.set_mode(window_size)
    pygame.display.set_caption("Raytracer")

    render_buffer = pygame.Surface((data.shape[0], data.shape[1]))
    screen_buffer = pygame.Surface(window_size)

    live_render = True

    samples_per_pixel = 100

    world = HittableList()
    world.add(Sphere(Vec3(-0.5, 0, -1.5), 0.5, Lambertian(Vec3(0.7, 0.3, 0.3))))
    world.add(Sphere(Vec3(0, -100.5, -1), 100, Lambertian(Vec3(0.8, 0.8, 0.0))))
    world.add(Sphere(Vec3(0.5, 0, -1.5), 0.5, Metal(Vec3(0.8, 0.8, 0.8), 0.2)))

    cam = Camera()

    renderer = Renderer()

    max_depth = 10

    for x in range(0, image_width):
        for y in range(0, image_height):
            pixel = Vec3(0, 0, 0)
            for s in range(0, samples_per_pixel):
                u = (x + random.uniform(0, 0.999)) / image_width
                v = (y + random.uniform(0, 0.999)) / image_height
                r = cam.get_ray(u, v)
                pixel += renderer.ray_color(r, world, max_depth)

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
