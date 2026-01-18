
from google import genai
from typing import Type, Optional
import json

class Gemini:
    def __init__(self, model: str):
        self.model = model
        self.__initialize()
    
    def __initialize(self):
        self.gemini = genai.Client()
    
    def generate(self, prompt:str, pydantic_object:Optional[object]=None):
        config = {"temperature" : 1}
        if pydantic_object:
            additional_config = {
                "response_mime_type": "application/json",
                "response_json_schema": pydantic_object.model_json_schema()
            }
            config.update(additional_config)

        res= self.gemini.models.generate_content(model=self.model, contents=prompt, config=config).text
        if pydantic_object:
            return json.loads(res)
        else: return res
