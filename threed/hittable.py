from abc import ABC, abstractmethod
from .vec3 import Vec3
from .ray import Ray
from .material import Material
from .lambert_material import Lambertian

class HitRecord(object):
    def __init__(self,
                 p=Vec3(0, 0, 0),
                 normal=Vec3(1, 1, 1),
                 t=1,
                 front_face=False,
                 material=Lambertian(Vec3(0, 0, 0))):
        self.p = p
        self.normal = normal
        self.t = t
        self.front_face = front_face
        self.material = material

    def set_face_normal(self, r: Ray, outward_normal: Vec3):
        front_face = Vec3.dot(r.dir, outward_normal) < 0
        self.normal = outward_normal if front_face else -outward_normal

class Hittable(ABC):
    @abstractmethod
    def hit(self, r: Ray, t_min: float, t_max: float, rec: HitRecord):
        pass
