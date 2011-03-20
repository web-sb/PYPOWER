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

"""Defines constants for named column indices to bus matrix.

Some examples of usage, after defining the constants using the line above,
are:

 Pd = bus(3, PD)     # get the real power demand at bus 4
 bus(:, VMIN) = 0.95 # set the min voltage magnitude to 0.95 at all buses

The index, name and meaning of each column of the bus matrix is given
below:

columns 0-12 must be included in input matrix (in case file)
 0  BUS_I       bus number (1 to 29997)
 1  BUS_TYPE    bus type (1 = PQ, 2 = PV, 3 = ref, 4 = isolated)
 2  PD          Pd, real power demand (MW)
 3  QD          Qd, reactive power demand (MVAr)
 4  GS          Gs, shunt conductance (MW at V = 1.0 p.u.)
 5  BS          Bs, shunt susceptance (MVAr at V = 1.0 p.u.)
 6  BUS_AREA    area number, 1-100
 7  VM          Vm, voltage magnitude (p.u.)
 8  VA          Va, voltage angle (degrees)
 9  BASE_KV     baseKV, base voltage (kV)
 10 ZONE        zone, loss zone (1-999)
 11 VMAX        maxVm, maximum voltage magnitude (p.u.)
 12 VMIN        minVm, minimum voltage magnitude (p.u.)

columns 13-16 are added to matrix after OPF solution
they are typically not present in the input matrix
                (assume OPF objective function has units, u)
 13 LAM_P       Lagrange multiplier on real power mismatch (u/MW)
 14 LAM_Q       Lagrange multiplier on reactive power mismatch (u/MVAr)
 15 MU_VMAX     Kuhn-Tucker multiplier on upper voltage limit (u/p.u.)
 16 MU_VMIN     Kuhn-Tucker multiplier on lower voltage limit (u/p.u.)

additional constants, used to assign/compare values in the BUS_TYPE column
 1  PQ    PQ bus
 2  PV    PV bus
 3  REF   reference bus
 4  NONE  isolated bus

@see: U{http://www.pserc.cornell.edu/matpower/}
"""

# define bus types
PQ      = 1
PV      = 2
REF     = 3
NONE    = 4

# define the indices
BUS_I       = 0    # bus number (1 to 29997)
BUS_TYPE    = 1    # bus type
PD          = 2    # Pd, real power demand (MW)
QD          = 3    # Qd, reactive power demand (MVAr)
GS          = 4    # Gs, shunt conductance (MW at V = 1.0 p.u.)
BS          = 5    # Bs, shunt susceptance (MVAr at V = 1.0 p.u.)
BUS_AREA    = 6    # area number, 1-100
VM          = 7    # Vm, voltage magnitude (p.u.)
VA          = 8    # Va, voltage angle (degrees)
BASE_KV     = 9    # baseKV, base voltage (kV)
ZONE        = 10   # zone, loss zone (1-999)
VMAX        = 11   # maxVm, maximum voltage magnitude (p.u.)
VMIN        = 12   # minVm, minimum voltage magnitude (p.u.)

# included in opf solution, not necessarily in input
# assume objective function has units, u
LAM_P       = 13   # Lagrange multiplier on real power mismatch (u/MW)
LAM_Q       = 14   # Lagrange multiplier on reactive power mismatch (u/MVAr)
MU_VMAX     = 15   # Kuhn-Tucker multiplier on upper voltage limit (u/p.u.)
MU_VMIN     = 16   # Kuhn-Tucker multiplier on lower voltage limit (u/p.u.)
