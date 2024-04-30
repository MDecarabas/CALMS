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
    a: float,
    b: float,
    c: float,
    alpha: float,
    beta: float,
    gamma: float,
    peak: list[int],
):
    if len(peak) != 3:
        return "Peak parameters were incorrect. Instrument was NOT set"

    print(a, b, c, alpha, beta, gamma)
    print(peak[0], peak[1], peak[2])

    return "Diffractometer Set"


diffractometer_tool = StructuredTool.from_function(
    set_motor,
    name="SetInstrument",
    description="Sets the instrument to a material's lattice. Requires the 6 lattice parameters: a,b,c,alp,bet,gam."
    + " Do not assume these parameters. Use the GetLattice tool to retrieve them."
    + " The peak parameters are supplied by the user. They are 3 integers.",
)
