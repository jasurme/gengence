from gemini import Gemini
from message_types import Message

from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.prompts import MessagesPlaceholder, ChatPromptTemplate
gemini = Gemini(model="gemini-2.5-flash")
messages = []
messages.append(Message(1, "always answer within 2 not long sentences"))
while True:
    inp = input("ask: ")
    if inp == 'q':
        break
    human = Message(2, inp)
    messages.append(human)
    ai = gemini.generate(messages)
    messages.append(ai)
    print('ai: ', ai)

print(messages)



