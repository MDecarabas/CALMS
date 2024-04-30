from langchain.chat_models import ChatOpenAI
import requests
from langchain.tools import BaseTool, StructuredTool, Tool, tool
from pydantic import Extra
from typing import Optional, Type
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
import pexpect


def set_motor(
    text: str,
): 
    print("hello baby")
    return "Diffractometer Set"


diffractometer_tool = StructuredTool.from_function(
    set_motor,
    name="SetInstrument",
    description="Sets the instrument to a material's lattice. Requires the 6 lattice parameters: a,b,c,alp,bet,gam."
    + " Do not assume these parameters. Use the GetLattice tool to retrieve them."
    + " The peak parameters are supplied by the user. They are 3 integers.",
)
