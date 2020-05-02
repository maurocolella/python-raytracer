import math
import random
from .material import Material
from .vec3 import Vec3
from .ray import Ray

def random_unit_vector():
    a = random.uniform(0, 2*math.pi)
    z = random.uniform(-1, 1)
    r = math.sqrt(1 - z ** 2)
    return Vec3(r*math.cos(a), r*math.sin(a), z)

class Lambertian(Material):
    def __init__(self, albedo: Vec3):
        self.albedo = albedo

    def scatter(self, r_in: Ray, rec, attenuation: Vec3, scattered: Ray):
        scatter_direction = rec.normal + random_unit_vector()
        scattered = Ray(rec.p, scatter_direction)
        attenuation = self.albedo
        return (True, scattered, attenuation)
