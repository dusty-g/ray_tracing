from ray import Ray
from vec3 import Point3, Vec3
import rtweekend
import math

class Camera:
    def __init__(self, lookfrom:Point3, lookat: Point3, vup: Vec3, aspect_ratio = 16.0 / 9.0, vfov = 90):
        self.vfov = vfov
        self.theta = rtweekend.degrees_to_radians(vfov)
        h = math.tan(self.theta / 2)

        self.aspect_ratio = aspect_ratio
        self.viewport_height = 2.0 * h
        self.viewport_width = aspect_ratio * self.viewport_height
        self.focal_length = 1


        w = lookfrom - lookat
        w = w.unit_vector()

        u = vup.cross(w)
        u = u.unit_vector()

        v = w.cross(u)
        
        self.origin = lookfrom
        self.horizontal = self.viewport_width * u
        self.vertical = self.viewport_height * v
        self.lower_left_corner = self.origin - self.horizontal/2 - self.vertical/2 - w

    def get_ray(self, s, t):
        return Ray(self.origin, self.lower_left_corner + s*self.horizontal + t*self.vertical - self.origin)