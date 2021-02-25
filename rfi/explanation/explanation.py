"""Explanations are the output of Explainers.

Aggregated or obser-wise wise results can be
accessed. Plotting functionality is available.
"""
# import numpy as np
import rfi.plots._barplot as _barplot
import pandas as pd
# import itertools
# import rfi.utils as utils


class Explanation:
    """Stores and provides access to results from Explainer.

    Aggregated as well as observation-wise results are stored.
    Plotting functionality is available.

    Attributes:
        fsoi: Features of interest (column names)
        scores: DataFrame with Multiindex (sample, i)
            and one column per feature of interest
            deprecated: np.array with (nr_fsoi, nr_runs, nr_obs)
        ex_name: Explanation description
    """

    def __init__(self, fsoi, scores, ex_name=None):
        """Inits Explanation with fsoi indices, fsoi names, """
        self.fsoi = fsoi  # TODO evaluate, do I need to make a copy?
        self.scores = scores  # TODO evaluate, do I need to make a copy?
        if ex_name is None:
            self.ex_name = 'Unknown'

    def _check_shape(self):
        """Checks whether the array confirms the
        specified shape (3 dimensional).
        Cannot tell whether the ordering
        (nr_fsoi, nr_runs, nr_obs) is correct.
        """
        raise NotImplementedError('Check shape has to be '
                                  'updated for Data Frame.')
        # if len(self.lss.shape) != 3:
        #     raise RuntimeError('.lss has shape {self.lss.shape}.'
        #                        'Expected 3-dim.')

    def fi_vals(self):
        """ Computes the sample-wide RFI for each run

        Returns:
            pd.DataFrame with index: sample and fsoi as columns
        """
        # self._check_shape()
        # arr = np.mean(self.lss, axis=(2))
        # if return_np:
        #     return arr
        # else:
        #     runs = range(arr.shape[1])
        #     index = utils.create_multiindex(['feature', 'run'],
        #                                     [self.fsoi_names, runs])
        #     arr = arr.reshape(-1)
        #     df = pd.DataFrame(arr, index=index, columns=['importance'])
        # return df
        df = self.scores.mean(level='sample')
        return df

    def fi_means_stds(self):
        """Computes Mean RFI over all runs

        Returns:
            A pd.DataFrame with the relative feature importance value for
            features of interest.
        """
        # self._check_shape()
        # means = np.mean(self.lss, axis=(2, 1))
        # stds = np.std(np.mean(self.lss, axis=2), axis=(1))
        # arr = np.array([means, stds]).T
        # df = pd.DataFrame(arr,
        #                   index=self.fsoi_names,
        #                   columns=['mean', 'std'])
        df = pd.DataFrame(self.scores.mean(), columns=['mean'])
        df['std'] = self.scores.std()
        df.index.set_names(['feature'], inplace=True)
        return df

    def hbarplot(self, ax=None, figsize=None):
        return _barplot.fi_sns_hbarplot(self, ax=ax, figsize=figsize)
