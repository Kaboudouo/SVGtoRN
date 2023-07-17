import colorsys
import os
from bs4 import BeautifulSoup
import numpy as np

in_folder_path = './SVGs'
out_folder_path = './ColorSwapped'
new_colors = ["#36272E", "#7D6D6E" , "#A8B6B7", "#2A191F" , "#211415", "#2A1C1F"]

def interpolate_color(color1, color2, ratio):
    # Interpolate between two RGB colors
    r1, g1, b1 = hex_to_rgb(color1)
    r2, g2, b2 = hex_to_rgb(color2)
    r = r1 + ratio * (r2 - r1)
    g = g1 + ratio * (g2 - g1)
    b = b1 + ratio * (b2 - b1)
    return rgb_to_hex((int(r), int(g), int(b)))

def luminance(r, g, b):
    # The relative luminance is calculated using this formula
    # Y = 0.2126*R + 0.7152*G + 0.0722*B
    return 0.2126*r + 0.7152*g + 0.0722*b

def hex_to_rgb(hex_color):
    # Convert hexadecimal color to RGB
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb_color):
    # Convert RGB to hexadecimal
    return "#{:02x}{:02x}{:02x}".format(*rgb_color)

from collections import defaultdict

def swap_colors_with_interpolation(in_folder_path, out_folder_path, new_colors):
    new_colors = sorted(new_colors, key=lambda x: luminance(*hex_to_rgb(x)))

    for filename in os.listdir(in_folder_path):
        in_file_path = os.path.join(in_folder_path, filename)
        out_file_path = os.path.join(out_folder_path, filename)

        with open(in_file_path, "r") as file:
            svg = BeautifulSoup(file.read(), 'lxml')

            colors_found = defaultdict(list)

            for shape in svg.find_all(['circle', 'rect', 'polygon', 'path', 'ellipse']):
                fill_color = shape.get('fill')

                if not fill_color or not fill_color.startswith('#'):
                    continue

                colors_found[fill_color].append(shape)

            colors_found = sorted(colors_found.items(), key=lambda item: luminance(*hex_to_rgb(item[0])))

            for i, (color, shapes) in enumerate(colors_found):
                color_ratio = i / (len(colors_found) - 1)  # normalize to range 0.0 - 1.0
                new_color_index = color_ratio * (len(new_colors) - 1)  # Scale the index to fit within new_colors
                
                lower_index = int(np.floor(new_color_index))
                upper_index = int(np.ceil(new_color_index))
                
                if lower_index == upper_index:  # new_color_index is integer, so just pick the color
                    new_color = new_colors[lower_index]
                else:  # Interpolate the color
                    lower_color = new_colors[lower_index]
                    upper_color = new_colors[upper_index]
                    ratio = new_color_index - lower_index  # ratio for the interpolation
                    new_color = interpolate_color(lower_color, upper_color, ratio)

                for shape in shapes:
                    shape['fill'] = new_color

            with open(out_file_path, "w") as file:
                file.write(str(svg))
                
        # if (os.path.exists(in_file_path)):
        #     os.remove(in_file_path)
        # else:
        #     print("File does not exist.")

swap_colors_with_interpolation(in_folder_path, out_folder_path, new_colors)

