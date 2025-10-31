import numpy as np
from spotlightcurve.preprocess import quality_mask

def test_quality_mask_filters_outliers():
    # 99 inliers at 1, one outlier at 100
    f = np.r_[np.ones(99), 100.0]
    mask = quality_mask(f, sigma=3)  # 3-sigma clip
    assert mask[:-1].all()
    assert not mask[-1]
