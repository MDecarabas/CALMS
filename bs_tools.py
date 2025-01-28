
# from langchain.chat_models import ChatOpenAI
import requests
from langchain.tools import BaseTool, StructuredTool#, Tool, tool
from pydantic import Extra
from typing import Optional, Type
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
import pexpect
import os
import subprocess
import params
import params
from IPython import embed



"""
===============================
Python Execution Tools
===============================
"""

def launch_ipython():
    """
    Launches an IPython terminal.
    """
    print("Launching IPython terminal...")
    embed()

def exec_cmd(py_str: str):
    """
    Placeholder for the function. While in testing, just keeping it as a print statement
    """
    print(py_str)
    
    return "Command Executed"


def lint_cmd(py_str: str, lint_fp, py_pfx = None): # = 'agent_scripts/tmp_lint.py'
    """
    Helper function to enable linting.
    Creates a file, prepends text to it, lints it, then removes the file.
        py_str: string to lint
        py_pfx: prefix to add to string. Used if appending py_str to an existing python file
    """
    with open(lint_fp, 'w') as lint_file:
        if py_pfx is not None:
            lint_file.write(py_pfx)
            lint_file.write("\n")
        lint_file.write(py_str)


    # Pylint's internal reporter API fails on so just use subprocess which seesm to be more reliable
    result = subprocess.run([r"c:/Users/Public/robot/polybot-env/python.exe", "-m", "pylint", lint_fp, "-d R,C,W"], stdout=subprocess.PIPE)
    
    #"C:\Users\cnmuser\.conda\envs\calms\python.exe"
    result_str = result.stdout.decode('utf-8')

    with open(lint_fp, 'w') as lint_file:
        pass
    # os.remove(lint_fp)

    result_str_split = result_str.split('\n')
    result_str = '\n'.join(result_str_split[1:])

    return result_str

def filter_pylint_lines(lint_output, start_ln):
    """
    Filter out the pylint lines that are not needed for the output
    """
    filtered_ouput = []
    for line in lint_output.split('\n'):
        if line.startswith("*********"):
            filtered_ouput.append(line)

        line_split = line.split(':') 
        if len(line_split) > 1:
            if line_split[1].isdigit():
                if int(line.split(':')[1]) > start_ln:
                    filtered_ouput.append(line)

    return '\n'.join(filtered_ouput)

"""
===============================
Bluesky Tools
===============================
"""
# filepath: /Users/ecodrea/CALMS/bot_tools.py
from langchain.tools import StructuredTool
# from ipython_tool import launch_ipython

# exec_ipython_tool = StructuredTool.from_function(launch_ipython,
#                                                  name="LaunchIPython",
#                                                  description="Launches an IPython terminal for interactive use.")

# exec_polybot_tool = StructuredTool.from_function(polybot_exec_cmd,
#                                             name="WritePython",
#                                             description="Takes in a python string and execs it in the environment described by the script."
#                                             + "The script will contain objects and functions used to interact with the instrument. "
#                                             + "Here are some rules to follow: \n"
#                                             + "Before running the experiment create a new python file with all the library imports (robotics, loca, rack_status, proc, pandas, etc.) or any other list that is required."
#                                             + "Check if the requested polymer is available in the rack_status and then directly proceed with the experimental excecution"
#                                             + "Some useful commands and instructions are provided below \n\n" + POLYBOT_FILE_FILTER)
                                            

# """
# ===============================
# Polybot Tools
# ===============================
# """

# def polybot_exec_cmd(py_str: str):

#     file_path = POLYBOT_RUN_FILE_PATH
    
#     # Write the command to the file
#     with open(file_path, 'a') as file:
#         file.write(py_str + '\n')
    
#     return "Command Executed and Saved"

# def python_exec_cmd(py_str: str):
#     """function to execute simple python commands"""

#     print(py_str)
#     return "Command Executed and Saved"

# # with open('polybot_experiment.py', 'r') as polybot_file:
# #     POLYBOT_FILE = ''.join(polybot_file.readlines())

# # POLYBOT_FILE_FILTER = POLYBOT_FILE.replace("{", "")
# # POLYBOT_FILE_FILTER = POLYBOT_FILE_FILTER.replace("}", "")

# with open('polybot_experiment.py', 'r') as polybot_file:
#     POLYBOT_FILE = ''.join(polybot_file.readlines())

# POLYBOT_FILE_FILTER = POLYBOT_FILE.replace("{", "")
# POLYBOT_FILE_FILTER = POLYBOT_FILE_FILTER.replace("}", "")
# POLYBOT_FILE_LINES = len(POLYBOT_FILE.split('\n'))

# POLYBOT_RUN_FILE_PATH = "C:/Users/Public/robot/N9_demo_3d/polybot_screenshots/polybot_screenshots.py"
# if os.path.exists(POLYBOT_RUN_FILE_PATH):
#     POLYBOT_RUN_FILE = ''.join(open(POLYBOT_RUN_FILE_PATH).readlines())
# else:
#     POLYBOT_RUN_FILE = ''
# POLYBOT_RUN_FILE_FILTER = POLYBOT_RUN_FILE.replace("{", "").replace("}", "")
# POLYBOT_RUN_FILE_LINES = len(POLYBOT_RUN_FILE.split('\n'))

# exec_polybot_tool = StructuredTool.from_function(polybot_exec_cmd,
#                                             name="WritePython",
#                                             description="Takes in a python string and execs it in the environment described by the script."
#                                             + "The script will contain objects and functions used to interact with the instrument. "
#                                             + "Here are some rules to follow: \n"
#                                             + "Before running the experiment create a new python file with all the library imports (robotics, loca, rack_status, proc, pandas, etc.) or any other list that is required."
#                                             + "Check if the requested polymer is available in the rack_status and then directly proceed with the experimental excecution"
#                                             + "Some useful commands and instructions are provided below \n\n" + POLYBOT_FILE_FILTER)
                                            

# def polybot_linter(py_str: str):
#     """
#     Linting tool for Polybot. Prepends the Polybot file.
#     """
#     print("running linter......")
#     lint_fp = POLYBOT_RUN_FILE_PATH # 'agent_scripts/tmp_lint.py' #POLYBOT_RUN_FILE_PATH
#     lint_output = lint_cmd(py_str, lint_fp, py_pfx=POLYBOT_RUN_FILE_FILTER)
#     # lint_output = filter_pylint_lines(lint_output, POLYBOT_RUN_FILE_LINES)
    
#     if ':' not in lint_output:
#         lint_output += '\nNo errors.'
        
#     return lint_output


# exec_polybot_lint_tool = StructuredTool.from_function(
#     polybot_linter,
#     name="LintPython",
#     description="Takes in a python string and lints it."
#     + " Always run the linter to check the code before running it."
#     + " The output will provide suggestions on how to improve the code."
#     + " Attempt to correct the code based on the linter output."
#     + " Rewrite the code until there are no errors. "
#     + " Otherwise, fix the code and check again using linter."
# )



# """
# ===============================
# S26 Tools
# ===============================
# """
# from langchain_community.utilities.wolfram_alpha import WolframAlphaAPIWrapper

# with open('S26_commandline.py', 'r') as s26_file:
#     S26_FILE = ''.join(s26_file.readlines())

# # Filters for langchain seems to be parsing the description as a fstring
# S26_FILE = S26_FILE.replace("{", "")
# S26_FILE = S26_FILE.replace("}", "")

# if params.use_wolfram:
#     wolfram = WolframAlphaAPIWrapper()

#     wolfram_tool = StructuredTool.from_function(wolfram.run,
#                                                 name="Calculator",
#                                                 description="When performing an arithmatic operation don't assume, run them through this tool as a seperate action. Examples may include addition, subtraction, multiplicaiton, and divison.")


# exec_cmd_tool = StructuredTool.from_function(exec_cmd,
#                                             name="ExecPython",
#                                             description="Takes in a python string and execs it in the envionment described by the script."
#                                             + "The script will contain objects and functions used to interact with the instrument. "
#                                             + "Here are some rules to follow: \n"
#                                             + "unlock_hybrid() and lock_hybrid() must be called before and after all motor movements"
#                                             + " and scans."
#                                             + " The script is described below \n\n" + S26_FILE)

