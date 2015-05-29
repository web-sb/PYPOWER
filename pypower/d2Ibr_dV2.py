# Copyright 1996-2015 PSERC. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

"""Computes 2nd derivatives of complex branch current w.r.t. voltage.
"""

from numpy import ones, arange
from scipy.sparse import csr_matrix as sparse


def d2Ibr_dV2(Ybr, V, lam):
    """Computes 2nd derivatives of complex branch current w.r.t. voltage.

    Returns 4 matrices containing the partial derivatives w.r.t. voltage
    angle and magnitude of the product of a vector LAM with the 1st partial
    derivatives of the complex branch currents. Takes sparse branch admittance
    matrix C{Ybr}, voltage vector C{V} and C{nl x 1} vector of multipliers
    C{lam}. Output matrices are sparse.

    For more details on the derivations behind the derivative code used
    in PYPOWER information, see:

    [TN2]  R. D. Zimmerman, I{"AC Power Flows, Generalized OPF Costs and
    their Derivatives using Complex Matrix Notation"}, MATPOWER
    Technical Note 2, February 2010.
    U{http://www.pserc.cornell.edu/matpower/TN2-OPF-Derivatives.pdf}

    @author: Ray Zimmerman (PSERC Cornell)
    @author: Richard Lincoln
    """
    nb = len(V)
    ib = arange(nb)
    diaginvVm = sparse((ones(nb) / abs(V), (ib, ib)))

    Haa = sparse((-(Ybr.T * lam) * V, (ib, ib)))
    Hva = -1j * Haa * diaginvVm
    Hav = Hva.copy()
    Hvv = sparse((nb, nb))

    return Haa, Hav, Hva, Hvv
