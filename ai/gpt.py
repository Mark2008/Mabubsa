import os
import json
from dotenv import load_dotenv
from openai import OpenAI


# API Key 가져오기
try:
    load_dotenv()
    GPT_KEY = os.getenv("GPT_KEY")
except Exception as ex:
    print('API KEY가 설정되지 않았습니다! (.env를 설정하세요)')
    raise ex

# AI가 사용할 수 있는 도구(함수)들을 정의
try:
    with open('ai/tools.json', 'r', encoding='UTF-8') as file:
        TOOL_DEFINITIONS = json.load(file)
except Exception as ex:
    print('tools.json을 찾을 수 없습니다!')
    raise ex

SYSTEM_MESSAGE = \
"""
그저 AI
"""


# 채팅 기록을 저장한다
class MessageHistory:
    def __init__(self):
        self.rec = []

    def add_something(self, role, content):
        self.rec.append({'role': role, 'content': content})

    def add_system(self, content):
        self.rec.append({'role': 'system', 'content': content})
    
    def add_user(self, content):
        self.rec.append({'role': 'user', 'content': content})

    def add_assistant(self, content):
        self.rec.append({'role': 'assistant', 'content': content})
        

# AI 관리 클래스
class AIManager:
    def __init__(self):
        self.client = OpenAI(api_key=GPT_KEY)
        self.message_history = MessageHistory()
        self.message_history.add_system(SYSTEM_MESSAGE)

    # 사용자의 입력을 받고 AI의 입력을 받음
    def process(self, user_text):
        self.message_history.add_user(user_text)
        completion = self.gpt_request()

        print(completion)

    # gpt api에 요청을 하고 결과를 반환
    def gpt_request(self):
        completion = self.client.chat.completions.create(
            model = "gpt-4o-mini",
            messages = self.message_history.rec,
            tools = TOOL_DEFINITIONS,
            tool_choice = "auto"
        )
        return completion
    


