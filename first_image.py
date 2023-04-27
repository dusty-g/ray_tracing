# image width and height
image_width = 256
image_height = 256

# print P3 followed by the width and height, then 255 for max color
print(f"P3\n{image_width} {image_height}\n255")

# for loops over the image from top to bottom
for j in range(image_height - 1, -1, -1):
    for i in range(image_width):
        r = i / (image_width - 1)
        g = j / (image_height - 1)
        b = 0.25

        ir = int(255.99 * r)
        ig = int(255.99 * g)
        ib = int(255.99 * b)
        print(f"{ir} {ig} {ib}")

