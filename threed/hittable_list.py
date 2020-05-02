from .ray import Ray
from .hittable import Hittable, HitRecord

class HittableList(Hittable):
    def __init__(self):
        self.objects = []

    def add(self, obj):
        self.objects.append(obj)

    def clear(self):
        self.objects.clear()

    def hit(self, r: Ray, t_min: float, t_max: float, rec: HitRecord):
        temp_rec = HitRecord()
        hit_anything = False
        closest_so_far = t_max

        for obj in self.objects:
            did_hit, temp_rec = obj.hit(r, t_min, closest_so_far, temp_rec)
            if did_hit:
                hit_anything = True
                closest_so_far = temp_rec.t
                rec = temp_rec
        return (hit_anything, rec)
