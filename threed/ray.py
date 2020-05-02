from .vec3 import Vec3

class Ray(object):
    def __init__(self, origin: Vec3, direction: Vec3):
        self.orig = origin
        self.dir = direction

    def at(self, t: float):
        return self.orig + t*self.dir
