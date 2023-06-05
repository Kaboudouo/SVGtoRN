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
        file_contents = file_contents.replace('fill="#D9D9D9"', "fill={color}")
        file_contents = file_contents.replace('stroke="#D9D9D9"', "stroke={color}")

        with open(out_file_path, "w") as file:
            file.write(file_contents)
        

