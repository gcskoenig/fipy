"""Model-X Knockoff sampler based on arXiv:1610.02351.

Second-order Gaussian models are used to model the
conditional distribution.
"""
from rfi.samplers.sampler import Sampler
from rfi.samplers._helpers import sample_id, sample_perm
import rfi.utils as utils
from DeepKnockoffs import GaussianKnockoffs
import numpy as np

class GaussianSampler(Sampler):
    """
    Second order Gaussian Sampler.

    Attributes:
        see rfi.samplers.Sampler
    """

    def __init__(self, X_train):
        """Initialize Sampler with X_train and mask."""
        super().__init__(X_train)

    def __train_j(self, jj, G, verbose=True):

        G = np.array(G, dtype=np.int16)
        G_key = utils.to_key(G)
        jj_key = utils.to_key([jj])
        if verbose:
            print('Start training')
            print('G: {}, fsoi: {}'.format(G, jj))
        self._trainedGs[(jj_key, G_key)] = train_gaussian(self.X_train, jj, G)
        if verbose:
            print('Training ended. Sampler saved.')

    def train(self, J, G, verbose=True):
        """Trains sampler using dataset to resample
        variable jj relative to G.

        Args:
            J: features of interest
            G: arbitrary set of variables
            verbose: printing
        """
        try:
            for jj in J:
                self.__train_j(jj, G, verbose=verbose)
        except TypeError as te:
            self.__train_j(J, G, verbose=verbose)
            

    def sample(self, X_test, J, G, verbose=True):
        """

        """
        # initialize numpy matrix
        J = np.array(J, dtype=np.int16)
        sampled_data = np.zeros((X_test.shape[0], J.shape[0]))

        #sample
        G_key = utils.to_key(G)
        for kk in range(J.shape[0]):
            jj_key = utils.to_key([J[kk]])
            if not super().is_trained([J[kk]], G):
                print('Sampler not trained yet.')
                self.train(J[kk], G, verbose=verbose)
            sample_func = self._trainedGs[(jj_key, G_key)]
            sampled_data[:, kk] = sample_func(X_test)
        return sampled_data


# TODO(gcsk): Replace Knockoff dependency with my own conditional gaussian sampling

def train_gaussian(X_train, j, G):
    '''Training a conditional sampler under the assumption
    of gaussianity

    Args:
        G: relative feature set
        j: feature of interest
    '''
    data = np.zeros((X_train.shape[0], G.shape[0]+1))
    if j in G:
        return sample_id(j)
    elif G.size == 0:
        return sample_perm(j)
    else:
        data[:, :-1] = X_train[:, G]
        data[:, -1] = X_train[:, j]
        SigmaHat = np.cov(data, rowvar=False)
        second_order = GaussianKnockoffs(SigmaHat, mu=np.mean(data, 0))
        def sample(X_test):
            ixs = np.zeros((G.shape[0] + 1), dtype=np.int16)
            ixs[:-1] = G
            ixs[-1] = j
            knockoffs = second_order.generate(X_test[:, ixs])
            return knockoffs[:, -1]
        return sample