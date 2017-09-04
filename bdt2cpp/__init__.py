import jinja2
from os import path, getcwd, mkdir
import re
import numpy as np

CUR_DIR = getcwd()
float_regex = '[+-]?\d+(\.\d+)?([eE][+-]?\d+)?'
TEMPLATE_DIR = path.join(path.abspath(path.dirname(__file__)), 'templates')
BRANCH_REGEX = re.compile(f'(?P<branch>\d+):\[(?P<feature>\w+)(?P<comp><)(?P<value>{float_regex})\]')
LEAF_REGEX = re.compile(f'(?P<leaf>\d+):leaf=(?P<value>{float_regex})')
FEATURE_REGEX = re.compile('\w(?P<id>\d+)')


class Node:
    root_id_counter = 0

    def __init__(self, line, parent=None):
        self.left = None
        self.right = None
        self.parent = parent
        self.level = 0 if not parent else parent.level + 1
        if not parent:
            self.id = Node.root_id_counter
            Node.root_id_counter += 1

        match_leaf = LEAF_REGEX.search(line)
        if match_leaf:
            self.weight = float(match_leaf.groupdict().get('value'))
            self.final = True
        else:
            self.weight = 0
            self.final = False

        match_branch = BRANCH_REGEX.search(line)
        if match_branch:
            self.cut_value = float(match_branch.groupdict().get('value'))
            self.feature = match_branch.groupdict().get('feature')
            feature_match = FEATURE_REGEX.search(self.feature)
            self.feature_index = feature_match.groupdict().get('id')
        else:
            self.cut_value = None
            self.feature = None
            self.feature_index = None

    def __str__(self):
        if self.final:
            return f'{self.level*"  "}{self.weight}'
        else:
            return (f'{self.level*"  "}{self.feature} < {self.cut_value}\n'
                    f'{self.left}\n'
                    f'{self.right}')

    def __iter__(self):
        return [self].__iter__()

    @property
    def root(self):
        if self.parent:
            return self.parent.root
        else:
            return self


def parse_model(filename):
    trees = []
    with open(filename, 'r') as f:
        lines = f.readlines()

    node = None
    for i, line in enumerate(lines):
        # save finished tree
        if line.startswith('booster'):
            if node:
                trees.append(node.root)
                node = None
            continue

        # start a new tree
        if node is None:
            node = Node(line)
            continue

        # move upwards if a leaf is reached
        while node.final or (node.parent and node.left and node.right):
            node = node.parent

        # fill left and right leaf
        if not node.left:
            node.left = Node(line, parent=node)
            node = node.left
            continue

        if not node.right:
            node.right = Node(line, parent=node)
            node = node.right
            continue

    trees.append(node.root)

    return trees


def split(arr, splits=2):
    """Split given array into `splits` smaller, similar sized arrays"""

    if len(arr) < splits:
        raise ValueError("Can't find more splits than array has elements")

    new_size = int(len(arr) / splits)
    return ([arr[n * new_size:(n+1) * new_size] for n in range(splits-1)]
            + [arr[(splits-1) * new_size:]])


def main(input_file, output_dir='build', trees_per_file=None):
    # template settings
    env = jinja2.Environment(loader=jinja2.PackageLoader('bdt2cpp'),
                             trim_blocks=True, lstrip_blocks=True)

    full_ensemble = parse_model(input_file)

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
            with open(path.join(CUR_DIR, output_dir, f'tree_{i}.cpp'), 'w') as f:
                f.write(tree_template.render(tree_number=i, tree=tree))

    # render main template
    template = env.get_template('main.cpp.template')
    with open(path.join(CUR_DIR, output_dir, 'main.cpp'), 'w') as f:
        f.write(template.render(trees=trees))

    # render makefile
    template = env.get_template('Makefile.template')
    with open(path.join(CUR_DIR, output_dir, 'Makefile'), 'w') as f:
        f.write(template.render(trees=trees))
