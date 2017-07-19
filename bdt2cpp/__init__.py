from jinja2 import Template
from os import path
import re
import numpy as np

CUR_DIR = path.abspath('.')
TEMPLATE_DIR = path.join(path.abspath(path.dirname(__file__)), 'templates')
BRANCH_REGEX = re.compile('(?P<branch>\d+):\[(?P<feature>\w+)(?P<comp><)(?P<value>-?\d+\.\d+)\]')
LEAF_REGEX = re.compile('(?P<leaf>\d+):leaf=(?P<value>-?\d+\.\d+)')
FEATURE_REGEX = re.compile('\w(?P<id>\d+)')


class Node:
    def __init__(self, line, parent=None):
        self.left = None
        self.right = None
        self.parent = parent
        self.level = 0 if not parent else parent.level + 1

        match_leaf = LEAF_REGEX.search(line)
        if match_leaf:
            self.weight = float(match_leaf.groupdict().get('value'))
            self.final = True
        else:
            self.weight = 0
            self.final = False

        match_branch = BRANCH_REGEX.search(line)
        if match_branch:
            self.cut_value = match_branch.groupdict().get('value')
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


def main(output_file='main.cpp'):
    trees = parse_model('/Users/kheinicke/playground/random.model')

    with open(path.join(TEMPLATE_DIR, 'main.cpp.template'), 'r') as f:
        template = Template(f.read())

    with open(path.join(CUR_DIR, output_file), 'w') as f:
        f.write(template.render(trees=trees))
