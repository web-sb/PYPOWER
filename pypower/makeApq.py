# Copyright (C) 1996-2011 Power System Engineering Research Center
# Copyright (C) 2010-2011 Richard Lincoln
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Construct linear constraints for generator capability curves.
"""

from numpy import array, linalg, zeros, arange, r_, c_
from numpy import flatnonzero as find
from scipy.sparse import csr_matrix as sparse

from idx_gen import PC1, PC2, QC1MIN, QC1MAX, QC2MIN, QC2MAX

from hasPQcap import hasPQcap


def makeApq(baseMVA, gen):
    """Construct linear constraints for generator capability curves.

    Constructs the parameters for the following linear constraints
    implementing trapezoidal generator capability curves, where
    C{Pg} and C{Qg} are the real and reactive generator injections::

        Apqh * [Pg, Qg] <= ubpqh
        Apql * [Pg, Qg] <= ubpql

    C{data} constains additional information as shown below.

    Example::
        Apqh, ubpqh, Apql, ubpql, data = makeApq(baseMVA, gen)

        data['h']      [Qc1max-Qc2max, Pc2-Pc1]
        data['l']      [Qc2min-Qc1min, Pc1-Pc2]
        data['ipqh']   indices of gens with general PQ cap curves (upper)
        data['ipql']   indices of gens with general PQ cap curves (lower)
    """
    data = {}
    ## data dimensions
    ng = gen.shape[0]      ## number of dispatchable injections

    ## which generators require additional linear constraints
    ## (in addition to simple box constraints) on (Pg,Qg) to correctly
    ## model their PQ capability curves
    ipqh = find( hasPQcap(gen, 'U') )
    ipql = find( hasPQcap(gen, 'L') )
    npqh = ipqh.shape[0]   ## number of general PQ capability curves (upper)
    npql = ipql.shape[0]   ## number of general PQ capability curves (lower)

    ## make Apqh if there is a need to add general PQ capability curves
    ## use normalized coefficient rows so multipliers have right scaling
    ## in $$/pu
    if npqh > 0:
        data["h"] = c_[gen[ipqh, QC1MAX] - gen[ipqh, QC2MAX],
                       gen[ipqh, PC2] - gen[ipqh, PC1]]
        ubpqh = data["h"][:, 0] * gen[ipqh, PC1] + \
                data["h"][:, 1] * gen[ipqh, QC1MAX]
        for i in range(npqh):
            tmp = linalg.norm(data["h"][i, :])
            data["h"][i, :] = data["h"][i, :] / tmp
            ubpqh[i] = ubpqh[i] / tmp
        Apqh = sparse((data["h"].flatten('F'),
                       (r_[arange(npqh), arange(npqh)], r_[ipqh, ipqh+ng])),
                      (npqh, 2*ng))
        ubpqh = ubpqh / baseMVA
    else:
        data["h"] = array([])
        Apqh  = zeros((0, 2*ng))
        ubpqh = array([])

    ## similarly Apql
    if npql > 0:
        data["l"] = c_[gen[ipql, QC2MIN] - gen[ipql, QC1MIN],
                       gen[ipql, PC1] - gen[ipql, PC2]]
        ubpql = data["l"][:, 0] * gen[ipql, PC1] + \
                data["l"][:, 1] * gen[ipql, QC1MIN]
        for i in range(npql):
            tmp = linalg.norm(data["l"][i, :])
            data["l"][i, :] = data["l"][i, :] / tmp
            ubpql[i] = ubpql[i] / tmp
        Apql = sparse((data["l"].flatten('F'),
                       (r_[arange(npql), arange(npql)], r_[ipql, ipql+ng])),
                      (npql, 2*ng))
        ubpql = ubpql / baseMVA
    else:
        data["l"] = array([])
        Apql  = zeros((0, 2*ng))
        ubpql = array([])

    data["ipql"] = ipql
    data["ipqh"] = ipqh

    return Apqh, ubpqh, Apql, ubpql, data
