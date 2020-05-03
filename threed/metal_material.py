from .material import Material
from .vec3 import Vec3
from .ray import Ray
from .utils import Utils

class Metal(Material):
    def __init__(self, albedo: Vec3, fuzz: float):
        self.albedo = albedo
        self.fuzz = fuzz if fuzz < 1 else 1

    def __reflect(self, v: Vec3, n: Vec3):
        return v - 2 * Vec3.dot(v, n) * n

    def scatter(self, r_in: Ray, rec, attenuation: Vec3, scattered: Ray):
        reflected = self.__reflect(Vec3.normalize(r_in.dir), rec.normal)
        scattered = Ray(rec.p, reflected + self.fuzz * Utils.random_in_unit_sphere())
        attenuation = self.albedo
        return (Vec3.dot(scattered.dir, rec.normal) > 0, scattered, attenuation)
