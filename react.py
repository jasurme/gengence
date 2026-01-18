from langchain.agents import create_agent
from langchain.tools import tool
from langgraph.prebuilt import create_react_agent
from datetime import datetime
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import TypedDict, Union, Annotated
import operator
from langchain_core.agents import AgentAction,AgentFinish
from langgraph.prebuilt import ToolNode
load_dotenv()

gpt = ChatOpenAI(model='gpt-4o-mini')

@tool
def get_current_date(format: str="%Y-%m-%d %H-%M-%S"):
    now = datetime.now()
    return now.strftime(format)


tavily_tool = TavilySearch()

tools = [get_current_date, tavily_tool]

react = create_agent(model=gpt, tools=tools)  

class AgentState(TypedDict):
    input: str
    agent_outcome: Union[AgentAction, AgentFinish, None]
    intermediate_steps: Annotated[list[tuple[AgentAction, str]], operator.add]


def reason_node(state: AgentState):
    agent_outcome = react.invoke(state)
    state['agent_outcome'] = agent_outcome
    return state




def act_node(state:AgentState):
    agent_action = state['agent_outcome']
    chosentool_name = agent_action.tool
    chosentool_input = agent_action.tool_input
    tool_fn = None

    if tools:
        for tool in tools:
            if tool.name == chosentool_name:
                tool_fn = tool

    if tool_fn:
        if isinstance(chosentool_input, dict):
            output = tool_fn.invoke(**chosentool_input)
        else: output = tool_fn.invoke(chosentool_input)
    else: output = f"tool '{chosentool_name}' not found"

    state['intermediate_steps'] = [(agent_action, str(output))]




