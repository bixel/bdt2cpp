#! /usr/bin/env python3

from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
import pandas as pd
import os

from utils import prepare_test_env

scenarios = [
    {  # for "manual" debugging
        'n_estimators': 5,
        'max_depth': 2,
    },
    {  # a realisitc scenario
        'n_estimators': 100,
        'max_depth': 3,
    },
    {  # performance test
        'n_estimators': 5000,
        'max_depth': 5,
        'nthread': 4,
    },
]

X, y = make_classification(10000)
X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.7)

df_test = pd.DataFrame(X_test)
df_test['target'] = y_test

prepare_test_env()

for i, kwargs in enumerate(scenarios):
    classifier = XGBClassifier(**kwargs)
    classifier.fit(X_train, y_train)
    model_dir = os.path.join(os.path.dirname(__file__), f'build/model-{i}.txt')
    classifier.get_booster().dump_model(
        os.path.join(os.path.dirname(__file__), f'build/model-{i}.xgb'))
    probas = classifier.predict_proba(X_test)
    df_test[f'p_{i}_0'] = probas[:, 0]
    df_test[f'p_{i}_1'] = probas[:, 1]

df_test.to_csv(os.path.join(os.path.dirname(__file__),
                            'build/comparison_data.csv'))
