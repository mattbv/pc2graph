# Copyright (c) 2017, Matheus Boni Vicari, TLSeparation Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#     1. Redistributions of source code must retain the above copyright notice,
#        this list of conditions and the following disclaimer.
#
#     2. Redistributions in binary form must reproduce the above copyright
#        notice, this list of conditions and the following disclaimer in the
#        documentation and/or other materials provided with the distribution.
#
#     3. Neither the name of the Raysect Project nor the names of its
#        contributors may be used to endorse or promote products derived from
#        this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

__author__ = "Matheus Boni Vicari"
__copyright__ = "Copyright 2017, TLSeparation Project"
__credits__ = ["Matheus Boni Vicari"]
__license__ = "GPL3"
__version__ = "0.1"
__maintainer__ = "Matheus Boni Vicari"
__email__ = "matheus.boni.vicari@gmail.com"
__status__ = "Development"

import numpy as np
from shortpath import (array_to_graph, extract_path_info)


if __name__ == "__main__":

    # Loads point cloud into a numpy.ndarray (n_points x dimensions).
    point_cloud = np.loadtxt('../data/point_cloud_example.txt')

    # Growth factor. Each point adds 3 new points to graph.
    kpairs = 3

    # NN search of the whole point cloud. This allocates knn indices
    # for each point in order to grow the graph. The more segmented (gaps)
    # the cloud is, the larger knn has to be.
    knn = 100

    # Maximum distance between points. If distance > threshold, neighboring
    # point is not added to graph.
    nbrs_threshold = 0.04

    # When initial growth process is broken (gap in the cloud) and no
    # other point can be added, incease threshold to include missing points.
    nbrs_threshold_step = 0.02

    # Base/root point of the point cloud.
    base_point = np.argmin(point_cloud[:, 2])

    # Generates graph from numpy array.
    G = array_to_graph(point_cloud, base_point, kpairs, knn, nbrs_threshold,
                       nbrs_threshold_step)

    # Extracts shortest path info from G and generate nodes point cloud.
    nodes_ids, distance, path_list = extract_path_info(G, base_point,
                                                       return_path=True)
    nodes = point_cloud[nodes_ids]
