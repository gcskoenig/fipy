import numpy as np

from rfi.backend.causality.dags import DirectedAcyclicGraph
from rfi.backend.causality.sem import LinearGaussianNoiseSEM
from rfi.examples import SyntheticExample

sigma_low = 0.3
sigma_medium = .5
sigma_high = 1


"""
EXAMPLE 1: CONFOUNDING

Order: C, X_1, X_2, X_3, Y
"""
confounding2 = SyntheticExample(
    name='confounding2',
    sem=LinearGaussianNoiseSEM(
            dag=DirectedAcyclicGraph(
                adjacency_matrix=np.array([[0, 0, 1, 1, 1],
                                           [0, 0, 0, 0, 1],
                                           [0, 0, 0, 0, 1],
                                           [0, 0, 0, 0, 0],
                                           [0, 0, 0, 0, 0]]),
                var_names=['c', 'x1', 'x2', 'x3', 'y']
            ),
            coeff_dict={'x2': {'c': 1.0}, 'x3': {'c': 1.0}, 'y': {'x1': 1.0, 'x2': 1.0, 'c': 1.0}},
            noise_std_dict={'c': sigma_high, 'x1': sigma_high, 'x2': sigma_high, 'x3': sigma_medium, 'y': sigma_medium}
        )
)

"""
EXAMPLE 2: CHAIN with multiple paths

Order: X_1, X_2, X_3, X_4, Y
"""
chain2 = SyntheticExample(
    name='chain2',
    sem=LinearGaussianNoiseSEM(
        dag=DirectedAcyclicGraph(
            adjacency_matrix=np.array([[0, 1, 0, 1, 0],
                                       [0, 0, 1, 0, 0],
                                       [0, 0, 0, 0, 1],
                                       [0, 0, 0, 0, 1],
                                       [0, 0, 0, 0, 0]]),
            var_names=['x1', 'x2', 'x3', 'x4', 'y']
        ),
        coeff_dict={'x2': {'x1': 1.0}, 'x3': {'x2': 1.0}, 'x4': {'x1': 1.0}, 'y': {'x3': 1.0, 'x4': 1.0}},
        noise_std_dict={'x1': sigma_high, 'x2': sigma_high, 'x3': sigma_low, 'x4': sigma_high, 'y': sigma_medium}
    )
)