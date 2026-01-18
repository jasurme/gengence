from typing import Optional
import sqlite3
import os
from typing import List
class Message:
    def __init__(self, type:int, text:str):
        self.type = type
        self.text = text
    
    def _format_message(self):
        type_mapping = {1: {"type":"system_message", "intent": "you are helpful assistant"},
                        2: {"type":"human_message", "intent": "it is human message"}, 
                        3: {"type":"ai_message", "intent": "it is ai-generated message"}}

        return f"<{type_mapping[self.type]['type']} intent={type_mapping[self.type]['intent']}>{self.text}</{type_mapping[self.type]['type']}>"

    def __str__(self):
        return self._format_message()
    def __repr__(self):
        return self._format_message()

class Messages:
    def __init__(self, table_name: str, message: Optional[str | List[str] | Message] = None):
        self.message = message
        self.table_name = table_name
        self._initialize()
    
    def _initialize(self):
        if self.message:
            os.makedirs("message_bank", exist_ok=True)
            conn = sqlite3.connect(f"message_bank/{self.table_name}.db")
            c = conn.cursor()
            c.execute(f"CREATE TABLE IF NOT EXISTS {self.table_name} (message TEXT)")
            conn.commit()
            print(f'initialized {self.table_name} db')
            conn.close()
    
    def add(self, message: str | Message | List[str]):
        os.makedirs('message_bank', exist_ok=True)
        conn = sqlite3.connect(f"message_bank/{self.table_name}.db")
        c = conn.cursor()
        c.execute(f"CREATE TABLE IF NOT EXISTS {self.table_name} (message TEXT)")
    
        if isinstance(message,Message):
            message = str(message)
        elif isinstance(message, list):
            for msg in message:
                self.add(msg)
        else: raise TypeError("incorrect message type. should be either str, Message obj or list[str]")

        c.execute(f"INSERT into {self.table_name} (message) values (?)", (message, ))
        conn.commit()
        print('successfully added')
        conn.close()
    
    def _fetch_all(self):
        os.makedirs('message_bank', exist_ok=True)
        conn = sqlite3.connect(f"message_bank/{self.table_name}.db")
        c = conn.cursor()
        c.execute(f"CREATE TABLE IF NOT EXISTS {self.table_name} (message TEXT)")
        c.execute(f"select * from {self.table_name}")
        rows = c.fetchall()
        conn.close()
        msgs = ""
        if rows:
            for row in rows:
                (r,) = row
                msgs  += "\n" + r
        return msgs
        
    def get(self):
        return self._fetch_all()

    def __str__(self):
        return self._fetch_all()
    def __repr__(self):
        return self._fetch_all()
        
            


        
            


        