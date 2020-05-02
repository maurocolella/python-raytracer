import math
import numpy as np
# import multiprocessing as mp
import pygame
from PIL import Image
from threed.vec3 import Vec3
from threed.ray import Ray

pygame.init()

def hit_sphere(center: Vec3, radius: float, r: Ray):
    oc = r.orig - center
    a = r.dir.length_squared()
    half_b = Vec3.dot(oc, r.dir)
    c = oc.length_squared() - radius ** 2
    discriminant = half_b ** 2 - a * c
    if discriminant < 0:
        return -1.0
    else:
        return (-half_b - math.sqrt(discriminant)) / a

def ray_color(r: Ray):
    t = hit_sphere(Vec3(0, 0, -1), 0.5, r)
    if t > 0.0:
        N = Vec3.normalize(r.at(t) - Vec3(0, 0, -1))
        return 0.5 * Vec3(N.x+1, N.y+1, N.z+1)
    unit_direction = Vec3.normalize(r.dir)
    t = 0.5*(unit_direction.y + 1.0)
    return (1.0-t) * Vec3(1.0, 1.0, 1.0) + t * Vec3(0.5, 0.7, 1.0)

def main():
    window_width = 2000
    window_height = 1000

    image_width = 200
    image_height = 100

    window_size = (window_width, window_height)
    data = np.empty((image_width, image_height, 3), dtype=np.uint8)
    size = (image_width, image_height)

    screen = pygame.display.set_mode(window_size)
    pygame.display.set_caption("Raytracer")
    surf = pygame.Surface((data.shape[0], data.shape[1]))
    render_buffer = pygame.Surface(window_size)
    live_render = True

    lower_left_corner = Vec3(-2.0, -1.0, -1.0)
    horizontal = Vec3(4.0, 0.0, 0.0)
    vertical = Vec3(0.0, 2.0, 0.0)
    origin = Vec3(0.0, 0.0, 0.0)
    # pool = mp.Pool(mp.cpu_count())

    for x in range(0, image_width):
        for y in range(0, image_height):
            u = x / image_width
            v = y / image_height
            r = Ray(origin, lower_left_corner + u*horizontal + v*vertical)
            rgb = ray_color(r)

            data[x, y] = rgb.asColor()
        if live_render:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
            pygame.surfarray.blit_array(surf, np.fliplr(data))
            screen.fill((0, 0, 0))
            # blit the transformed surface onto the screen
            render_buffer = pygame.transform.scale(surf, window_size)
            screen.blit(render_buffer, (0, 0))
            pygame.display.update()

    img = Image.fromarray(np.rot90(data), 'RGB')
    img.save('render.png')

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

main()
