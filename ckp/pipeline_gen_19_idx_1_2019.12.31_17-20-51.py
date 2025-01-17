import numpy as np
import pandas as pd
from sklearn.linear_model import RidgeCV, SGDRegressor
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline, make_union
from tpot.builtins import StackingEstimator

# NOTE: Make sure that the outcome column is labeled 'target' in the data file
tpot_data = pd.read_csv('PATH/TO/DATA/FILE', sep='COLUMN_SEPARATOR', dtype=np.float64)
features = tpot_data.drop('target', axis=1)
training_features, testing_features, training_target, testing_target = \
            train_test_split(features, tpot_data['target'], random_state=None)

# Average CV score on the training set was: -0.747194341250974
exported_pipeline = make_pipeline(
    StackingEstimator(estimator=RidgeCV()),
    SGDRegressor(alpha=0.01, eta0=0.01, fit_intercept=True, l1_ratio=0.25, learning_rate="constant", loss="epsilon_insensitive", penalty="elasticnet", power_t=0.5)
)

exported_pipeline.fit(training_features, training_target)
results = exported_pipeline.predict(testing_features)
