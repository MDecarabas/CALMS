import sys
import pathlib

# Appending the bluesky training path to sys.path
bluesky_path = str(pathlib.Path.home() / "bluesky_training/bluesky")
sys.path.append(bluesky_path)
print(sys.path)  # This will show all current entries in sys.path, including the newly added path

# Importing necessary modules after the path has been appended
import bluesky
import databroker
from ophyd import EpicsMotor
from bluesky.callbacks.best_effort import BestEffortCallback
from instrument.collection import *  # Assuming that 'Noisy' is imported from here

from apstools.plans.xpcs_mesh import mesh_list_grid_scan

import matplotlib
matplotlib.use('agg')

print("hello")

# # a single reading of the detector 'det'
# RE(count([Noisy]))

cat = databroker.temp().v2
RE = bluesky.RunEngine()
RE.subscribe(cat.v1.insert)
RE.subscribe(BestEffortCallback())

print("\n Loading Motors")
x_motor = EpicsMotor("eac99:m1", name="xpos", labels=("motor",))
y_motor = EpicsMotor("eac99:m2", name="ypos", labels=("motor",))
detectors = [noisy]

print("\n Motors loaded \n")

position_list_1 = [1, 2, 3]

position_list_2 = [1.0, 1.5, 2.0, 2.5, 3.0]


number_of_collection_points = 20

RE(mesh_list_grid_scan(detectors, x_motor, position_list_1, y_motor, position_list_2, number_of_collection_points = number_of_collection_points, snake_axes=True))
print("\n Big Succcesm \n")