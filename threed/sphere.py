import math
from .vec3 import Vec3
from .ray import Ray
from .hittable import Hittable, HitRecord

class Sphere(Hittable):
    def __init__(self, center: Vec3, radius):
        self.center = center
        self.radius = radius

    def hit(self, r: Ray, t_min, t_max, rec: HitRecord):
        oc = r.origin() - self.center
        a = r.dir.length_squared()
        half_b = Vec3.dot(oc, r.dir)
        c = oc.length_squared() - self.radius ** 2
        discriminant = half_b ** 2 - a * c

        if (discriminant > 0) :
            root = math.sqrt(discriminant)
            temp = (-half_b - root)/a
            if (temp < t_max and temp > t_min) :
                rec.t = temp
                rec.p = r.at(rec.t)
                rec.normal = (rec.p - self.center) / self.radius
                return True
            temp = (-half_b + root) / a
            if (temp < t_max and temp > t_min) :
                rec.t = temp
                rec.p = r.at(rec.t)
                rec.normal = (rec.p - self.center) / self.radius
                return True
        return False
