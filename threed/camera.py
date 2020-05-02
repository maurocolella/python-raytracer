from .vec3 import Vec3
from .ray import Ray

class Camera(object):
    def __init__(self,
                 lower_left_corner=Vec3(-2, -1, -1),
                 horizontal=Vec3(4, 0, 0),
                 vertical=Vec3(0, 2, 0),
                 origin=Vec3(0, 0, 0)):
        self.lower_left_corner = lower_left_corner
        self.horizontal = horizontal
        self.vertical = vertical
        self.origin = origin

    def get_ray(self, u: float, v: float):
        return Ray(self.origin,
                   self.lower_left_corner + u*self.horizontal + v*self.vertical - self.origin)
