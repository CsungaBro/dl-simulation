import os
print("PYTHONPATH:", os.environ.get('PYTHONPATH'))
print("PATH:", os.environ.get('PATH'))

import igl
# import scipy as sp
# import numpy as np
from meshplot import plot, subplot, interact, offline


mesh_path = "output\k_files\sim_0_120x120x27.5_R6.5\pls_1.stl"

v, f = igl.read_triangle_mesh(mesh_path)
k = igl.gaussian_curvature(v, f)
offline()
plot(v, f, k)