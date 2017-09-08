""" bdt2cpp
Transpile your bdt weight file into compilable c++ code.
"""

from os import path, getcwd, mkdir
import re

import jinja2

from .XGBoostParser import parse_model as parse_model_xgb

CUR_DIR = getcwd()
TEMPLATE_DIR = path.join(path.abspath(path.dirname(__file__)), 'templates')


def split(arr, splits=2):
    """Split given array into `splits` smaller, similar sized arrays"""

    if len(arr) < splits:
        raise ValueError("Can't find more splits than array has elements")

    new_size = int(len(arr) / splits)
    return ([arr[n * new_size:(n + 1) * new_size] for n in range(splits - 1)]
            + [arr[(splits - 1) * new_size:]])


def main(input_file, output_dir='build', trees_per_file=None):
    """
    Read in input file, render templates and write compilable files to
    output_dir.
    """
    # template settings
    env = jinja2.Environment(loader=jinja2.PackageLoader('bdt2cpp'),
                             trim_blocks=True, lstrip_blocks=True)

    full_ensemble = parse_model_xgb(input_file)

    if trees_per_file and len(full_ensemble) > trees_per_file:
        trees = split(full_ensemble, int(len(full_ensemble) / trees_per_file))
    else:
        trees = [full_ensemble]

    if not path.isdir(output_dir):
        mkdir(output_dir)

    # render subtrees if any
    if len(trees) > 1:
        tree_template = env.get_template('standalone.function.template')
        for i, tree in enumerate(trees):
            with open(path.join(CUR_DIR, output_dir, f'tree_{i}.cpp'), 'w') as out:
                out.write(tree_template.render(tree_number=i, tree=tree))

    # render main template
    template = env.get_template('main.cpp.template')
    with open(path.join(CUR_DIR, output_dir, 'main.cpp'), 'w') as out:
        out.write(template.render(trees=trees))

    # render makefile
    template = env.get_template('Makefile.template')
    with open(path.join(CUR_DIR, output_dir, 'Makefile'), 'w') as out:
        out.write(template.render(trees=trees))
