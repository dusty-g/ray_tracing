import math

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
    def __sub____(self, vec3):
        return Vec3(self.e[0] - vec3.e[0], self.e[1] - vec3.e[1], self.e[2] - vec3.e[2])
    # overload imul
    def __imul__(self, t): 
        self.e[0] *= t
        self.e[1] *= t
        self.e[2] *= t
        return self
    def __mul__(self, vec3):
        return Vec3(self.e[0]*vec3.e[0], self.e[1]*vec3.e[1], self.e[2]*vec3.e[2])
    def __itruediv__(self, t):
        self *= 1/t
        return self
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
    def write_color(self):
        return f"{int(255.999 * self.e[0])} {int(255.999 * self.e[1])} {int(255.999 * self.e[2])}"
Point3 = Vec3
Color = Vec3 