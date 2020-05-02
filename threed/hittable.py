from abc import ABC, abstractmethod
from typing import NamedTuple
from .vec3 import Vec3
from .ray import Ray

class HitRecord(NamedTuple):
    p: Vec3
    normal: Vec3

class Hittable(ABC):
    @abstractmethod
    def hit(self, r: Ray, t_min: float, t_max: float, rec: HitRecord):
        pass
