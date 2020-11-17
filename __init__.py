from scipy.stats import zscore
import numpy as np

def to_num(s, func):
    try:
        return func(s)
    except:
        return 0

def remove_outliers(df, cols, thres=2, positive_only=True):
    """
    Remove outliers in the DataFrame using scipy's zscore

    Parameters
    ----------
    df:
        DataFrame
    cols:
        Column names for outlier removal
    thres:
        Rows with zscore absolute value lower than thres will be considered as outliers
    positive_only:
        If True, remove negative values
    """

    for c in cols:
        df = df.loc[(df[c] > 0) & (np.abs(zscore(df[c])) < thres)] if positive_only else df.loc[np.abs(zscore(df[c])) < thres]

    return df

def normalize(a):
    s = sum(a)
    return [x / s for x in a]

def bin_grp(a, num_bins):
    """
    Group a list by equal width bins

    Parameters
    ----------
    a:
        List of values to be binned
    num_bins:
        Number of equal width bins
    """

    a = list(a)
    a.sort()

    left = min(a)
    right = max(a)

    bin_size = (right - left) / num_bins
    bins = []
    labels = []
    pt = 0

    for i in range(num_bins):
        b = []
        labels.append((left + i * bin_size, left + (i + 1) * bin_size))

        while pt < len(a) and a[pt] <= left + (i + 1) * bin_size:
            b.append(a[pt])
            pt += 1

        bins.append(b)

    return labels, bins

def bin_count(a, num_bins):
    """
    Parameters
    ----------
    a:
        List of values to be binned
    num_bins:
        Number of equal width bins
    """
    labels, bins = bin_grp(a, num_bins)

    return labels, [len(x) for x in bins]

def bin_avg(a, num_bins):
    """
    Parameters
    ----------
    a:
        List of values to be binned
    num_bins:
        Number of equal width bins
    """
    labels, bins = bin_grp(a, num_bins)

    return labels, [np.mean(x) for x in bins]
