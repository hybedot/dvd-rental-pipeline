from jinja2 import Environment, FileSystemLoader 
import yaml 
import os
from pathlib import Path


file_dir = Path(__file__).parent.parent.parent
env = Environment(loader=FileSystemLoader(f"{file_dir}/include"))
template = env.get_template('templates/dag_template.jinja2')

print(file_dir)


for filename in os.listdir(f"{file_dir}/include/inputs"):
    print(filename)
    if filename.endswith('.yaml'):
        with open(f"{file_dir}/include/inputs/{filename}", "r") as input_file:
            inputs = yaml.safe_load(input_file)
            with open (f"{file_dir}/dags/{inputs['table_name']}_extract_load.py", "w") as f:
                f.write(template.render(inputs))