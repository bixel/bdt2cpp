from sklearn.datasets import make_classification
from xgboost import XGBClassifier
import numpy as np

from bdt2cpp.XGBoostParser import XGBoostNode


class TestNode:
    @classmethod
    def setup_class(self):
        X, y = make_classification(n_features=5, random_state=1)
        self.classifier = XGBClassifier(n_estimators=3)
        self.classifier.fit(X, y)
        self.predictions = self.classifier.predict_proba(X)
        print(self.classifier.get_booster().get_dump())
        self.model_dump = [tree.split('\n') for tree in self.classifier.get_booster().get_dump()]

    def test_parse_root_node(self):
        node = XGBoostNode(line=self.model_dump[0][0])
        assert np.equal(node.cut_value, -0.464102179)
        assert not node.weight
        assert node.root == node
        assert node.parent is None
        return node

    def test_parse_left_node(self):
        node = self.test_parse_root_node()
        root = node
        node.left = XGBoostNode(line=self.model_dump[0][1], parent=node)
        node = node.left
        assert node.parent == root
        assert not node.cut_value
        assert np.equal(node.weight, -0.554717004)
