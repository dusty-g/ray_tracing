import math
import random

def clamp(x, minimum, maximum):
    return max(minimum, min(maximum, x))

class Vec3:
    def __init__(self, e0=0.0, e1=0.0, e2=0.0):
        self.e = [e0, e1, e2]

    # x y z separated by a space
    def __str__(self):
        return f"{self.e[0]} {self.e[1]} {self.e[2]}"
    
    def __repr__(self) -> str:
        return f"Vec3(x={self.e[0]}, y={self.e[1]}, z={self.e[2]})"
    
    
    # return vector with negative x,y,z values
    def __neg__(self):
        return Vec3(-self.e[0], -self.e[1], -self.e[2])
    
    def __getitem__(self, index):
        return self.e[index]
    
    # setitem
    def __setitem__(self, index, value):
        self.e[index] = value

    # overload iadd
    def __iadd__(self, vec3):
        self.e[0] += vec3.e[0]
        self.e[1] += vec3.e[1]
        self.e[2] += vec3.e[2]
        return self
    def __add__(self, vec3):
        return Vec3(self.e[0] + vec3.e[0], self.e[1] + vec3.e[1], self.e[2] + vec3.e[2])
    def __sub__(self, vec3):
        return Vec3(self.e[0] - vec3.e[0], self.e[1] - vec3.e[1], self.e[2] - vec3.e[2])
    # overload imul
    def __imul__(self, t): 
        self.e[0] *= t
        self.e[1] *= t
        self.e[2] *= t
        return self
    def __mul__(self, other):
        if isinstance(other, Vec3):
            return Vec3(self.e[0]*other.e[0], self.e[1]*other.e[1], self.e[2]*other.e[2])
        elif isinstance(other, (int, float)):
            return Vec3(self.e[0]* other, self.e[1] * other, self.e[2] * other)
        else:
            raise TypeError("Operand must be either Vec3 or int/float.")
    def __rmul__(self, other):
        return self * other
    def __itruediv__(self, t):
        self *= 1/t
        return self
    def __truediv__(self, t):
        return Vec3(self.e[0] / t, self.e[1] / t, self.e[2] / t)
    def length(self):
        return math.sqrt(self.length_squared())
    def length_squared(self):
        return self.e[0] * self.e[0] + self.e[1] * self.e[1] + self.e[2] * self.e[2]
    def dot(self, vec3):
        return self.e[0] * vec3.e[0]+ self.e[1] * vec3.e[1] + self.e[2] * vec3.e[2]
    def cross(self, vec3):
        return Vec3(self.e[1] * vec3.e[2] - self.e[2] * vec3.e[1], self.e[2] * vec3.e[0] - self.e[0] * vec3.e[2], self.e[0] * vec3.e[1] - self.e[1] * vec3.e[0])
    def unit_vector(self):
        return self / self.length()
    def write_color(self, samples_per_pixel = 1):
        r, g, b = self.e

        scale = 1.0 / samples_per_pixel
        # gamma = 2
        r = math.sqrt(scale * r)
        g = math.sqrt(scale * g)
        b = math.sqrt(scale * b)

        return f"{int(256 * clamp(r,0.0,0.999))} {int(256 * clamp(g, 0.0, 0.999))} {int(256 * clamp(b, 0.0, 0.999))}"
    # static create random point in unit cube
    
    @staticmethod
    def random(min: float = 0, max: float = 1):
        return Vec3(random.uniform(min, max), random.uniform(min, max), random.uniform(min, max))

    @staticmethod
    def random_in_unit_sphere():
        while True:
            candidate_point: Vec3 = Vec3.random(-1, 1)
            if(candidate_point.length_squared() >= 1):
                continue
            return candidate_point
    @staticmethod
    def random_in_unit_disk():
         while True:
            candidate_point: Vec3 = Vec3(random.uniform(-1, 1), random.uniform(-1, 1), 0)
            if(candidate_point.length_squared() >= 1):
                continue
            return candidate_point
    

    @staticmethod
    def random_unit_vector():
        vector: Vec3 = Vec3.random_in_unit_sphere()
        return vector.unit_vector()
    
    def near_zero(self):
        s = 1e-8
        return all(math.isclose(_, 0, abs_tol=s) for _ in self.e)
    
    def refract(self, n, etai_over_etat: float):
        cos_theta = min(-self.dot(n), 1.0)
        r_out_perp: Vec3 = etai_over_etat * (self + cos_theta*n)
        r_out_parallel = -math.sqrt(abs(1.0 - r_out_perp.length_squared())) * n
        return r_out_perp + r_out_parallel

Point3 = Vec3
Color = Vec3 