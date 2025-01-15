# Written by Noa Chayer
# 07-06-23
# No interface | To be converted SVGs are placed in the SVGs folder > run main.py > RN Componts appear in RN-Components folder
# This find and replace tool was made assuming a pre-existing interface with size and color. Modify to suit your needs.

import os
import re
import string

# Paths
in_folder_path = './SVGs'
out_folder_path = './RN-Components'

# Suffix for new files
suffix = "Icon"

for filename in os.listdir(in_folder_path):

    # Input and output paths
    in_file_path = os.path.join(in_folder_path, filename)
    base_name, _ = os.path.splitext(filename)
    out_file_name = f"{base_name}{suffix}.tsx"
    out_file_path = os.path.join(out_folder_path, out_file_name)

    with open(in_file_path, "r") as file:
        # Read and process SVG file contents
        file_contents = file.read()
        file_contents = re.sub(r'<svg width="(\d+)" height="(\d+)"', "<Svg width={size} height={size}", file_contents)    
        file_contents = file_contents.replace('xmlns="http://www.w3.org/2000/svg"', "")

        for letter in string.ascii_lowercase:
            file_contents = file_contents.replace("<" + letter, "<" + letter.upper())
            file_contents = file_contents.replace("</" + letter, "</" + letter.upper())

        file_contents = file_contents.replace('"#D9D9D9"', "{color}")  # Replace main color
        file_contents = file_contents.replace('"#000000"', "{subColor}")  # Replace sub color

        file_contents = re.sub(r'stroke-width="(\d+)"', r'strokeWidth={\1}', file_contents)
        file_contents = re.sub(r"(^|[-_])([a-zA-Z])", lambda x: x.group(2).upper(), file_contents)

        # Create the functional component
        functionalComponent = f"""
import React from 'react'
import Svg, {{ Path }} from 'react-native-svg'

interface Props {{
    size?: number;
    color?: string;
    subColor?: string;
}}

const {base_name}{suffix} = ({{ size = 24, color = '#D9D9D9', subColor = '#000000' }}: Props) => {{
  return (
    {file_contents}
  )
}}

export default {base_name}{suffix}
"""

        # Write the component to the output file
        with open(out_file_path, "w") as out_file:
            out_file.write(functionalComponent)

    # Remove the input file
    if os.path.exists(in_file_path):
        os.remove(in_file_path)
    else:
        print(f"File {in_file_path} does not exist.")