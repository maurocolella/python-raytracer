import math
import random
from .vec3 import Vec3

class Utils(object):
    @staticmethod
    def random_in_hemisphere(normal: Vec3):
        in_unit_sphere = Utils.random_in_unit_sphere()
        if Vec3.dot(in_unit_sphere, normal) > 0.0: # In the same hemisphere as the normal
            return in_unit_sphere
        return -in_unit_sphere

    @staticmethod
    def random_unit_vector():
        a = random.uniform(0, 2*math.pi)
        z = random.uniform(-1, 1)
        r = math.sqrt(1 - z ** 2)
        return Vec3(r*math.cos(a), r*math.sin(a), z)

    @staticmethod
    def random_in_unit_sphere():
        while True:
            p = Vec3.random(-1, 1)
            if p.length_squared() < 1:
                return p

    @staticmethod
    def random_in_unit_disk():
        while True:
            p = Vec3(random.uniform(-1, 1), random.uniform(-1, 1), 0)
            if p.length_squared() < 1:
                return p
