from dotenv import load_dotenv
load_dotenv()
from gemini import Gemini
gemini = Gemini("gemini-2.5-flash")
from agents import react_agent
from tools import  tool
from datetime import datetime
from tavily import TavilyClient
@tool
def get_current_time(format: str):
    "use to get current time"
    return datetime.now().strftime(format)

@tool
def search(content: str):
    "can search internet for up to date information. parameter 'content' can be like search content you wanna search"
    tavily = TavilyClient()
    try: 
        return tavily.search(content)['results'][0]['content']
    except: Exception("error happened during executing tavily search")


print(react_agent(Gemini("gemini-2.5-flash"),prompt="what time is it now in south korea?", tools=[get_current_time, search]))