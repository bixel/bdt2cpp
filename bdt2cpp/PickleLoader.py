import pickle
import tempfile
import os


from .XGBoostParser import parse_model as parse_model_xgb


def load_model(filename, feature_names=None):
    with open(filename, 'rb') as f:
        model = pickle.load(f)

    _, tmp = tempfile.mkstemp(text=True)
    model.get_booster().dump_model(tmp)

    trees =  parse_model_xgb(tmp, model.get_booster().feature_names)

    os.remove(tmp)

    return trees
