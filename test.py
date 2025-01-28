from instrument.startup import *

# Define the grid scan parameters
x_start, x_stop, y_start, y_stop = -10, 10, -10, 10
x_num, y_num = 100, 100  # Number of steps in x and y

# Perform a grid scan
RE(bp.grid_scan([sim_det], m1, x_start, x_stop, x_num, m2, y_start, y_stop, y_num, snake_axes=True))
