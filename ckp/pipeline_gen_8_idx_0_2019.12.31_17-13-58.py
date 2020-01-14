import numpy as np
import pandas as pd
from sklearn.linear_model import SGDRegressor
from sklearn.model_selection import train_test_split

# NOTE: Make sure that the outcome column is labeled 'target' in the data file
tpot_data = pd.read_csv('PATH/TO/DATA/FILE', sep='COLUMN_SEPARATOR', dtype=np.float64)
features = tpot_data.drop('target', axis=1)
training_features, testing_features, training_target, testing_target = \
            train_test_split(features, tpot_data['target'], random_state=None)

# Average CV score on the training set was: -1.1537199612882436
exported_pipeline = SGDRegressor(alpha=0.01, eta0=0.1, fit_intercept=True, l1_ratio=0.5, learning_rate="constant", loss="huber", penalty="elasticnet", power_t=0.0)

exported_pipeline.fit(training_features, training_target)
results = exported_pipeline.predict(testing_features)