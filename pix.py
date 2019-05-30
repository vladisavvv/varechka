from PIL import Image, ImageDraw
import math


def get_color_block(x, y, pix, width, height):
    A, B, C = 0, 0, 0
    num = 0

    for i in range(x, min(width, x + SIZE_BLOCK)):
        for j in range(y, min(height, y + SIZE_BLOCK)):
            a = pix[i, j][0]
            b = pix[i, j][1]
            c = pix[i, j][2]

            A += a
            B += b
            C += c

            num += 1

    if (num > 0):
        A //= num
        B //= num
        C //= num

    return A, B, C


def get_mid_color(colors):
    A, B, C = 0, 0, 0

    for color in colors:
        A += color[0]
        B += color[1]
        C += color[2]

    return A // len(colors), B // len(colors), C // len(colors)


def set_color_block(x, y, color, draw, width, height):
    for i in range(x, min(width, x + SIZE_BLOCK)):
        for j in range(y, min(height, y + SIZE_BLOCK)):
            draw.point((i, j), color)


def get_dist_for_two_color(first_color, second_color):
    dx = abs(first_color[0] - second_color[0])
    dy = abs(first_color[1] - second_color[1])
    dz = abs(first_color[2] - second_color[2])

    return math.sqrt(dx ** 2 + dy ** 2 + dz ** 2)


image = Image.open("medium.jpg")

SIZE_BLOCK = 17
NUMBER_COLOR = 5

width = image.size[0]
height = image.size[1]

pix = image.load()

draw = ImageDraw.Draw(image)

number_color = {}

for i_block in range(width // SIZE_BLOCK + (1 if width % SIZE_BLOCK == 0 else 0)):
    for j_block in range(height // SIZE_BLOCK + (1 if height % SIZE_BLOCK == 0 else 0)):
        color = get_color_block(i_block * SIZE_BLOCK, j_block * SIZE_BLOCK, pix, width, height)

        if number_color.get(color) is None:
            number_color[color] = 1
        else:
            number_color[color] = number_color.get(color) + 1

        set_color_block(i_block * SIZE_BLOCK, j_block * SIZE_BLOCK, color, draw, width, height)

image.show()

print len(number_color)

to_color = {}

while len(number_color) > 0:
    max_number = 0
    for color, number in number_color.iteritems():
        if number > max_number:
            max_number = number
            max_color = color

    list_colors = []

    for color, number in number_color.iteritems():
        if get_dist_for_two_color(color, max_color) < 35:
            list_colors.append(color)

    mid_color = get_mid_color(list_colors)

    for color, number in number_color.iteritems():
        if get_dist_for_two_color(color, max_color) < 35:
            to_color[color] = max_color

    # print max_color, len(list_colors)

    for color in list_colors:
        number_color.pop(color)

number_color = {}

for i_block in range(width // SIZE_BLOCK + (1 if width % SIZE_BLOCK == 0 else 0)):
    for j_block in range(height // SIZE_BLOCK + (1 if height % SIZE_BLOCK == 0 else 0)):
        color = get_color_block(i_block * SIZE_BLOCK, j_block * SIZE_BLOCK, pix, width, height)

        if not to_color.get(color) is None:
            color = to_color.get(color)

        if number_color.get(color) is None:
            number_color[color] = 1
        else:
            number_color[color] = number_color.get(color) + 1

        set_color_block(i_block * SIZE_BLOCK, j_block * SIZE_BLOCK, color, draw, width, height)

size = (height // SIZE_BLOCK + (1 if height % SIZE_BLOCK == 0 else 0)) * (width // SIZE_BLOCK + (1 if width % SIZE_BLOCK == 0 else 0))
print len(number_color), size

image.show()
