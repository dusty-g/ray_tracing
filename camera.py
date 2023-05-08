from ray import Ray
from vec3 import Point3, Vec3
import rtweekend
import math

class Camera:
    def __init__(self, lookfrom:Point3, lookat: Point3, vup: Vec3, aperture:float, focus_dist: float, aspect_ratio = 16.0 / 9.0, vfov = 90):
        self.vfov = vfov
        self.theta = rtweekend.degrees_to_radians(vfov)
        h = math.tan(self.theta / 2)

        self.aspect_ratio = aspect_ratio
        self.viewport_height = 2.0 * h
        self.viewport_width = aspect_ratio * self.viewport_height
        self.focal_length = 1
        self.aperture = aperture
        self.focus_dist = focus_dist


        w = lookfrom - lookat
        w = w.unit_vector()

        u = vup.cross(w)
        self.u = u.unit_vector()

        self.v = w.cross(u)
        
        self.origin = lookfrom
        self.horizontal = self.focus_dist * self.viewport_width * self.u
        self.vertical = self.focus_dist * self.viewport_height * self.v
        self.lower_left_corner = self.origin - self.horizontal/2 - self.vertical/2 - self.focus_dist * w
        self.lens_radius = self.aperture / 2

    def get_ray(self, s, t):
        rd: Vec3 = self.lens_radius * Vec3.random_in_unit_disk()
        offset: Vec3 = self.u * rd.e[0]  + self.v * rd.e[1]
        return Ray(self.origin + offset, self.lower_left_corner + s * self.horizontal + t * self.vertical - self.origin - offset)
        