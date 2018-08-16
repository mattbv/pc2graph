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
from downsampling import (downsample_cloud, upsample_cloud)
import os

if __name__ == '__main__':

    # Declaring list of files to process and output folder.
    filelist = '../data/batch/files.txt'
    out_folder = '../data/batch/'
    
    # Declaring downsample size of 10 cm.
    downsample_size = 0.1
    
    # Reading list of files to process.
    with open(filelist, 'r') as r:
        files = r.read()
    files = files.split('\n')
    files = filter(None, files)
    
    for f in files:
        # Detecting file name.
        fname = os.path.splitext(os.path.basename(f))[0]
        
        print('Processing %s' % fname)
        
        # Loading point cloud and selecting only xyz coordinates.
        point_cloud = np.loadtxt(f)
        point_cloud = point_cloud[:, :3]
        
        # Downsample point cloud to speed up processing.
        downsample_indices, downsample_nn = downsample_cloud(point_cloud,
                                                             downsample_size,
                                                             True, True)
        downsample_pc = point_cloud[downsample_indices, :3]
        
        # Growth factor. Each point adds 3 new points to graph.
        kpairs = 3
    
        # NN search of the whole point cloud. This allocates knn indices
        # for each point in order to grow the graph. The more segmented (gaps)
        # the cloud is, the larger knn has to be.
        knn = 100
    
        # Maximum distance between points. If distance > threshold, neighboring
        # point is not added to graph.
        nbrs_threshold = 0.08
    
        # When initial growth process is broken (gap in the cloud) and no
        # other point can be added, incease threshold to include missing points.
        nbrs_threshold_step = 0.02
    
        # Base/root point of the point cloud.
        base_point = np.argmin(downsample_pc[:, 2])
    
        # Generates graph from numpy array.
        G = array_to_graph(downsample_pc, base_point, kpairs, knn, nbrs_threshold,
                           nbrs_threshold_step)
    
        # Extracts shortest path info from G and generate nodes point cloud.
        nodes_ids, distance, path_list = extract_path_info(G, base_point,
                                                           return_path=True)
        
        # Upscaling the point cloud and distance values.
        nodes_ids = np.array(nodes_ids)
        # Get the upscaled set of indices for the final points.
        upscale_ids = upsample_cloud(downsample_indices[nodes_ids],
                                     downsample_nn)
        # Allocating upscale_distance. Looping over the original downsample
        # indices and distance values. This will be used to retrieve each
        # downsampled points' neighbors indices and apply the distance value
        # to them.
        upscale_distance = np.full(upscale_ids.shape[0], np.nan)
        for n, d in zip(downsample_indices[nodes_ids], distance):
            up_ids = downsample_nn[n]
            upscale_distance[up_ids] = d
        
        # Generating the upscaled cloud.
        upscale_cloud = point_cloud[upscale_ids]
        
        # Calculating difference array and preparing output point cloud.
        diff = np.abs(upscale_cloud[:, 2] - upscale_distance)
        
        # Stacking all variables and exporting.
        out_cloud = np.hstack((upscale_cloud, upscale_distance.reshape(-1, 1),
                               diff.reshape(-1, 1)))
        np.savetxt('%s%s.txt' % (out_folder, fname), out_cloud, fmt='%1.3f')