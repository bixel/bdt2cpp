#! /usr/bin/env python3

from sklearn.datasets import make_classification
from sklearn.cross_validation import train_test_split
from xgboost import XGBClassifier
import pandas as pd

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

for i, kwargs in enumerate(scenarios):
    classifier = XGBClassifier(**kwargs)
    classifier.fit(X_train, y_train)
    classifier.booster().dump_model(f'model-{i}.txt')
    probas = classifier.predict_proba(X_test)
    df_test[f'p_{i}_0'] = probas[:, 0]
    df_test[f'p_{i}_1'] = probas[:, 1]

df_test.to_csv('comparison_data.csv')
