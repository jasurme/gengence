import inspect
from pydantic import create_model
from typing import Callable
from datetime import datetime


class ToolObject:
    def __init__(self, name: str, description:str, func: Callable, arg_schema):
        self.name = name
        self.description = description
        self.func = func
        self.arg_schema = arg_schema
    
    def invoke(self, args):
        return self.func(**self.arg_schema(**args).model_dump())
        




def tool(func):
    tool_name = func.__name__
    if not func.__doc__:
        raise ValueError(f"tools must have docstring explaining what the tool does, its parameters and output. \n tool '{tool_name}' isn't given with docstring")
    else: tool_description = func.__doc__
    fields = {}
    sig = inspect.signature(func)
    for param_name, param in sig.parameters.items():
        if param.annotation == inspect._empty:
            raise ValueError(f"data types should be specified for tool parameters. parameter '{param_name}' is missing data type ")
        default = param.default if param.default != inspect._empty else ...
        fields[param_name] = (param.annotation, default)
        ArgsModel = create_model(f"{tool_name}Args", **fields)

    return ToolObject(tool_name, tool_description, func, ArgsModel)

@tool
def get_current_time(format: str ="%Y-%m-%d %H:%M:%S"):
    "use to get current time"
    return datetime.now().strftime(format)

print(get_current_time.arg_schema.model_json_schema())



