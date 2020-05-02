from .material import Material
from .vec3 import Vec3
from .ray import Ray

def random_in_unit_sphere():
    while True:
        p = Vec3.random(-1, 1)
        if p.length_squared() < 1:
            return p

def reflect(v: Vec3, n: Vec3):
    return v - 2 * Vec3.dot(v, n) * n

class Metal(Material):
    def __init__(self, albedo: Vec3, fuzz: float):
        self.albedo = albedo
        self.fuzz = fuzz if fuzz < 1 else 1

    def scatter(self, r_in: Ray, rec, attenuation: Vec3, scattered: Ray):
        reflected = reflect(Vec3.normalize(r_in.dir), rec.normal)
        scattered = Ray(rec.p, reflected + self.fuzz * random_in_unit_sphere())
        attenuation = self.albedo
        return (Vec3.dot(scattered.dir, rec.normal) > 0, scattered, attenuation)
