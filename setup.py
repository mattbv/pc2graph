# Copyright (c) 2017, Matheus Boni Vicari, pc2graph
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
__copyright__ = "Copyright 2018-2019, pc2graph"
__credits__ = ["Matheus Boni Vicari"]
__license__ = "GPL3"
__version__ = "1.0"
__maintainer__ = "Matheus Boni Vicari"
__email__ = "matheus.boni.vicari@gmail.com"
__status__ = "Development"

from setuptools import setup, find_packages


def readme():
    with open('README.rst') as f:
        return f.read()

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name="pc2graph",
    version="1.0",
    author='Matheus Boni Vicari',
    author_email='matheus.boni.vicari@gmail.com',
    packages=find_packages(),
    entry_points={
	},
    url='https://github.com/mattbv/pc2graph',
    license='LICENSE.txt',
    description='Generates a NetworkX graph from\
 3D point clouds acquired using Terrestrial LiDAR\
 Scanners.',
    long_description=readme(),
    classifiers=['Programming Language :: Python',
                 'Topic :: Scientific/Engineering'],
    keywords='networkx graph shortest path TLS point cloud LiDAR',
    install_requires=required,
    # ...
)
