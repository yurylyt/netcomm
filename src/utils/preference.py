import numpy as np


def uncertainty(m):
    return np.array(m * [1.0 / m], float)


def normalized_entropy(w):
    """
    the normalised entropy of distribution 'w'
    entropy is the highest (1.0 normalized) when every choice can occur with the same probability (aka uncertainty)
    it is the lowest (0.0) when probability is 1.0 for one of the choices
    """
    h = float(0)
    for p in w:
        if p:
            h -= p * np.log2(p)
    # For array size == 2 max_enthropy is non-essential, as log2(2) == 1
    max_enthropy = np.log2(len(w))
    return h / max_enthropy if max_enthropy > 0 else 0
