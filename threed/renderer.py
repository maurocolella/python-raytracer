import math
import random
# import multiprocessing as mp
from .vec3 import Vec3
from .ray import Ray
from .hittable import Hittable, HitRecord
from .hittable_list import HittableList
from .camera import Camera

class Renderer(object):
    def __init__(self,
                 cam: Camera,
                 world: HittableList,
                 image_width: int,
                 image_height: int,
                 max_depth: int,
                 aa_samples_per_pixel: int):
        self.cam = cam
        self.world = world
        self.image_width = image_width
        self.image_height = image_height
        self.max_depth = max_depth
        self.aa_samples_per_pixel = aa_samples_per_pixel

    def render(self, x: int, y: int):
        samples = []
        for s in range(0, self.aa_samples_per_pixel):
            u = (x + random.uniform(0, 0.999)) / self.image_width
            v = (y + random.uniform(0, 0.999)) / self.image_height
            r = self.cam.get_ray(u, v)
            samples.append(self.ray_color(r, self.world, self.max_depth))
        return samples

    def random_in_hemisphere(self, normal: Vec3):
        in_unit_sphere = self.random_in_unit_sphere()
        if Vec3.dot(in_unit_sphere, normal) > 0.0: # In the same hemisphere as the normal
            return in_unit_sphere
        return -in_unit_sphere

    def random_unit_vector(self):
        a = random.uniform(0, 2*math.pi)
        z = random.uniform(-1, 1)
        r = math.sqrt(1 - z ** 2)
        return Vec3(r*math.cos(a), r*math.sin(a), z)

    def random_in_unit_sphere(self):
        while True:
            p = Vec3.random(-1, 1)
            if p.length_squared() < 1:
                return p

    def ray_color(self, r: Ray, world: Hittable, depth: int):
        rec = HitRecord()
        if depth <= 0:
            return Vec3(0, 0, 0)

        did_hit, rec = world.hit(r, 0.001, float("inf"), rec)
        if did_hit:
            scattered = Ray(Vec3(0, 0, 0), Vec3(1, 1, 1))
            attenuation = Vec3(0, 0, 0)
            scatter, scattered, attenuation = rec.material.scatter(r, rec, attenuation, scattered)

            if scatter:
                return attenuation * self.ray_color(scattered, world, depth-1)
            return Vec3(0, 0, 0)
        unit_direction = Vec3.normalize(r.dir)
        t = 0.5*(unit_direction.y + 1.0)
        return (1.0-t) * Vec3(1.0, 1.0, 1.0) + t * Vec3(0.5, 0.7, 1.0)
