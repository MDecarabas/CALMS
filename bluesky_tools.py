# from langchain.chat_models import ChatOpenAI
# import requests
# from langchain.tools import BaseTool, StructuredTool, Tool, tool
# from langchain.agents import initialize_agent, AgentType

# from pydantic import Extra
# from typing import Optional, Type
# from langchain.callbacks.manager import (
#     AsyncCallbackManagerForToolRun,
#     CallbackManagerForToolRun,
# )
# import pexpect

# # import sys
# # import pathlib

# # # Appending the bluesky training path to sys.path
# # bluesky_path = str(pathlib.Path.home() / "bluesky_training/bluesky")
# # sys.path.append(bluesky_path)
# # print(sys.path)  # This will show all current entries in sys.path, including the newly added path

# # # Importing necessary modules after the path has been appended
# # import bluesky
# # import databroker
# # from ophyd import EpicsMotor
# # from bluesky.callbacks.best_effort import BestEffortCallback
# # from instrument.collection import *  # Assuming that 'Noisy' is imported from here

# # from apstools.plans.xpcs_mesh import mesh_list_grid_scan

# # import matplotlib
# # matplotlib.use('agg')

# # def set_motor(
# #     motor_name: str,
# #     ioc_name: str
# # ):

# #     motor = EpicsMotor(ioc_name, name=motor_name, labels=("motor",))
# #     print(motor)

# #     return motor

# # def assemble_plan(
# #     x_motor,
# #     y_motor
# # ):
# #     cat = databroker.temp().v2
# #     RE = bluesky.RunEngine()
# #     RE.subscribe(cat.v1.insert)
# #     RE.subscribe(BestEffortCallback())

# #     detectors = [noisy]

# #     print("\n Motors loaded \n")

# #     position_list_1 = [1, 2, 3]
# #     position_list_2 = [1.0, 1.5, 2.0, 2.5, 3.0]


# #     number_of_collection_points = 20

# #     RE(mesh_list_grid_scan(detectors, x_motor, position_list_1, y_motor, position_list_2, number_of_collection_points = number_of_collection_points, snake_axes=True))


# ##################

# class DeviceCodeGeneratorTool(BaseTool):
#     name = "device_code_generator"
#     description = "Generates Python code for devices in station 8-ID-D"

#     def generate_code(self, device_name: str, prefix: str, motors: dict):
#         code_template = """
# import logging
# from ophyd import Component as Cpt
# from ophyd import Device
# from ophyd import FormattedComponent as FCpt
# from ophyd import EpicsMotor

# logger = logging.getLogger(__name__)
# logger.info(__file__)

# class {class_name}(Device):
#     def __init__(
#         self,
#         prefix: str,
#         {motor_params},
#         *args,
#         **kwargs,
#     ):
#         # Determine the prefix for the motors
#         pieces = prefix.strip(":").split(":")
#         self.motor_prefix = ":".join(pieces[:-1])

#         {motor_assignments}

#         super().__init__(prefix, *args, **kwargs)

#     {formatted_components}

# {device_instance}
# """
#         class_name = device_name.capitalize()
#         motor_params = ", ".join([f"{motor}_motor: str" for motor in motors.keys()])
#         motor_assignments = "\n        ".join([f"self._{motor}_motor = {motor}_motor" for motor in motors.keys()])
#         formatted_components = "\n    ".join([f"{motor} = FCpt(EpicsMotor, '{{{{motor_prefix}}}}:{{{{_{motor}_motor}}}}', labels={{'motors'}})" for motor in motors.keys()])
#         device_instance_parts = [
#             f"{motor}_motor='{motor_value}'" for motor, motor_value in motors.items()
#         ]
#         device_instance = f"{device_name} = {class_name}(name='{device_name}', prefix='{prefix}', {', '.join(device_instance_parts)})"

#         return code_template.format(
#             class_name=class_name,
#             motor_params=motor_params,
#             motor_assignments=motor_assignments,
#             formatted_components=formatted_components,
#             device_instance=device_instance
#         )

#     # def _call(self, inputs):
#     #     device_name = inputs.get('device_name')
#     #     prefix = inputs.get('prefix')
#     #     motors = inputs.get('motors')
#     #     return self.generate_code(device_name, prefix, motors)


# ###############
# device_code_generator_tool = DeviceCodeGeneratorTool()

# # ophyd_motor_tool = StructuredTool.from_function(
# #     set_motor,
# #     name="set_motor",
# #     description="Creates an ophyd epics motor object. Requires the 2 parameters: motor_name, ioc_name."
# #     + " The parameters are supplied by the user. They are 2 strings.",
# # )

# # bluesky_plan_tool = StructuredTool.from_function(
# #     assemble_plan,
# #     name="assemble_plan",
# #     description="Initializes a bluesky plan. Requires the 2 parameters: x_motor, y_motor."
# #     + "Do not assume these parameters. Use the GetLattice tool to retrieve them.",
# # )

# ophyd_tool_builder = initialize_agent(
#     tools=[device_code_generator_tool],
#     agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION
# )

from typing import List
from langchain.tools import StructuredTool


def generate_device_code(prefix: str, name: str, motor_names: List[str]) -> str:
    class_name = name.capitalize()
    motor_definitions = "\n".join(
        [
            f'    {motor} = FCpt(EpicsMotor, "{{motor_prefix}}:{{_{motor}_motor}}", labels={{"motors"}})'
            for motor in motor_names
        ]
    )
    motor_init_params = ", ".join([f"{motor}_motor: str" for motor in motor_names])
    motor_init_assignments = "\n".join(
        [f"        self._{motor}_motor = {motor}_motor" for motor in motor_names]
    )

    template = f"""
from ophyd import Component as Cpt
from ophyd import Device
from ophyd import FormattedComponent as FCpt
from ophyd import EpicsMotor

class {class_name}(Device):
    def __init__(
        self,
        prefix: str,
        {motor_init_params},
        *args,
        **kwargs,
    ):
        # Determine the prefix for the motors
        pieces = prefix.strip(":").split(":")
        self.motor_prefix = ":".join(pieces[:-1])

{motor_init_assignments}

        super().__init__(prefix, *args, **kwargs)

{motor_definitions}

{name} = {class_name}(
    name="{name}",
    prefix="{prefix}",
    {", ".join([f'{motor}_motor="{motor}"' for motor in motor_names])},
)
"""
    return template


code_generator_tool = StructuredTool.from_function(
    func=generate_device_code,
    name="CodeGenerator",
    description="Generates ophyd motor device based on the provided prefix, name, and motor names."
    + " The parameters are supplied by the user. They are 3 integers."
    + "return template as thought"
)
