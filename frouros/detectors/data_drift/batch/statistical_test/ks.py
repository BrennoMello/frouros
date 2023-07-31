"""KSTest (Kolmogorov-Smirnov test) module."""

from typing import Optional, List, Union

import numpy as np  # type: ignore
from scipy.stats import ks_2samp  # type: ignore

from frouros.callbacks.batch.base import BaseCallbackBatch
from frouros.detectors.data_drift.base import NumericalData, UnivariateData
from frouros.detectors.data_drift.batch.statistical_test.base import (
    BaseStatisticalTest,
    StatisticalResult,
)


class KSTest(BaseStatisticalTest):
    """KSTest (Kolmogorov-Smirnov test) [massey1951kolmogorov]_ detector.

    :param callbacks: callbacks, defaults to None
    :type callbacks: Optional[Union[BaseCallbackBatch, List[BaseCallbackBatch]]]
    :param kwargs: additional keyword arguments to pass to scipy.stats.ks_2samp
    :type kwargs: Dict[str, Any]

    :References:

    .. [massey1951kolmogorov] Massey Jr, Frank J.
        "The Kolmogorov-Smirnov test for goodness of fit."
        Journal of the American statistical Association 46.253 (1951): 68-78.

    :Example:

    >>> from frouros.detectors.data_drift import KSTest
    >>> import numpy as np
    >>> np.random.seed(seed=31)
    >>> X = np.random.normal(loc=0, scale=1, size=100)
    >>> Y = np.random.normal(loc=1, scale=1, size=100)
    >>> detector = KSTest()
    >>> _ = detector.fit(X=X)
    >>> detector.compare(X=Y)[0]
    StatisticalResult(statistic=0.55, p_value=3.0406585087050305e-14)
    """

    def __init__(
        self,
        callbacks: Optional[Union[BaseCallbackBatch, List[BaseCallbackBatch]]] = None,
        **kwargs,
    ) -> None:
        super().__init__(
            data_type=NumericalData(),
            statistical_type=UnivariateData(),
            callbacks=callbacks,
        )
        self.kwargs = kwargs

    def _statistical_test(
        self, X_ref: np.ndarray, X: np.ndarray, **kwargs  # noqa: N803
    ) -> StatisticalResult:
        test = ks_2samp(
            data1=X_ref,
            data2=X,
            alternative=self.kwargs.get("alternative", "two-sided"),
            method=self.kwargs.get("method", "auto"),
        )
        test = StatisticalResult(statistic=test.statistic, p_value=test.pvalue)
        return test
