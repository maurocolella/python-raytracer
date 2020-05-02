from abc import ABC, abstractmethod
from .vec3 import Vec3
from .ray import Ray

class Material(ABC):
    @abstractmethod
    def scatter(self,
                r_in: Ray,
                rec,
                attenuation: Vec3,
                scattered: Ray):
        pass
