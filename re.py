from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
load_dotenv()
from tavily import TavilyClient
tavily = TavilyClient()
from langchain.tools import tool
from datetime import datetime
from gemini import Gemini   
from pydantic import BaseModel, Field
from typing import Union, Any, TypedDict, Annotated
import operator
gemini = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

class AgentAction(BaseModel):
    tool:str
    tool_input:Any
    log: str = Field(description='explain why you are doing what you are doing')

class AgentFinish(BaseModel):
    output: Any
    log: str = Field(description='explain what you have done')

class AgentToolAction(BaseModel):
    tool: Union[AgentAction, AgentFinish]

# class AgentLanggraph(TypedDict):
#     input: str
#     agent_outcome: Union[AgentAction, AgentFinish, None]
#     intermediate_steps: Annotated[list[tuple[AgentAction, str]],operator.add]

@tool
def tavily_tool(content):
    """tavily search"""
    return tavily.search(content)['results'][0]['content']

@tool
def get_current_time(format=""):
    """get current time"""
    time = datetime.now()
    return time.strftime("%Y-%m-%d %H-%M-%S")

tools = [ tavily_tool, get_current_time]

gemini = Gemini(model="gemini-2.5-flash")

question = 'how many days have been since gpt-5 launch. first know current time and find gpt5 launch date'

prompt = f"""
    you have following tools: tavily_tool(parameters: content that is searched) and get_current_time tool(parameter:  format(strftime)).
      here is the question: {question}. Use the following format:  
      Question: the input question you must answer 
      Thought: you should always think about what to do 
      Action: the action to take, should be one of [tool_names]
    And you break down question into tiny steps and call tools step by step and once you reach final answer that answers user question, output it to user in friendly response text
    for time related questions, first if available use get curent time tool to know current time and do the rest of what question asks
    """
while True:
   
    response = gemini.generate(prompt=prompt, pydantic_object=AgentToolAction)
    response = AgentToolAction.model_validate(response)
    response_tool = response.tool
    
    if isinstance(response_tool, AgentAction):
        tool_name = response_tool.tool
        log = response_tool.log
        tool_input = response_tool.tool_input
        for tool in tools:
            if tool_name == tool.name:
                tool_fn = tool
            
        tool_ans = tool_fn.invoke(tool_input)
        print(f"tool output: {tool_ans}")

        print(f"\n\nThought: {log}")
        print(f"Action: {tool_name}")
        print(f"Action input: {tool_input}\n")
        prompt += f"tool output: {tool_ans}"
        
    elif isinstance(response_tool, AgentFinish):
        print(f"Final Thought:{response_tool.log}")
        print(f"Final Response: {response_tool.output}")
        break

print('successfully finished')
    

