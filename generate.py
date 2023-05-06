from camera import Camera
from material import Lambertian, Material, Metal
from vec3 import Color, Point3, Vec3
from ray import Ray
from tqdm import tqdm
from math import sqrt
from hittable import Sphere, HittableList, Torus
from rtweekend import infinity, pi, degrees_to_radians
import random
from typing import List, Tuple
from concurrent.futures import ProcessPoolExecutor, as_completed


def ray_color(ray: Ray, world: HittableList, depth: int):
    if depth <= 0:
        return Color(0,0,0)
    
    hit_record = world.hit(ray, 0.001, infinity)
    if hit_record:
        result = hit_record.material.scatter(ray, hit_record)
        if result is not None:
            scattered, attenuation = result
            return attenuation * ray_color(scattered, world, depth -1)
        return Color(0,0,0)
    unit_direction = ray.direction.unit_vector()
    t = 0.5*(unit_direction[1] + 1.0)
    return (1.0 - t)*Color(1.0, 1.0, 1.0) + t*Color(0.5,0.7,1)



# world
world = HittableList()
material_ground: Material = Lambertian(Color(0.8, 0.8, 0.0))
material_center: Material = Lambertian(Color(0.7, 0.3, 0.3))

material_left: Material = Metal(Color(0.8, 0.8, 0.8))
material_right: Material = Metal(Color(0.8, 0.6, 0.2))

world.add(Sphere(Point3(0,-100.5,-1), 100, material_ground))
world.add(Sphere(Point3(0, 0, -1), 0.5, material_center))
world.add(Sphere(Point3(-1, 0, -1), 0.5, material_left))
world.add(Sphere(Point3(1, 0, -1), 0.5, material_right))
# world.add(Torus(Point3(-1, 0, -1), 0.3, 0.2, material_left))


# image
aspect_ratio = 16.0 / 9.0
image_width = 400
image_height = int(image_width / aspect_ratio)
samples_per_pixel = 100
max_depth: int = 50

# camera
camera = Camera()


def render_row(width: int, height: int, samples_per_pixel: int, camera: Camera, world: HittableList, row: int) -> Tuple[int, List[Vec3]]:
    row_pixels = []
    for x in range(width):
        pixel_color = Color(0,0,0)
        for sample in range(samples_per_pixel):
            u = (x + random.random()) / (width - 1)
            v = (row + random.random()) / (height - 1)
            r = camera.get_ray(u,v)
            pixel_color += ray_color(r, world, max_depth)
        row_pixels.append(pixel_color)
    return row, row_pixels

def main():

    with ProcessPoolExecutor() as executor:
        futures = [executor.submit(render_row, image_width, image_height, samples_per_pixel, camera, world, row) for row in range(image_height)]
        rendered_rows = [None for _ in range(image_height)]
        progress_bar = tqdm(total=image_height, desc="Rendering", ncols=100)
        for f in as_completed(futures):
            row, row_pixels = f.result()
            rendered_rows[row] = row_pixels # type: ignore
            progress_bar.update(1)
        progress_bar.close()
    # render
    print(f"P3\n{image_width} {image_height}\n255")

    for row in reversed(rendered_rows):
        for color in row: # type: ignore
            print(color.write_color(samples_per_pixel))

if __name__ == '__main__':
    main()
