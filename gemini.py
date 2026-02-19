
from google import genai
from typing import Type, Optional
import json

class Gemini:
    def __init__(self, model: str):
        self.model = model
        self.__initialize()
    
    def __initialize(self):
        self.gemini = genai.Client()
    
    def generate(self, prompt:str, pydantic_object:Optional[object]=None, tools:list=None):
        config = {"temperature" : 1}
        tools_prompt = ""
        try: 
            tools_prompt += "you are given following tools(use it when necessary): \n"
            for index, tool in tools:
                toolname = tool.name
                tool_description = tool.description
                arg_schema = tool.arg_schema
                tools_prompt += f"tool [{index}+1] name: {toolname}.\ntool description: {tool_description}. \narg schema: {arg_schema}\n\n"
        except: Exception("error happened")


                
        if pydantic_object:
            additional_config = {
                "response_mime_type": "application/json",
                "response_json_schema": pydantic_object.model_json_schema()
            }
            config.update(additional_config)

        res= self.gemini.models.generate_content(model=self.model, contents=tools_prompt + "question: " + prompt, config=config).text
        if pydantic_object:
            return json.loads(res)
        else: return res
