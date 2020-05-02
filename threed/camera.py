import math
from .vec3 import Vec3
from .ray import Ray

class Camera(object):
    def __init__(self,
                 look_from: Vec3,
                 look_at: Vec3,
                 vup: Vec3,
                 vfov: float,
                 aspect: float):
        theta = math.radians(vfov)
        half_height = math.tan(theta/2)
        half_width = aspect * half_height
        w = Vec3.normalize(look_from - look_at)
        u = Vec3.normalize(Vec3.cross(vup, w))
        v = Vec3.cross(w, u)

        self.origin = look_from
        self.lower_left_corner = self.origin - half_width*u - half_height*v - w
        self.horizontal = 2*half_width*u
        self.vertical = 2*half_height*v

    def get_ray(self, u: float, v: float):
        return Ray(self.origin,
                   self.lower_left_corner + u*self.horizontal + v*self.vertical - self.origin)
