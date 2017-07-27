import unittest
from sklearn.datasets import make_classification
from xgboost import XGBClassifier

import bdt2cpp


class TestNode(unittest.TestCase):
    def setUp(self):
        X, y = make_classification(n_features=5, random_state=1)
        self.classifier = XGBClassifier(n_estimators=3)
        self.classifier.fit(X, y)
        self.predictions = self.classifier.predict_proba(X)
        self.model_dump = [tree.split('\n') for tree in self.classifier.booster().get_dump()]

    def test_parse_root_node(self):
        node = bdt2cpp.Node(self.model_dump[0][0])
        self.assertEqual(node.cut_value, -0.464102)
        self.assertFalse(node.weight)
        self.assertEqual(node.root, node)
        self.assertIsNone(node.parent)
        return node

    def test_parse_left_node(self):
        node = self.test_parse_root_node()
        root = node
        node.left = bdt2cpp.Node(self.model_dump[0][1], parent=node)
        node = node.left
        self.assertEqual(node.parent, root)
        self.assertFalse(node.cut_value)
        self.assertEqual(node.weight, -0.184906)
        return node


if __name__ == '__main__':
    unittest.main()
