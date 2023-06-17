# Written by Noa Chayer
# 07-06-23
# No interface | To be converted SVGs are placed in the SVGs folder > run main.py > RN Componts appear in RN-Components folder
# This find and replace tool was made assuming a pre-existing interface with size and color. Modify to suit your needs.

import os
import re

in_folder_path = './SVGs'
out_folder_path = './RN-Components'

for filename in os.listdir(in_folder_path):

    in_file_path = os.path.join(in_folder_path, filename)
    out_file_path = os.path.join(out_folder_path, filename)

    with open(in_file_path, "r") as file:
        file_contents = file.read()
        
        file_contents = re.sub(r'<svg width="(\d+)" height="(\d+)"', "<Svg width={size} height={size}", file_contents)    
        file_contents = file_contents.replace('xmlns="http://www.w3.org/2000/svg"', "")
        file_contents = file_contents.replace("</svg", "</Svg")

        file_contents = file_contents.replace("<path", "<Path")
        file_contents = file_contents.replace("<rect", "<Rect")
        file_contents = file_contents.replace("<circle", "<Circle")
        file_contents = file_contents.replace("<mask", "<Mask")

        file_contents = file_contents.replace("<line", "<Line")
        file_contents = file_contents.replace("</line", "</Line")
        file_contents = file_contents.replace("<stop", "<Stop")
        file_contents = file_contents.replace("<defs", "<Defs")
        file_contents = file_contents.replace("</defs", "</Defs")

        file_contents = file_contents.replace("<g", "<G")
        file_contents = file_contents.replace("</g", "</G")

        file_contents = file_contents.replace('fill="#D9D9D9"', "fill={color}") # Uses #D9D9D9 as reference to replace
        file_contents = file_contents.replace('stroke="#D9D9D9"', "stroke={color}") # Replace to suit your needs

        file_contents = re.sub(r'stroke-width="(\d+)"', r'strokeWidth={\1}', file_contents)
        file_contents = re.sub('stroke-linecap', 'strokeLinecap', file_contents)
        file_contents = re.sub('stop-color', 'stopColor', file_contents)

        with open(out_file_path, "w") as file:
            file.write(file_contents)

    if (os.path.exists(in_file_path)):
        os.remove(in_file_path)
    else:
        print("File does not exist.")
