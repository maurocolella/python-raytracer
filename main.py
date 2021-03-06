import random
import numpy as np
from PIL import Image
import multiprocessing as mp

from threed.vec3 import Vec3
from threed.sphere import Sphere
from threed.hittable_list import HittableList
from threed.camera import Camera
from threed.renderer import Renderer
from threed.timing import Timer

from threed.lambert_material import Lambertian
from threed.metal_material import Metal
from threed.dielectric_material import Glass

def random_scene():
    world = HittableList()

    world.add(Sphere(
        Vec3(0, -1000, 0), 1000, Lambertian(Vec3(0.5, 0.5, 0.5))
    ))

    i = 1
    for a in range(-11, 11):
        for b in range(-11, 11):
            choose_mat = random.uniform(0, 0.999)
            center = Vec3(a + 0.9 * random.uniform(0, 0.999), 0.2, b + random.uniform(0, 0.999))
            if (center - Vec3(4, 0.2, 0)).norm() > 0.9:
                if choose_mat < 0.8:
                    # diffuse
                    albedo = Vec3.random() * Vec3.random()
                    world.add(
                        Sphere(center, 0.2, Lambertian(albedo))
                    )
                elif choose_mat < 0.95:
                    # metal
                    albedo = Vec3.random(.5, 1)
                    fuzz = random.uniform(0, .5)
                    world.add(
                        Sphere(center, 0.2, Metal(albedo, fuzz))
                    )
                else:
                    # glass
                    world.add(Sphere(center, 0.2, Glass(1.5)))

    world.add(Sphere(Vec3(0, 1, 0), 1.0, Glass(1.5)))
    world.add(Sphere(Vec3(-4, 1, 0), 1.0, Lambertian(Vec3(0.4, 0.2, 0.1))))
    world.add(Sphere(Vec3(4, 1, 0), 1.0, Metal(Vec3(0.7, 0.6, 0.5), 0.0)))

    return world

def main():
    timer = Timer()
    aspect_ratio = 16.0 / 9.0
    aspect_bias = 1.2 # workaround for subtle discrepancies between numeric operations in C++ vs Python3+
    window_width = 900
    window_height = (int) (window_width / aspect_ratio)
    num_cpus = max(1, int(mp.cpu_count() - 2))

    window_size = (window_width, window_height)
    screen = pygame.display.set_mode(window_size)
    pygame.display.set_caption("Raytracer")

    image_width = 120 # 7680
    image_height = (int) (image_width / aspect_ratio) # 4320

    data = np.empty((image_width, image_height, 3), dtype=np.uint8)

    render_buffer = pygame.Surface((data.shape[0], data.shape[1]))
    screen_buffer = pygame.Surface(window_size)

    aa_samples_per_pixel = 100

    world = random_scene()
    # world.add(Sphere(Vec3(0, -100.5, -1), 100, Lambertian(Vec3(0.8, 0.7, 0.0))))
    # world.add(Sphere(Vec3(-1.0, 0, -1), 0.45, Glass(1.5)))
    # world.add(Sphere(Vec3(0, 0, -1), 0.5, Lambertian(Vec3(0.3, 0.3, 0.5))))
    # world.add(Sphere(Vec3(1.0, 0, -1), 0.5, Metal(Vec3(0.8, 0.8, 0.8), 0.1)))

    look_from = Vec3(13, 2, 3)
    look_at = Vec3(0, 0, 0)
    vup = Vec3(0, 1, 0)
    dist_to_focus = 10 # (look_from - look_at).norm()
    aperture = 0.1
    cam = Camera(look_from, look_at, vup, 20, aspect_ratio * aspect_bias, aperture, dist_to_focus)

    max_depth = 10
    live_render = True
    renderer = Renderer(cam, world, image_width, image_height, max_depth, aa_samples_per_pixel)

    pool = mp.Pool(num_cpus)

    for x in range(0, image_width):
        for y in range(0, image_height):
            # TODO: spawn sub-processes as a function of and y
            samples = pool.starmap_async(renderer.render,
                                         [(x, y) for s in range(0, aa_samples_per_pixel)])
            pixel = sum(samples.get(), Vec3(0, 0, 0))
            data[x, y] = pixel.asColor(aa_samples_per_pixel)
            # TODO: decouple render/display
            if live_render:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return
        if live_render:
            pygame.surfarray.blit_array(render_buffer, np.fliplr(data))
            # transform the surface (scale)
            screen.fill((0, 0, 0))
            screen_buffer = pygame.transform.scale(render_buffer, window_size)
            # blit onto the screen
            screen.blit(screen_buffer, (0, 0))
            pygame.display.update()

    img = Image.fromarray(np.rot90(data), 'RGB')
    img.save('render.png')
    timer.log("Render Complete", True)
    pool.close()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

if __name__ == '__main__':
    import pygame
    pygame.init()
    main()
