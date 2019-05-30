from PIL import Image, ImageDraw
from math import sqrt
from random import randint
from enum import Enum


class TypePixelation(Enum):
    K_AVERAGE_RANDOM_POINT = 1
    K_AVERAGE_POPULAR_POINT = 2
    NEURAL_NETWORK = 3
    CUSTOM_ALGORITHM = 4
    NONE = 5


class Pixelation:
    # static settings
    NUMBER_ITERATION = 10

    def __init__(self, path_to_read_file, size_block, number_colors, type_pixelation):
        self.size_block = size_block
        self.number_colors = number_colors
        self.type = type_pixelation

        self.image = Image.open(path_to_read_file)
        self.pixels = self.image.load()
        self.image_draw = ImageDraw.Draw(self.image)

        self.width = self.image.size[0]
        self.height = self.image.size[1]

        self.number_blocks_in_width = (self.width + self.size_block - 1) // self.size_block
        self.number_blocks_in_height = (self.height + self.size_block - 1) // self.size_block

    @staticmethod
    def _get_average_color(colors):
        if len(colors) == 0:
            return -1, -1, -1

        sum_r, sum_g, sum_b = 0, 0, 0

        for color in colors:
            sum_r += color[0]
            sum_g += color[1]
            sum_b += color[2]

        return sum_r // len(colors), sum_g // len(colors), sum_b // len(colors)

    def _get_average_color_in_block(self, x, y):
        colors = []
        for i in range(x, min(self.width, x + self.size_block)):
            for j in range(y, min(self.height, y + self.size_block)):
                colors.append(self.pixels[i, j])

        return self._get_average_color(colors)

    def _set_color_block(self, x, y, color):
        for i in range(x, min(self.width, x + self.size_block)):
            for j in range(y, min(self.height, y + self.size_block)):
                self.image_draw.point((i, j), color)

    @staticmethod
    def _get_dist_for_two_color(first_color, second_color):
        delta_r = abs(first_color[0] - second_color[0])
        delta_g = abs(first_color[1] - second_color[1])
        delta_b = abs(first_color[2] - second_color[2])

        return sqrt(delta_r ** 2 + delta_g ** 2 + delta_b ** 2)

    def _break_into_blocks(self):
        for i_block in range(self.number_blocks_in_width):
            for j_block in range(self.number_blocks_in_height):
                color_for_block = self._get_average_color_in_block(i_block * self.size_block, j_block * self.size_block)

                self._set_color_block(i_block * self.size_block, j_block * self.size_block, color_for_block)

    @staticmethod
    def _get_k_most_popular_color(colors, k):
        number_color = {}

        for color in colors:
            if number_color.get(color) is None:
                number_color[color] = 1
            else:
                number_color[color] = number_color[color] + 1

        number_color_list = []
        for color, number in number_color.items():
            number_color_list.append([number, color])

        number_color_list.sort()
        number_color_list.reverse()

        return [number_color_list[i][1] for i in range(k)]

    def _get_id_nearest_point(self, point, random_points):
        dist_to_nearest_point = 10 ** 10  # big integer
        nearest_point_id = -1

        for point_id in range(len(random_points)):
            dist = self._get_dist_for_two_color(point, random_points[point_id])
            if dist < dist_to_nearest_point:
                dist_to_nearest_point = dist
                nearest_point_id = point_id

        return nearest_point_id

    def _get_all_colors(self):
        colors = []

        for i_block in range(self.number_blocks_in_width):
            for j_block in range(self.number_blocks_in_height):
                colors.append(self.pixels[i_block * self.size_block, j_block * self.size_block])

        return colors

    def _solve_clustering(self):
        if self.type == TypePixelation.K_AVERAGE_POPULAR_POINT:
            center_points = self._get_k_most_popular_color(self._get_all_colors(), self.number_colors)
        else:
            center_points = []
            for i in range(self.number_colors):
                center_points.append((randint(0, 255), randint(0, 255), randint(0, 255)))

        list_points_match_random_point = [[] for i in range(self.number_colors)]
        for it in range(self.NUMBER_ITERATION):
            for list_points in list_points_match_random_point:
                list_points.clear()

            for i_block in range(self.number_blocks_in_width):
                for j_block in range(self.number_blocks_in_height):
                    list_points_match_random_point[self._get_id_nearest_point(self.pixels[
                        i_block * self.size_block,
                        j_block * self.size_block
                    ], center_points)].append(self.pixels[i_block * self.size_block, j_block * self.size_block])

            for list_points_id in range(self.number_colors):
                center_points[list_points_id] = self._get_average_color(list_points_match_random_point[list_points_id])

        to_color = {}
        for list_points in list_points_match_random_point:
            average_color = self._get_average_color(list_points)

            for point in list_points:
                to_color[point] = average_color

        for i_block in range(self.number_blocks_in_width):
            for j_block in range(self.number_blocks_in_height):
                self._set_color_block(i_block * self.size_block, j_block * self.size_block, to_color[self.pixels[i_block * self.size_block, j_block * self.size_block]])

    def process_image(self):
        self._break_into_blocks()
        if self.type == TypePixelation.K_AVERAGE_POPULAR_POINT or self.type == TypePixelation.K_AVERAGE_RANDOM_POINT:
            self._solve_clustering()
        self.image.show()


pixelation = Pixelation('res/varya.jpg', 10, 30, TypePixelation.K_AVERAGE_POPULAR_POINT)
pixelation.process_image()

# to_color = {}
#
# while len(number_color) > 0:
#     max_number = 0
#     for color, number in number_color.items():
#         if number > max_number:
#             max_number = number
#             max_color = color
#
#     list_colors = []
#
#     for color, number in number_color.items():
#         if get_dist_for_two_color(color, max_color) < 35:
#             list_colors.append(color)
#
#     mid_color = get_mid_color(list_colors)
#
#     for color, number in number_color.items():
#         if get_dist_for_two_color(color, max_color) < 35:
#             to_color[color] = max_color
#
#     for color in list_colors:
#         number_color.pop(color)
#
# number_color = {}
#
# for i_block in range(width // SIZE_BLOCK + (1 if width % SIZE_BLOCK == 0 else 0)):
#     for j_block in range(height // SIZE_BLOCK + (1 if height % SIZE_BLOCK == 0 else 0)):
#         color = get_color_block(i_block * SIZE_BLOCK, j_block * SIZE_BLOCK, pix, width, height)
#
#         if not to_color.get(color) is None:
#             color = to_color.get(color)
#
#         if number_color.get(color) is None:
#             number_color[color] = 1
#         else:
#             number_color[color] = number_color.get(color) + 1
#
#         set_color_block(i_block * SIZE_BLOCK, j_block * SIZE_BLOCK, color, draw, width, height)
#
# print(len(number_color), size)
#
# image.show()
