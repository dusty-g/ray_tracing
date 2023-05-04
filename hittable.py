from math import sqrt
from typing import Optional, List
from vec3 import Point3, Vec3
from ray import Ray



class HitRecord:
    def __init__(self, point: Point3, normal: Vec3, t: float, front_face: bool):
        self.point = point
        self.normal = normal
        self.t = t
        self.front_face = front_face
    def set_face_normal(self, r: Ray, outward_normal: Vec3):
        self.front_face = r.direction.dot(outward_normal) < 0
        self.normal = outward_normal if self.front_face else -outward_normal
class Hittable:
    def hit(self, r: Ray, t_min: float, t_max: float) -> Optional[HitRecord]:
        raise NotImplementedError
    
class Torus(Hittable):
    def __init__(self, center: Point3, major_radius: float, minor_radius: float, max_steps: int = 100, epsilon: float = 1e-3, t_max: float = 1e3):
        self.center = center
        self.major_radius = major_radius
        self.minor_radius = minor_radius
        self.max_steps = max_steps
        self.epsilon = epsilon
        self.t_max = t_max
    
    def hit(self, r: Ray, t_min: float, t_max: float) -> Optional[HitRecord]:
        t = self.hit_torus(r)
        if t > 0:
            p = r.at(t)
            outward_normal = self.torus_normal(p)
            hit_record = HitRecord(point=p, normal=outward_normal, t=t, front_face=True)
            hit_record.set_face_normal(r, outward_normal)
            return hit_record
        return None
    
    def torus_distance_function(self, point: Point3) -> float:
        x, y, z = point.e[0] - self.center.e[0], point.e[1] - self.center.e[1], point.e[2] - self.center.e[2]
        temp = sqrt(x*x + y*y) - self.major_radius
        return sqrt(temp*temp + z*z) - self.minor_radius

    def hit_torus(self, ray: Ray) -> float:
        t=0.0
        for _ in range(self.max_steps):
            point = ray.at(t)
            d = self.torus_distance_function(point)
            if d < self.epsilon:
                return t
            t += d
            if t > self.t_max:
                break
        return -1.0
    
    def torus_normal(self, point: Point3, delta: float = 1e-5) -> Vec3:
        dx = Vec3(delta, 0, 0)
        dy = Vec3(0, delta, 0)
        dz = Vec3(0, 0, delta)
        
        nx = self.torus_distance_function(point + dx) - self.torus_distance_function(point - dx)
        ny = self.torus_distance_function(point + dy) - self.torus_distance_function(point - dy)
        nz = self.torus_distance_function(point + dz) - self.torus_distance_function(point - dz)

        return Vec3(nx, ny, nz).unit_vector()

class Sphere(Hittable):
    def __init__(self, center: Point3, radius: float):
        self.center = center
        self.radius = radius
    def hit(self, r: Ray, t_min: float, t_max: float) -> Optional[HitRecord]:
        oc = r.origin - self.center
        a = r.direction.length_squared()
        half_b = oc.dot(r.direction)
        c = oc.length_squared() - self.radius * self.radius

        discriminant = half_b * half_b - a * c
        if(discriminant < 0):
            return None
        sqrtd = sqrt(discriminant)

        # find nearest root in range
        root = (-half_b - sqrtd) / a
        if(root < t_min or t_max < root):
            root = (-half_b + sqrtd) / a
            if(root < t_min or t_max < root):
                return None
        t = root
        p = r.at(t)
        outward_normal = (p - self.center) / self.radius
        rec = HitRecord(point=p, normal=outward_normal, t=t, front_face = True)
        rec.set_face_normal(r, outward_normal)
        return rec

class HittableList(Hittable):
    def __init__(self, objects: Optional[List[Hittable]] = None):
        self.objects = objects if objects else []

    def clear(self):
        self.objects.clear()

    def add(self, obj: Hittable):
        self.objects.append(obj)

    def hit(self, r: Ray, t_min: float, t_max: float) -> Optional[HitRecord]:
        hit_anything = False
        closest_so_far = t_max
        closest_record = None
        for obj in self.objects:
            temp_record = obj.hit(r, t_min, closest_so_far)
            if temp_record:
                hit_anything = True
                closest_so_far = temp_record.t
                closest_record = temp_record
        return closest_record if hit_anything else None