# Copyright (c) 2018-2019, Matheus Boni Vicari, pc2graph
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
__copyright__ = "Copyright 2018-2019"
__credits__ = ["Matheus Boni Vicari"]
__license__ = "GPL3"
__version__ = "1.0.1"
__maintainer__ = "Matheus Boni Vicari"
__email__ = "matheus.boni.vicari@gmail.com"
__status__ = "Development"

from downsampling import downsample_cloud
from shortpath import array_to_graph
import numpy as np
import glob
import os

if __name__ == '__main__':
    
    try:
        import mayavi.mlab as mlab
    
        # Setting up where to save the data.
        out_dir = '../../data/test_gif/'
        out_file = 'test'
        layer_delay = 2
       
        # Setting up parameters to generate the graph.
        point_cloud = np.loadtxt('../../data/point_cloud_example.txt')
        downsample_dist = 0.05
        kpairs = 3
        knn = 100
        nbr_dist_threshold = downsample_dist * 1.5
        nbr_dist_threshold_step = 0.03
        downsample_cloud = downsample_cloud(point_cloud, downsample_dist)
        
        # Obtaining base id (lowest point in the cloud).
        base_id = np.argmin(downsample_cloud[:, 2])
        
        # Generating graph with option to return the step_register as True.
        G, step_register = array_to_graph(downsample_cloud, base_id, kpairs,
                                          knn, nbr_dist_threshold,
                                          nbr_dist_threshold_step,
                                          return_step=True)
    
    
        # Starts the iterative plotting. This will require the Mayavi package.
        iteration = 0
        mlab.figure(bgcolor=(1, 1, 1), fgcolor=(0, 0, 0))
        mlab.points3d(downsample_cloud[:, 0], downsample_cloud[:, 1],
                      downsample_cloud[:, 2], color=(0.3, 0.3, 0.3), mode='point')
        for s in np.unique(step_register):
            mask = step_register == s
            mlab.points3d(downsample_cloud[mask, 0], downsample_cloud[mask, 1],
                          downsample_cloud[mask, 2], color=(1, 0, 0), mode='point')
            mlab.savefig(out_dir + '%s.png' % iteration)
            iteration += 1
        mlab.close()
    
        # Generating the list of step images to join in a gif later.
        file_list = glob.glob('%s*.png' % out_dir)
        file_list = [os.path.basename(f) for f in file_list]
        list.sort(file_list, key=lambda x: int(os.path.basename(x).split('.png')[0]))
        with open('%simage_list.txt' % out_dir, 'w') as file:
            for item in file_list:
                file.write("%s\n" % item)
                
        # Changing directory and using ImageMagik to join all images into a gif.
        # Then, delets all unnecessary files.In the end, returns to initial
        # directory.
        cwd = os.getcwd()
        os.chdir(out_dir)
        os.system('convert -loop 0 -delay %s @image_list.txt %s.gif' % (layer_delay, out_file))
        os.remove('image_list.txt')
        for f in file_list:
            os.remove(f)
        os.chdir(cwd)
    
    except:
        print('Mayavi not installed, this example cannot run!')
        
