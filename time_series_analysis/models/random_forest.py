"""
Model 1: Random Forest Regressor (Classical Machine Learning Baseline)
-----------------------------------------------------------------------
A non-deep-learning ensemble of decision trees. It establishes the baseline
performance to evaluate whether deep neural networks are justified.
"""

from sklearn.ensemble import RandomForestRegressor
import numpy as np

class GlacierRandomForest:
    def __init__(self, n_estimators=100, max_depth=12, random_state=42):
        self.model = RandomForestRegressor(
            n_estimators=n_estimators,
            max_depth=max_depth,
            random_state=random_state,
            n_jobs=-1
        )

    def fit(self, X_train, y_train):
        self.model.fit(X_train, y_train)
        return self

    def predict(self, X):
        return self.model.predict(X)

    def get_feature_importances(self, feature_names=None):
        importances = self.model.feature_importances_
        if feature_names is not None:
            return dict(sorted(zip(feature_names, importances), key=lambda x: x[1], reverse=True))
        return importances

