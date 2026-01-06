class Message:
    def __init__(self, type:int, text:str):
        self.type = type
        self.text = text
        self.__initialize()

    def __initialize(self):
        type_mapping = {1: {"type":"system_message", "intent": "you are helpful assistant"},
                        2: {"type":"human_message", "intent": "it is human message"}, 
                        3: {"type":"ai_message", "intent": "it is ai-generated message"}}

        return f"<{type_mapping[self.type]['type']} intent={type_mapping[self.type]['intent']}>{self.text}</{type_mapping[self.type]['type']}>"