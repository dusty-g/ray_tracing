from tqdm import tqdm
from vec3 import Color
# image width and height 
image_width = 256
image_height = 256

# print P3 followed by the width and height, then 255 for max color
print(f"P3\n{image_width} {image_height}\n255")

# for loops over the image from top to bottom
# for j in range(image_height - 1, -1, -1):
# use tqdm
for j in tqdm(range(image_height - 1, -1, -1)): 
    for i in range(image_width):
        
        color = Color(i / (image_width - 1), j / (image_height - 1), 0.25)
        
        print(color.write_color())

