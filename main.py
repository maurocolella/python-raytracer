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

def ray_color(r: Ray, world: Hittable):
    rec = HitRecord()
    did_hit, rec = world.hit(r, 0, float("inf"), rec)
    if did_hit:
        return 0.5 * (rec.normal + Vec3(1, 1, 1))
    unit_direction = Vec3.normalize(r.dir)
    t = 0.5*(unit_direction.y + 1.0)
    return (1.0-t) * Vec3(1.0, 1.0, 1.0) + t * Vec3(0.5, 0.7, 1.0)

def main():
    window_width = 2400
    window_height = 1200

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
    world.add(Sphere(Vec3(0, 0, -1), 0.5))
    world.add(Sphere(Vec3(0, -100.5, -1), 100))

    cam = Camera()

    # pool = mp.Pool(mp.cpu_count())

    for x in range(0, image_width):
        for y in range(0, image_height):
            pixel = Vec3(0, 0, 0)
            for s in range(0,samples_per_pixel):
                u = (x + random.uniform(0, 0.999)) / image_width
                v = (y + random.uniform(0, 0.999)) / image_height
                r = cam.get_ray(u, v)
                sample = ray_color(r, world)
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
