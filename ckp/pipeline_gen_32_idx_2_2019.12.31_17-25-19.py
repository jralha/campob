import numpy as np
import pandas as pd
from sklearn.decomposition import FastICA
from sklearn.linear_model import SGDRegressor
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import Normalizer

# NOTE: Make sure that the outcome column is labeled 'target' in the data file
tpot_data = pd.read_csv('PATH/TO/DATA/FILE', sep='COLUMN_SEPARATOR', dtype=np.float64)
features = tpot_data.drop('target', axis=1)
training_features, testing_features, training_target, testing_target = \
            train_test_split(features, tpot_data['target'], random_state=None)

# Average CV score on the training set was: -0.49982454189697584
exported_pipeline = make_pipeline(
    Normalizer(norm="max"),
    FastICA(tol=0.7000000000000001),
    SGDRegressor(alpha=0.0, eta0=1.0, fit_intercept=True, l1_ratio=0.25, learning_rate="constant", loss="huber", penalty="elasticnet", power_t=50.0)
)

exported_pipeline.fit(training_features, training_target)
results = exported_pipeline.predict(testing_features)
