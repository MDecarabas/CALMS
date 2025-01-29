from instrument.startup import *

# Define the 2D grid scan using the available motors and detector
grid_scan_plan = bp.grid_scan(
    [sim_det],
    m1, -10, 10, 10,
    m2, -10, 10, 10,
    snake_axes=False,
    md={'plan_name': '2d_grid_scan'}
)

# Execute the plan
RE(grid_scan_plan)
