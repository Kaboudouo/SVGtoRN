import os

template = """import {{ View, Text }} from "react-native";
import React from "react";
import {{ Defs, Path, RadialGradient, Stop, Svg, Rect, Ellipse }} from "react-native-svg";

interface Props{{
 width? : number;
 height? : number;
}}

const {component_name} = ({{width = 48, height = 24}} : Props) => {{
 return({svg_content})
}}

export default {component_name}
"""

def format_component_name(file_name):
    # Strip the .svg and capitalize the first letter of each word
    return ''.join(word.capitalize() for word in file_name.replace(".svg", "").split('_'))


for file_name in os.listdir('./TSXConvert'):
    print(file_name)
    if file_name.endswith('.svg'):
        with open(os.path.join('./TSXConvert', file_name), 'r') as svg_file:
            svg_content = svg_file.read()

            component_name = format_component_name(file_name)
            formatted_content = template.format(component_name=component_name, svg_content=svg_content)

            output_file_name = f"{component_name}.tsx"
            with open(output_file_name, 'w') as output_file:
                output_file.write(formatted_content)

        print(f"Generated {output_file_name}")

