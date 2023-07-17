import colorsys
import os
from bs4 import BeautifulSoup

in_folder_path = './SVGs'
out_folder_path = './ColorSwapped'
new_colors = ["#36272E", "#7D6D6E" , "#A8B6B7", "#2A191F" , "#211415", "#2A1C1F"]

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

def swap_colors_based_on_relative_luminance(in_folder_path, out_folder_path, new_colors):
    new_colors = sorted(new_colors, key=lambda x: luminance(*hex_to_rgb(x)))
    
    for filename in os.listdir(in_folder_path):
        in_file_path = os.path.join(in_folder_path, filename)
        out_file_path = os.path.join(out_folder_path, filename)
        
        with open(in_file_path, "r") as file:
            svg = BeautifulSoup(file.read(), 'lxml')
            
            # Hold a reference to all the colors we find, and their corresponding elements
            colors_found = defaultdict(list)
            
            # Iterate over each shape
            for shape in svg.find_all(['circle', 'rect', 'polygon', 'path', 'ellipse']):
                # Get the fill color
                fill_color = shape.get('fill')

                # If the fill color is not a hex color, skip this shape
                if not fill_color or not fill_color.startswith('#'):
                    continue
                
                # Add this shape to our colors_found dictionary
                colors_found[fill_color].append(shape)
                
            # Sort the found colors by their luminance
            colors_found = sorted(colors_found.items(), key=lambda item: luminance(*hex_to_rgb(item[0])))
            
            # For each color in our colors_found list, replace it with a corresponding color from new_colors
            for i, (color, shapes) in enumerate(colors_found):
                new_color_index = i * len(new_colors) // len(colors_found)  # Scale the index to fit within new_colors
                new_color = new_colors[new_color_index]
                for shape in shapes:
                    shape['fill'] = new_color
                    
            with open(out_file_path, "w") as file:
                file.write(str(svg))

        # if (os.path.exists(in_file_path)):
        #     os.remove(in_file_path)
        # else:
        #     print("File does not exist.")

swap_colors_based_on_relative_luminance(in_folder_path, out_folder_path, new_colors)

