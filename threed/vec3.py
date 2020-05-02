import math

class Vec3(object):
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    @staticmethod
    def dot(v1, v2):
        return v1.x * v2.x + v1.y * v2.y + v1.z * v2.z

    @staticmethod
    def cross(v1, v2):
        x = v1.y * v2.z - v1.z * v2.y
        y = v1.x * v2.x - v1.x * v2.z
        z = v1.z * v2.y - v1.y * v2.x
        return Vec3(x, y, z)

    @staticmethod
    def normalize(v):
        return v / v.norm()

    def norm(self):
        return math.sqrt(Vec3.dot(self, self))

    def length_squared(self):
        return self.x ** 2 + self.y ** 2 + self.z ** 2

    def clamp(self, x: float, min_value: float, max_value: float):
        return max(min(x, max_value), min_value)

    def asColor(self, samples_per_pixel: int):
        scale = 1 / samples_per_pixel
        r = scale * self.x
        g = scale * self.y
        b = scale * self.z
        return [int(256 * self.clamp(r, 0.0, 0.999)), int(256 * self.clamp(g, 0.0, 0.999)), int(256 * self.clamp(b, 0.0, 0.999))]

    def __truediv__(self, v):
        if isinstance(v, Vec3):
            return Vec3(self.x / v.x, self.y / v.y, self.z / v.z)
        else:
            return Vec3(self.x / v, self.y / v, self.z / v)

    def __mul__(self, v):
        if isinstance(v, Vec3):
            return Vec3(self.x * v.x, self.y * v.y, self.z * v.z)
        else:
            return Vec3(self.x * v, self.y * v, self.z * v)

    def __rmul__(self, v):
        return self.__mul__(v)

    def __add__(self, v):
        return Vec3(self.x + v.x, self.y + v.y, self.z + v.z)

    def __neg__(self):
        return Vec3(-self.x, -self.y, -self.z)

    def __sub__(self, v):
        return self + (-v)

    def __str__(self):
        return '[ %.4f, %.4f, %.4f ]' % (self.x, self.y, self.z)
