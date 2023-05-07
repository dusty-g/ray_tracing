from math import sqrt
from typing import Optional, Tuple, TYPE_CHECKING
from hittable import HitRecord
if TYPE_CHECKING:
    from hittable import HitRecord

from ray import Ray
from vec3 import Color, Vec3

def reflect(v: Vec3, n: Vec3) -> Vec3:
    return v - 2*v.dot(n)*n

class Material:
    def scatter(self, ray_in: Ray, hit_record: 'HitRecord')->Optional[Tuple[Ray, Color]]:
        raise NotImplementedError
    
class Lambertian(Material):
    def __init__(self, albedo: Color):
        self.albedo = albedo

    def scatter(self, ray_in: Ray, hit_record: 'HitRecord') ->Tuple[Ray, Color]:
        scattered_direction: Vec3 = hit_record.normal + Vec3.random_unit_vector()
        
        if scattered_direction.near_zero():
            scattered_direction = hit_record.normal

        scattered_ray: Ray = Ray(hit_record.point, scattered_direction)
        attenuation: Color = self.albedo
        return (scattered_ray, attenuation)
    
class Metal(Material):
    def __init__(self, albedo: Color, fuzz: float):
        self.albedo = albedo
        self.fuzz = min(fuzz, 1)
    
    def scatter(self, ray_in: Ray, hit_record: 'HitRecord') -> Optional[Tuple[Ray, Color]]:
        reflected: Vec3 = reflect(ray_in.direction.unit_vector(), hit_record.normal)
        scattered_ray: Ray = Ray(hit_record.point, reflected + self.fuzz*Vec3.random_in_unit_sphere())
        return ((scattered_ray, self.albedo) if (scattered_ray.direction.dot(hit_record.normal) > 0) else None) 
    
class Dialectric(Material):
    def __init__(self, index_of_refraction:float):
        self.index_of_refraction = index_of_refraction
        self.attenuation = Color(1,1,1)
    def scatter(self, ray_in: Ray, hit_record: HitRecord) -> Tuple[Ray, Color] | None:
        refraction_ratio = 1.0 / self.index_of_refraction if hit_record.front_face else self.index_of_refraction

        unit_direction: Vec3 = ray_in.direction.unit_vector()
        cos_theta = min(-unit_direction.dot(hit_record.normal), 1)
        sin_theta = sqrt(1.0 - cos_theta * cos_theta)

        cannot_refract: bool = refraction_ratio * sin_theta > 1.0

        direction: Vec3

        if cannot_refract:
            direction = reflect(unit_direction, hit_record.normal)
        else:
            direction = unit_direction.refract(hit_record.normal, refraction_ratio)



        scattered = Ray(hit_record.point, direction)

        return (scattered, self.attenuation)

