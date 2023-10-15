import os


directory = './TSXConvert'


output_file_name = 'exports.txt'


with open(output_file_name, 'w') as output_file:
    # Iterate over each file in the directory
    for file_name in os.listdir(directory):
        # If the file ends with .tsx (or any other extension you want)
        if file_name.endswith('.tsx'):
            # Remove the file extension to get just the filename
            base_name = os.path.splitext(file_name)[0]


            output_file.write(f'export {{ default as {base_name} }} from "../../../../assets/exercises/fullSvgs/{base_name}";\n')

print(f"Exports written to {output_file_name}")