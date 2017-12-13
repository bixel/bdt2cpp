from .Node import Node

import xml.etree.ElementTree as ET


class TMVANode(Node):
    def __init__(self, parent=None, xmlNode=None):
        super().__init__(parent=parent)
        print(xmlNode, xmlNode.get('nType'), xmlNode.items())
        if not parent or xmlNode.get('nType') == 0:
            self.final = False
        elif xmlNode is not None and xmlNode.get('nType') != 0:
            self.weight = self.parent.weight * xmlNode.get('nType')

        if len(xmlNode) == 2:
            left, right = list(xmlNode)
            self.left = TMVANode(self, left)
            self.right = TMVANode(self, right)
        elif len(xmlNode) not in [0, 2]:
            raise(ValueError(f"The node {xmlNode} seems not to be a proper "
                              "binary tree node"))


def parse_model(filename):
    trees = []
    with open(filename, 'r') as f:
        treeXML = ET.fromstring(f.read())

    for tree in treeXML.find('Weights'):
        firstNode = TMVANode(xmlNode=tree.find('Node'))
        firstNode.weight = tree.get('boostWeight')
        trees.append(firstNode)

    return trees
