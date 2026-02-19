from pydantic import BaseModel, Field
from typing import Any, Union
from gemini import Gemini
class AgentAction(BaseModel):
    tool_name: str
    tool_input: Any
    comment: str = Field(description="explain why you are doing what you are doing?")

class AgentFinish(BaseModel):
    final_response: str
    comment: str = Field(description="explain why you are doing what you are doing?")


class ReactAgent(BaseModel):
    choice: Union[AgentAction, AgentFinish]








def react_agent(llm:Gemini,prompt, tools: list):
    final_prompt = "You have following tools to use when necessary(break down question into small parts and use only one tool at a time and wait for its response and continue like this until you reach the final answer): \n"
    for index, tool in enumerate(tools):
        print(f"\n\n{tool.arg_schema}\n\n")
        final_prompt += f"tool {index+1}: name: {tool.name}. description: {tool.description}. arg schema: {tool.arg_schema.model_json_schema()}\n"
    final_prompt += f"""<instructions>:  you break down question into tiny steps and call tools step by step and once you reach final answer that answers user question, output it to user in friendly response text
    for time related questions, first if available use get curent time tool to know current time and do the rest of what question asks </instructions> \n Question: {prompt}"""
    while True:
        res = llm.generate(final_prompt, pydantic_object=ReactAgent)
        res = ReactAgent.model_validate(res)
        response_tool = res.choice
        if isinstance(response_tool, AgentAction):
            print(f"Thought: {response_tool.comment}")
            print(f"Action: {response_tool.tool_name}")
            print(f'type: {type(response_tool.tool_input)}')
            print(f"Action input: {response_tool.tool_input}")
            
            for tool in tools:
                if tool.name == response_tool.tool_name:
                    tool_fn = tool
            tool_response = tool_fn.invoke(response_tool.tool_input)
            print(f"Tool Response: {tool_response}")
            final_prompt += f"Thought: {response_tool.comment}\n" +f"Action: {response_tool.tool_name}\n" + f"Action input: {response_tool.tool_input}\n" + f"tool output: {tool_response}"
        elif isinstance(response_tool, AgentFinish):
            print(f"Final Thought: {response_tool.comment}")
            print("Final response: ", response_tool.final_response)
            break
    
    return response_tool.final_response





        



    