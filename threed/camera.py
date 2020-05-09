import math
from .vec3 import Vec3
from .ray import Ray
from .utils import Utils

class Camera(object):
    def __init__(self,
                 look_from: Vec3,
                 look_at: Vec3,
                 vup: Vec3,
                 vfov: float,
                 aspect: float,
                 aperture: float,
                 focus_dist: float):
        self.origin = look_from
        self.lens_radius = aperture / 2

        theta = math.radians(vfov)
        half_height = math.tan(theta / 2)
        half_width = aspect * half_height
        self.w = Vec3.normalize(look_from - look_at)
        self.u = Vec3.normalize(Vec3.cross(vup, self.w))
        self.v = Vec3.cross(self.w, self.u)

        self.lower_left_corner = self.origin \
                                 - half_width * focus_dist * self.u \
                                 - half_height * focus_dist * self.v \
                                 - focus_dist * self.w
        self.horizontal = 2 * half_width * focus_dist * self.u
        self.vertical = 2 * half_height * focus_dist * self.v

    def get_ray(self, s: float, t: float):
        rd = self.lens_radius * Utils.random_in_unit_disk()
        offset = self.u * rd.x + self.v * rd.y

        return Ray(self.origin + offset,
                   self.lower_left_corner + s * self.horizontal + t * self.vertical - self.origin - offset)
