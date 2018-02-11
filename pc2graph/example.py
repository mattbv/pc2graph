# Copyright (c) 2017, Matheus Boni Vicari, TLSeparation Project
# All rights reserved.
#
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

__author__ = "Matheus Boni Vicari"
__copyright__ = "Copyright 2017"
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
