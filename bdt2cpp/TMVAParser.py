from .Node import Node

import xml.etree.ElementTree as ET


class TMVANode(Node):
    def __init__(self, parent=None, xmlNode=None):
        super().__init__(parent=parent)
        if not parent or xmlNode.nType == 0:
            self.weight = xmlNode.boostWeight
            self.final = False
        else xmlNode and xmlNode.nType != 0:
            self.weight = self.parent.weight * xmlNode.nType
