import logging
from ophyd import Device, FormattedComponent as FCpt, EpicsMotor
from langchain.agents import initialize_agent, Tool
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
import sys
import params

import os
if params.set_visible_devices:
    os.environ["CUDA_VISIBLE_DEVICES"] = params.visible_devices

# Initialize logging
logger = logging.getLogger(__name__)
logger.info(__file__)

def create_device_class(class_name, prefix, motor_names):
    class DynamicDevice(Device):
        def __init__(self, prefix, name, *args, **kwargs):
            pieces = prefix.strip(":").split(":")
            self._motor_prefix = ":".join(pieces[:-1])
            super().__init__(prefix=prefix, name=name, *args, **kwargs)

        @property
        def motor_prefix(self):
            return self._motor_prefix
    
    components = {}
    for motor_name in motor_names:
        components[motor_name] = FCpt(EpicsMotor, "{motor_prefix}:{_motor_name}", labels={"motors"})
    
    DynamicDevice = type(class_name, (DynamicDevice,), components)
    instance = DynamicDevice(prefix=prefix, name=class_name.lower())

    return DynamicDevice, instance

def generate_class_code(class_name, prefix, motor_names):
    DynamicDeviceClass, _ = create_device_class(class_name, prefix, motor_names)
    class_code = f"""
class {class_name}(Device):
    def __init__(self, prefix, name, *args, **kwargs):
        pieces = prefix.strip(":").split(":")
        self._motor_prefix = ":".join(pieces[:-1])
        super().__init__(prefix=prefix, name=name, *args, **kwargs)

    @property
    def motor_prefix(self):
        return self._motor_prefix

"""
    for motor_name in motor_names:
        class_code += f"    {motor_name} = FCpt(EpicsMotor, \"{{{class_name.lower()}.motor_prefix}}:{{_{motor_name}}}\", labels={{\"motors\"}})\n"
    
    return class_code

# Define the agent tools
def create_class_tool(input_text):
    inputs = input_text.split(',')
    class_name = inputs[0].strip()
    prefix = inputs[1].strip()
    motor_names = [name.strip() for name in inputs[2:]]
    return generate_class_code(class_name, prefix, motor_names)

tools = [
    Tool(
        name="Create Device Class",
        func=create_class_tool,
        description="Create a new device class given class name, prefix, and motor names."
    )
]



# Initialize the agent
llm = llms.AnlLLM(params)

prompt = PromptTemplate(input_variables=["class_name", "prefix", "motor_names"], template="Generate a new class definition for {class_name} with prefix {prefix} and motors {motor_names}")
agent = initialize_agent(tools, llm, prompt)

def main():
    input_text = input("Enter class name, prefix, and motor names (comma-separated): ")
    output = agent.run(input_text)
    print("Generated Class Code:")
    print(output)

if __name__ == "__main__":
    main()
