"""
Model 1: Gradient Boosted Decision Trees / Random Forest (Tabular Baseline)
----------------------------------------------------------------------------
Provides the non-deep-learning baseline for both lake surface area forecasting
and categorical GLOF hazard tier classification.
"""

from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
import numpy as np

class GLOFTreeBaseline:
    def __init__(self, n_estimators=100, max_depth=10, random_state=42):
        self.regressor = RandomForestRegressor(
            n_estimators=n_estimators, max_depth=max_depth, random_state=random_state, n_jobs=-1
        )
        self.classifier = RandomForestClassifier(
            n_estimators=n_estimators, max_depth=max_depth, random_state=random_state, n_jobs=-1
        )

    def fit(self, X_train, y_reg_train, y_cls_train):
        # Flatten (N, Lookback, Features) to (N, Lookback * Features)
        X_flat = X_train.reshape(X_train.shape[0], -1)
        self.regressor.fit(X_flat, y_reg_train.ravel())
        self.classifier.fit(X_flat, y_cls_train.ravel())
        return self

    def predict_area(self, X):
        X_flat = X.reshape(X.shape[0], -1)
        return self.regressor.predict(X_flat)

    def predict_risk(self, X):
        X_flat = X.reshape(X.shape[0], -1)
        return self.classifier.predict(X_flat)

    def get_feature_importances(self, feature_names=None):
        return self.regressor.feature_importances_

