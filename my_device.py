
from ophyd import Component as Cpt
from ophyd import Device
from ophyd import FormattedComponent as FCpt
from ophyd import EpicsMotor

class My_device(Device):
    def __init__(
        self,
        prefix: str,
        m1_motor: str, m2_motor: str, m3_motor: str,
        *args,
        **kwargs,
    ):
        # Determine the prefix for the motors
        pieces = prefix.strip(":").split(":")
        self.motor_prefix = ":".join(pieces[:-1])

        self._m1_motor = m1_motor
        self._m2_motor = m2_motor
        self._m3_motor = m3_motor

        super().__init__(prefix, *args, **kwargs)

    m1 = FCpt(EpicsMotor, "{motor_prefix}:{_m1_motor}", labels={"motors"})
    m2 = FCpt(EpicsMotor, "{motor_prefix}:{_m2_motor}", labels={"motors"})
    m3 = FCpt(EpicsMotor, "{motor_prefix}:{_m3_motor}", labels={"motors"})

my_device = My_device(
    name="my_device",
    prefix="8iddSoft:CR8-D1:US",
    m1_motor="m1", m2_motor="m2", m3_motor="m3",
)
