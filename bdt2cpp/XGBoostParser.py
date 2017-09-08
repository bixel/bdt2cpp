import re

from .Node import Node



class XGBoostNode(Node):
    FLOAT_REGEX = '[+-]?\d+(\.\d+)?([eE][+-]?\d+)?'
    BRANCH_REGEX = re.compile(f'(?P<branch>\d+):\[(?P<feature>\w+)(?P<comp><)(?P<value>{FLOAT_REGEX})\]')
    LEAF_REGEX = re.compile(f'(?P<leaf>\d+):leaf=(?P<value>{FLOAT_REGEX})')
    FEATURE_REGEX = re.compile('\w(?P<id>\d+)')

    def __init__(self, parent=None, line=''):
        super().__init__(parent=parent)

        match_leaf = self.LEAF_REGEX.search(line)
        if match_leaf:
            self.weight = float(match_leaf.groupdict().get('value'))
            self.final = True
        else:
            self.weight = 0
            self.final = False

        match_branch = self.BRANCH_REGEX.search(line)
        if match_branch:
            self.cut_value = float(match_branch.groupdict().get('value'))
            self.feature = match_branch.groupdict().get('feature')
            feature_match = self.FEATURE_REGEX.search(self.feature)
            self.feature_index = feature_match.groupdict().get('id')
        else:
            self.cut_value = None
            self.feature = None
            self.feature_index = None


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
            node = XGBoostNode(line=line)
            continue

        # move upwards if a leaf is reached
        while node.final or (node.parent and node.left and node.right):
            node = node.parent

        # fill left and right leaf
        if not node.left:
            node.left = XGBoostNode(parent=node, line=line)
            node = node.left
            continue

        if not node.right:
            node.right = XGBoostNode(parent=node, line=line)
            node = node.right
            continue

    trees.append(node.root)

    return trees
