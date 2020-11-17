"""Explanations are the output of Explainers.

Aggregated or obser-wise wise results can be
accessed. Plotting functionality is available.
"""
import numpy as np

class Explanation():
    """Stores and provides access to results from Explainer.

    Aggregated as well as observation-wise results are stored.
    Plotting functionality is available.

    Attributes:
        fsoi: Features of interest.
        lss: losses on perturbed (# fsoi, # runs, # observations)
        ex_name: Explanation description
        fsoi_names: FSOI names
    """

    def __init__(self, fsoi, lss, fs_names, ex_name=None):
        """Inits Explainer with model, mask and potentially sampler and loss"""
        self.fsoi = fsoi # TODO evaluate, do I need to make a copy?
        self.lss = lss # TODO evaluate, do I need to make a copy?
        self.fs_names = fs_names
        if self.fs_names is None:
            self.fs_names = fsoi

    def mean_rfis(self):
        """Computes Mean RFI over all runs

        Returns:
            A np.array with the relative feature importance values for
            features of interest.
        """
        return self.fs_names[self.fsoi], np.mean(np.mean(self.lss, axis=2), axis=1)