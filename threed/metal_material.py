from .material import Material
from .vec3 import Vec3
from .ray import Ray

def reflect(v: Vec3, n: Vec3):
    return v - 2 * Vec3.dot(v, n) * n

class Metal(Material):
    def __init__(self, albedo: Vec3):
        self.albedo = albedo

    def scatter(self, r_in: Ray, rec, attenuation: Vec3, scattered: Ray):
        reflected = reflect(Vec3.normalize(r_in.dir), rec.normal)
        scattered = Ray(rec.p, reflected)
        attenuation = self.albedo
        return (Vec3.dot(scattered.dir, rec.normal) > 0, scattered, attenuation)
