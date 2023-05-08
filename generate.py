from camera import Camera
from material import Dielectric, Lambertian, Material, Metal
from vec3 import Color, Point3, Vec3
from ray import Ray
from tqdm import tqdm
from math import sqrt, cos
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








# image
aspect_ratio = 16.0 / 9.0
image_width = 1200
image_height = int(image_width / aspect_ratio)
samples_per_pixel = 100
max_depth: int = 50

# camera
lookfrom = Point3(13,2,3)
lookat = Point3(0,0,0)
vup: Vec3 = Vec3(0,1,0)
dist_to_focus = 10
aperture = 0.1
camera = Camera(lookfrom, lookat, vup,aperture, dist_to_focus, vfov=20)




def random_scene()->HittableList:
    world = HittableList()
    ground_material = Lambertian(Color(0.5, 0.5, 0.5))
    world.add(Sphere(Point3(0,-1000,0), 1000, ground_material))
    for a in range(-11,11):
        for b in range(-11,11):
            choose_mat = random.random()
            center: Point3 = Point3(a+0.9*random.random(),0.2,b+0.9*random.random())
            if ((center - Point3(4, 0.2, 0)).length() > 0.9):
                sphere_material: Material
                if choose_mat < 0.8:
                    # diffuse
                    albedo = Color.random() * Color.random()
                    sphere_material = Lambertian(albedo)
                    world.add(Sphere(center, 0.2, sphere_material))
                elif choose_mat < 0.95:
                    # metal
                    albedo = Color.random(0.5, 1)
                    fuzz = random.uniform(0,0.5)
                    sphere_material = Metal(albedo, fuzz)
                    world.add(Sphere(center, 0.2, sphere_material))
                else:
                    # glass
                    sphere_material = Dielectric(1.5)
                    world.add(Sphere(center, 0.2, sphere_material))
    material1: Material = Dielectric(1.5)
    world.add(Sphere(Point3(0,1,0), 1.0, material1))

    material2: Material = Lambertian(Color(0.4, 0.2, 0.1))
    world.add(Sphere(Point3(-4, 1, 0), 1, material2))

    material3: Material = Metal(Color(0.7, 0.6, 0.5), 0)
    world.add(Sphere(Point3(4,1,0), 1, material3))
    return world

# world
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
    world: HittableList = random_scene()
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
