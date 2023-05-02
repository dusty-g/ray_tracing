from vec3_class import Color, Point3, Vec3
from ray_class import Ray
from tqdm import tqdm
from math import sqrt

def ray_color(ray: Ray):
    t = hit_sphere(Point3(0,0,-1),0.5,ray)
    if(t > 0):
        normal: Vec3 = (ray.at(t) - Vec3(0,0,-1))
        normal = normal.unit_vector()
        return 0.5 * Color(normal[0]+1,  normal[1]+1, normal[2]+1)
    unit_direction = ray.direction.unit_vector()
    t = 0.5*(unit_direction[1] + 1.0)
    return (1.0 - t)*Color(1.0, 1.0, 1.0) + t*Color(0.5,0.7,1)

def hit_sphere(center: Point3, radius, r: Ray):
    oc = r.origin - center
    a = r.direction.dot(r.direction)
    b = 2.0 * oc.dot(r.direction)
    c = oc.dot(oc) - radius * radius
    discriminant = b * b - 4 * a * c
    if(discriminant < 0):
        return -1.0
    else:
        return (-b - sqrt(discriminant))/(2.0 * a)



aspect_ratio = 16.0 / 9.0
image_width = 400
image_height = int(image_width / aspect_ratio)

viewport_height = 2.0
viewport_width = aspect_ratio * viewport_height
focal_length = 1

origin = Point3(0,0,0)
horizontal = Vec3(viewport_width, 0, 0)
vertical = Vec3(0, viewport_height, 0)
lower_left_corner = origin - horizontal/2.0 - vertical/2.0 - Vec3(0, 0, focal_length)

print(f"P3\n{image_width} {image_height}\n255")
for j in tqdm(range(image_height-1, -1, -1)):
    for i in range(image_width):
        u = i / (image_width - 1)
        v = j / (image_height - 1)
        r = Ray(origin, lower_left_corner + u*horizontal + v*vertical - origin)
        pixel_color: Color = ray_color(r)
        print(pixel_color.write_color())
