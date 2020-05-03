from .material import Material
from .vec3 import Vec3
from .ray import Ray
from .utils import Utils

class Lambertian(Material):
    def __init__(self, albedo: Vec3):
        self.albedo = albedo

    def scatter(self, r_in: Ray, rec, attenuation: Vec3, scattered: Ray):
        scatter_direction = rec.normal + Utils.random_unit_vector()
        scattered = Ray(rec.p, scatter_direction)
        attenuation = self.albedo
        return (True, scattered, attenuation)
