from vec3_class import Color, Point3, Vec3
from ray_class import Ray
from tqdm import tqdm
from math import sqrt

def ray_color(ray: Ray):
    t = hit_torus(Point3(0,0,-1), 0.5, 0.2, ray)
    if t > 0:
        normal: Vec3 = torus_normal(Point3(0,0,-1), 0.5, 0.2, ray.at(t))
        return 0.5 * Color(normal[0]+1, normal[1]+1, normal[2]+1)
    unit_direction = ray.direction.unit_vector()
    t = 0.5 * (unit_direction[1] + 1.0)
    return (1.0 - t) * Color(1.0, 1.0, 1.0) + t * Color(0.5, 0.7, 1)

def torus_distance_function(center: Point3, R: float, r: float, point: Point3):
    x, y, z = point.e[0] - center.e[0], point.e[1] - center.e[1], point.e[2] - center.e[2]
    temp = sqrt(x*x + y*y) - R
    return sqrt(temp*temp + z*z) - r

def hit_torus(center: Point3, R: float, r: float, ray: Ray, max_steps=100, epsilon=1e-3, t_max=1e3):
    t = 0.0
    for _ in range(max_steps):
        point = ray.at(t)
        d = torus_distance_function(center, R, r, point)
        if d < epsilon:
            return t
        t += d
        if t > t_max:
            break
    return -1.0

def torus_normal(center: Point3, R: float, r: float, point: Point3, delta=1e-5):
    dx = Vec3(delta, 0, 0)
    dy = Vec3(0, delta, 0)
    dz = Vec3(0, 0, delta)
    
    nx = torus_distance_function(center, R, r, point + dx) - torus_distance_function(center, R, r, point - dx)
    ny = torus_distance_function(center, R, r, point + dy) - torus_distance_function(center, R, r, point - dy)
    nz = torus_distance_function(center, R, r, point + dz) - torus_distance_function(center, R, r, point - dz)

    return Vec3(nx, ny, nz).unit_vector()

# Rest of the code remains unchanged




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
