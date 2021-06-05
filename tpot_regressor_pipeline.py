import numpy as np
import pandas as pd
from sklearn.cluster import FeatureAgglomeration
from sklearn.kernel_approximation import Nystroem
from sklearn.linear_model import RidgeCV, SGDRegressor
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline, make_union
from tpot.builtins import StackingEstimator
from tpot.export_utils import set_param_recursive

# NOTE: Make sure that the outcome column is labeled 'target' in the data file
tpot_data = pd.read_csv('PATH/TO/DATA/FILE', sep='COLUMN_SEPARATOR', dtype=np.float64)
features = tpot_data.drop('target', axis=1)
training_features, testing_features, training_target, testing_target = \
            train_test_split(features, tpot_data['target'], random_state=42)

# Average CV score on the training set was: -5.853055578955521
exported_pipeline = make_pipeline(
    make_union(
        StackingEstimator(estimator=RidgeCV()),
        make_pipeline(
            FeatureAgglomeration(affinity="manhattan", linkage="complete"),
            Nystroem(gamma=0.30000000000000004, kernel="sigmoid", n_components=5)
        )
    ),
    FeatureAgglomeration(affinity="cosine", linkage="average"),
    SGDRegressor(alpha=0.0, eta0=0.01, fit_intercept=False, l1_ratio=1.0, learning_rate="invscaling", loss="epsilon_insensitive", penalty="elasticnet", power_t=100.0)
)
# Fix random state for all the steps in exported pipeline
set_param_recursive(exported_pipeline.steps, 'random_state', 42)

exported_pipeline.fit(training_features, training_target)
results = exported_pipeline.predict(testing_features)
