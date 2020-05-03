import math
import random
from .material import Material
from .vec3 import Vec3
from .ray import Ray

class Glass(Material):
    def __init__(self, ri: float):
        self.ref_idx = ri

    def __refract(self, uv: Vec3, n: Vec3, etai_over_etat: Vec3):
        nuv = Vec3.normalize(uv)
        dt = Vec3.dot(nuv, n)
        discriminant = 1 - etai_over_etat ** 2 *(1-dt ** 2)
        if discriminant > 0:
            return etai_over_etat * (nuv-n * dt) - n*math.sqrt(discriminant)
        return None

        # cos_theta = Vec3.dot(-uv, n)
        # r_out_parallel = etai_over_etat * (uv + cos_theta * n)
        # r_out_perp = -math.sqrt(1.0 - r_out_parallel.length_squared()) * n
        # return r_out_parallel + r_out_perp

    def __reflect(self, v: Vec3, n: Vec3):
        return v - 2 * Vec3.dot(v, n) * n

    def __schlick(self, cosine: float, ref_idx: float):
        r0 = (1-ref_idx) / (1+ref_idx)
        r0 = r0 ** 2
        return r0 + (1-r0) * ((1 - cosine) ** 5)

    def scatter(self, r_in: Ray, rec, attenuation: Vec3, scattered: Ray):
        reflected = self.__reflect(r_in.dir, rec.normal)
        if Vec3.dot(r_in.dir, rec.normal) > 0:
            outward_normal = -rec.normal
            ni_over_nt = self.ref_idx
            cosine = self.ref_idx * Vec3.dot(r_in.dir, rec.normal) / r_in.dir.norm()
        else:
            outward_normal = rec.normal
            ni_over_nt = 1/self.ref_idx
            cosine = Vec3.dot(-r_in.dir, rec.normal) / r_in.dir.norm()
        refracted = self.__refract(r_in.dir, outward_normal, ni_over_nt)
        reflect_probe = self.__schlick(cosine, self.ref_idx) if refracted else 1
        if random.uniform(0, 0.999) < reflect_probe:
            scattered = Ray(rec.p, reflected)
        else:
            scattered = Ray(rec.p, refracted)
        return (True, scattered, Vec3(1, 1, 1))

        # attenuation = Vec3(1.0, 1.0, 1.0)
        # etai_over_etat = 1.0 / self.ref_idx if rec.front_face else self.ref_idx

        # unit_direction = Vec3.normalize(r_in.dir)
        # cos_theta = min(Vec3.dot(-unit_direction, rec.normal), 1.0)
        # sin_theta = math.sqrt(1.0 - cos_theta ** 2)
        # if etai_over_etat * sin_theta > 1.0:
        #    reflected = self.__reflect(unit_direction, rec.normal)
        #    scattered = Ray(rec.p, reflected)
        #    return (True, scattered, attenuation)

        # reflect_prob = self.__schlick(cos_theta, etai_over_etat)
        # if random.uniform(0, 0.999) < reflect_prob:
        #    reflected = self.__reflect(unit_direction, rec.normal)
        #    scattered = Ray(rec.p, reflected)
        #    return (True, scattered, attenuation)

        # refracted = self.__refract(unit_direction, rec.normal, etai_over_etat)
        # scattered = Ray(rec.p, refracted)
        # return (True, scattered, attenuation)
