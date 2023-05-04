from camera import Camera
from vec3 import Color, Point3, Vec3
from ray import Ray
from tqdm import tqdm
from math import sqrt
from hittable import Sphere, HittableList, Torus
from rtweekend import infinity, pi, degrees_to_radians
import random


def ray_color(ray: Ray, world: HittableList):
    hit_record = world.hit(r, 0.001, infinity)
    if hit_record:
        return 0.5 * (hit_record.normal + Color(1,1,1))
    unit_direction = ray.direction.unit_vector()
    t = 0.5*(unit_direction[1] + 1.0)
    return (1.0 - t)*Color(1.0, 1.0, 1.0) + t*Color(0.5,0.7,1)



# world
world = HittableList()
world.add(Sphere(Point3(0,0,-1), 0.5))
world.add(Sphere(Point3(0,-100.5,-1), 100))

# image
aspect_ratio = 16.0 / 9.0
image_width = 400
image_height = int(image_width / aspect_ratio)
samples_per_pixel = 100

# camera
camera = Camera()

# render
print(f"P3\n{image_width} {image_height}\n255")
for j in tqdm(range(image_height-1, -1, -1)):
    for i in range(image_width):
        pixel_color = Color(0,0,0)
        for sample in range(samples_per_pixel):
            
            u = (i + random.random()) / (image_width - 1)
            v = (j + random.random()) / (image_height - 1)
            r = camera.get_ray(u, v)
            pixel_color += ray_color(r, world)
        
        print(pixel_color.write_color(samples_per_pixel))
