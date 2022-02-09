"""
==================================
   Convex Optimization Project
==================================
"""

import numpy as np
from math import sqrt
from scipy.stats import ortho_group


EPSILON = 1e-3
DELTA = 1e-6


def newton(S, x, E_ii, alpha=0.1, beta=0.5):
    e_i = x

    f = lambda l: l.T @ S @ l - 2 * np.log(l[0])
    g = lambda l: 2 * (S @ l - (1/l[0])*e_i)
    H = lambda l: 2 * (S + (1/(l[0]**2)) * E_ii)

    j = 0
    while True:
        grad = g(x)
        p_inv_H = np.linalg.pinv(H(x), hermitian=True)
        step = p_inv_H @ grad
        mu = sqrt(grad.T @ step)
        if mu / 2 <= EPSILON:
            return x

        # backtracking line search
        t = 1
        while f(x - t * p_inv_H @ grad) > f(x) - alpha * t * (mu**2):
            t *= beta
        x = x - t * step


def solve(S, k):
    """
    :param S: a PSD matrix
    :param k: an integer (bandwidth)
    :return: K - a k-band PSD matrix which minimizes the objective: Tr(SK)-log(|K|)
    """

    # Initial matrix - unit matrix
    n = len(S)

    # Initial vector
    e_i = np.zeros(k + 1)
    e_i[0] = 1

    E_ii = np.zeros((n, n))

    L = np.zeros((n, n))

    i = 0
    while i < n - k - 1:
        E_ii[i][i] = 1
        E = np.array(E_ii[i:i+k+1, i:i+k+1])
        S_i = np.array(S[i:i+k+1, i:i+k+1])
        L[i:i+k+1, i] = newton(S_i, e_i, E)
        i += 1

    r = 0
    while r <= k:
        e_i = np.zeros(k + 1 - r)
        e_i[0] = 1
        E_ii[i][i] = 1
        E = np.array(E_ii[i:i + k + 1 - r, i:i + k + 1 - r])
        S_i = np.array(S[i:i + k + 1 - r, i:i + k + 1 - r])
        L[i:i + k + 1 - r, i] = newton(S_i, e_i, E)
        i += 1
        r += 1

    K = L @ L.T

    return K


def random_psd(n):
    U = ortho_group.rvs(n)
    sin = np.random.normal(size=n)
    D = np.diag(sin ** 2)

    S = U.T @ D @ U

    assert (np.linalg.eigvals(S) > 0).all()

    return S


if __name__ == "__main__":
    S = random_psd(50)

    S1 = np.array([[0.152, -0.07975561, -0.05406262, 0.05926752],
                   [-0.07975561, 0.1032427, 0.03401931, -0.03794308],
                   [-0.05406262, 0.03401931, 0.06722056, 0.01723591],
                   [0.05926752, -0.03794308, 0.01723591, 0.0823307]])

    S2 = np.array([[0.17653648, 0.14606434, -0.03639839, 0.03938153, -0.15881158],
                   [0.14606434, 0.37884584, 0.06454572, 0.0905522, -0.16675416],
                   [-0.03639839, 0.06454572, 0.20423515, 0.12143917, 0.01075414],
                   [0.03938153, 0.0905522, 0.12143917, 0.68232489, -0.46468619],
                   [-0.15881158, -0.16675416, 0.01075414, -0.46468619, 0.51141915]])

    S3 = np.array([[0.41904335, 0.00178428, -0.03600531, -0.15406546],
                   [0.00178428, 0.49426407, -0.27000283, 0.09261175],
                   [-0.03600531, -0.27000283, 0.23902846, 0.10785086],
                   [-0.15406546, 0.09261175, 0.10785086, 0.41644895]])

    K = solve(S, 10)
    print(K)

