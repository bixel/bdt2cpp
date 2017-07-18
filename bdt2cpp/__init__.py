from jinja2 import Template
from os import path

TEMPLATE_DIR = path.join(path.abspath(path.dirname(__file__)), 'templates')

def main(output_file='main.cpp'):
    with open(path.join(TEMPLATE_DIR, 'main.cpp'), 'r') as f:
        template = Template(f.read())

    with open(output_file, 'w') as f:
        f.write(template.render(foo='bar'))
