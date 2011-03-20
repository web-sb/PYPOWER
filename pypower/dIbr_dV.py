# Copyright (C) 1996-2011 Power System Engineering Research Center (PSERC)
# Copyright (C) 2010-2011 Richard Lincoln <r.w.lincoln@gmail.com>
#
# PYPOWER is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 3 of the License,
# or (at your option) any later version.
#
# PYPOWER is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PYPOWER. If not, see <http://www.gnu.org/licenses/>.

from scipy.sparse import csr_matrix

def dIbr_dV(branch, Yf, Yt, V):
    """Computes partial derivatives of branch currents w.r.t. voltage.

    Returns four matrices containing partial derivatives of the complex
    branch currents at "from" and "to" ends of each branch w.r.t voltage
    magnitude and voltage angle respectively (for all buses). If YF is a
    sparse matrix, the partial derivative matrices will be as well. Optionally
    returns vectors containing the currents themselves. The following
    explains the expressions used to form the matrices:

    If = Yf * V

    Partials of V, Vf & If w.r.t. voltage angles
        dV/dVa  = j * diag(V)
        dVf/dVa = sparse(1:nl, f, j * V(f)) = j * sparse(1:nl, f, V(f))
        dIf/dVa = Yf * dV/dVa = Yf * j * diag(V)

    Partials of V, Vf & If w.r.t. voltage magnitudes
        dV/dVm  = diag(V./abs(V))
        dVf/dVm = sparse(1:nl, f, V(f)./abs(V(f))
        dIf/dVm = Yf * dV/dVm = Yf * diag(V./abs(V))

    Derivations for "to" bus are similar.

    @return: The partial derivatives of branch currents w.r.t. voltage
             magnitude and voltage angle.
    @see: U{http://www.pserc.cornell.edu/matpower/}
    """
    i = range(len(V))

    Vnorm = V / abs(V)
    diagV = csr_matrix((V, (i, i)))
    diagVnorm = csr_matrix((Vnorm, (i, i)))
    dIf_dVa = Yf * 1j * diagV
    dIf_dVm = Yf * diagVnorm
    dIt_dVa = Yt * 1j * diagV
    dIt_dVm = Yt * diagVnorm

    # Compute currents.
    If = Yf * V
    It = Yt * V

    return dIf_dVa, dIf_dVm, dIt_dVa, dIt_dVm, If, It
