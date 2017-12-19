from .Node import Node

import xml.etree.ElementTree as ET


class TMVANode(Node):
    def __init__(self, parent=None, xmlNode=None, weight=None):
        super().__init__(parent=parent)
        self.weight = weight
        if xmlNode.get('nType'):
            self.weight *= float(xmlNode.get('nType'))
        if len(xmlNode) == 2:
            leftXML, rightXML = list(xmlNode)
            self.left = TMVANode(self, leftXML, weight)
            self.right = TMVANode(self, rightXML, weight)
            self.cut_value = xmlNode.get('Cut')
            self.feature = xmlNode.get('IVar')
            self.feature_index = xmlNode.get('IVar')
            self.final = False
        elif len(xmlNode) == 0:
            self.final = True

        elif len(xmlNode) not in [0, 2]:
            raise(ValueError(f"The node {xmlNode} seems not to be a proper "
                              "binary tree node"))


def parse_model(filename, feature_names=None):
    trees = []
    with open(filename, 'r') as f:
        treeXML = ET.fromstring(f.read())

    for tree in treeXML.find('Weights'):
        firstNode = TMVANode(xmlNode=tree.find('Node'),
                weight=float(tree.get('boostWeight')))
        trees.append(firstNode)

    return trees
