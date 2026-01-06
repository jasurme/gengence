from dotenv import load_dotenv
from google import genai
from typing import Type, Optional
load_dotenv()
class Gemini:
    def __init__(self, model: str, structured_config:Optional[Type] = None):
        self.model = model
        self.structured_config=structured_config
        self.__initialize()
    
    def __initialize(self):
        self.gemini = genai.Client()
    
    def generate(self, prompt):
        config = {"temperature" : 1}
        if self.structured_config:
            config.update(self.structured_config)
        return self.gemini.models.generate_content(model=self.model, contents=prompt, config=config).text
