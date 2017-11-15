import re

from .Node import Node



class XGBoostNode(Node):
    FLOAT_REGEX = '[+-]?\d+(\.\d+)?([eE][+-]?\d+)?'
    BRANCH_REGEX = re.compile(f'(?P<branch>\d+):\[(?P<feature>\w+)(?P<comp><)(?P<value>{FLOAT_REGEX})\]')
    LEAF_REGEX = re.compile(f'(?P<leaf>\d+):leaf=(?P<value>{FLOAT_REGEX})')
    FEATURE_REGEX = re.compile('\w(?P<id>\d+)')

    def __init__(self, parent=None, line='', feature_index_dict=None):
        super().__init__(parent=parent)
        # propagate any feature index dict
        self.feature_index_dict = None
        if feature_index_dict or parent:
            self.feature_index_dict = feature_index_dict or parent.feature_index_dict

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
            if self.feature_index_dict:
                self.feature_index = self.feature_index_dict[self.feature]
            else:
                feature_match = self.FEATURE_REGEX.search(self.feature)
                if not feature_match:
                    raise ValueError(f'Feature {self.feature} needs to be '
                            'matched with its correct position in the feature '
                            'value vector. Please give a list of feature names'
                            ' in the correct order with `--feature-names`.')
                self.feature_index = feature_match.groupdict().get('id')
        else:
            self.cut_value = None
            self.feature = None
            self.feature_index = None


def get_feature_names(lines):
    features = set()
    for l in lines:
        match_branch = XGBoostNode.BRANCH_REGEX.search(l)
        if match_branch:
            features.add(match_branch.groupdict().get('feature'))
    return features


def parse_model(filename, feature_names):
    trees = []
    with open(filename, 'r') as f:
        lines = f.readlines()

    # build the feature name dict if neccessary
    if feature_names:
        # check that the feature names are in line with the names found in
        # the tree
        if not set(feature_names) >= get_feature_names(lines):
            raise ValueError('The given feature names do not properly describe'
                'the features found in the model. Please check that your '
                'argument for `--feature-names` is a proper superset of the '
                'feature names used in the model.\nThese features have been '
                f'found in the model:\n{" ".join(get_feature_names(lines))}')
        feature_index_dict = {name: i for i, name in enumerate(feature_names)}
    else:
        feature_index_dict = None

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
            node = XGBoostNode(line=line, feature_index_dict=feature_index_dict)
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
