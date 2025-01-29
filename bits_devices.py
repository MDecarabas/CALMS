"""
Sample Motors
"""

from ophyd import EpicsMotor, Component, EpicsSignal

class MyEpicsMotor(EpicsMotor):
    steps_per_revolution = Component(EpicsSignal, ".SREV", kind="omitted")

m1 = MyEpicsMotor("eac99:m1", name="m1", labels=("motor",))
m2 = MyEpicsMotor("eac99:m2", name="m2", labels=("motor",))


from ophyd.sim import noisy_det as sim_det # This is the detector you should use
