from dotenv import load_dotenv
from google import genai
load_dotenv()
class Gemini:
    def __init__(self, model):
        self.model = model
        self.__initialize()
    
    def __initialize(self):
        self.gemini = genai.Client()
    
    def generate(self, prompt):
        return self.gemini.models.generate_content(model=self.model, contents=prompt).text
