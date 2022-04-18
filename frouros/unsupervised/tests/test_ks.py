"""Test unsupervised Kolmogorov-Smirnov test (KS) module."""

from typing import Tuple

from sklearn.linear_model import LogisticRegression  # type: ignore
from sklearn.pipeline import Pipeline  # type: ignore
from sklearn.preprocessing import StandardScaler  # type: ignore
import numpy as np  # type: ignore

from frouros.unsupervised.ks import KSTest


def test_feature_detector(dataset: Tuple[np.array, np.array, np.array]) -> None:
    """Test feature detector.

    :param dataset: Elec2 raw dataset
    :type dataset: Tuple[numpy.array, numpy.array, numpy.array]
    """
    X_ref, y_ref, X_test = dataset  # noqa: N806

    detector = KSTest()

    pipe = Pipeline(
        [
            ("scaler", StandardScaler()),
            ("detector", detector),
            ("model", LogisticRegression(solver="lbfgs", max_iter=1000)),
        ]
    )

    pipe.fit(X=X_ref, y=y_ref)

    _ = pipe.predict(X=np.array([*X_test]).reshape(1, -1))
    _ = pipe["detector"].test  # pylint: disable=E1101
