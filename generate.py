from vec3 import Color, Point3, Vec3
from ray import Ray
from tqdm import tqdm
from math import sqrt
from hittable import Sphere, HittableList, Torus
from rtweekend import infinity, pi, degrees_to_radians



def ray_color(ray: Ray, world: HittableList):
    hit_record = world.hit(r, 0, infinity)
    if hit_record:
        return 0.5 * (hit_record.normal + Color(1,1,1))
    unit_direction = ray.direction.unit_vector()
    t = 0.5*(unit_direction[1] + 1.0)
    return (1.0 - t)*Color(1.0, 1.0, 1.0) + t*Color(0.5,0.7,1)

def hit_sphere(center: Point3, radius, r: Ray):
    oc = r.origin - center
    a = r.direction.length_squared()
    half_b = oc.dot(r.direction)
    c = oc.length_squared() - radius * radius
    discriminant = half_b * half_b - a * c
    if(discriminant < 0):
        return -1.0
    else:
        return (-half_b - sqrt(discriminant))/ a

# world
world = HittableList()
world.add(Sphere(Point3(0,0,-1), 0.5))
world.add(Sphere(Point3(0,-100.5,-1), 100))

# image
aspect_ratio = 16.0 / 9.0
image_width = 400
image_height = int(image_width / aspect_ratio)

# camera
viewport_height = 2.0
viewport_width = aspect_ratio * viewport_height
focal_length = 1

origin = Point3(0,0,0)
horizontal = Vec3(viewport_width, 0, 0)
vertical = Vec3(0, viewport_height, 0)
lower_left_corner = origin - horizontal/2.0 - vertical/2.0 - Vec3(0, 0, focal_length)

# render
print(f"P3\n{image_width} {image_height}\n255")
for j in tqdm(range(image_height-1, -1, -1)):
    for i in range(image_width):
        u = i / (image_width - 1)
        v = j / (image_height - 1)
        r = Ray(origin, lower_left_corner + u*horizontal + v*vertical - origin)
        pixel_color: Color = ray_color(r, world)
        print(pixel_color.write_color())
