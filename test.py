from messages import Message, Messages
from gemini import Gemini

gemini_llm = Gemini('gemini-2.5-flash')

message_bank = Messages()

message_bank.add(Message(1, "you are lionel messi who speak in english and answers with 2 max sentences"))

while True: 
    human_input = input('ask: ')
    if human_input == 'q':
        break
    print(type(human_input), repr(human_input))

    message_bank.add(Message(2, human_input))

    ai = gemini_llm.generate(message_bank.get())
    message_bank.add(Message(3, ai))
    print(ai)

print('\n\n', message_bank.get())

