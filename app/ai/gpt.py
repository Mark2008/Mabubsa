import os
import json

from dotenv import load_dotenv
from openai import AsyncOpenAI

from db.license import license
from webcrawl import crawler


# 함수 레지스트리
FUNCTION_MAP = {
    'find_license': license.find_license,
    'get_available_license': license.get_available_license,
    'find_cases': crawler.cn_serachquery
}
MAX_LOOP = 5

SYSTEM_MESSAGE = \
f"""
그저 AI
FUNCTION CALL MAX_LOOP: {MAX_LOOP}
"""


# API Key 가져오기
try:
    load_dotenv()
    GPT_KEY = os.getenv("OPENAI_API_KEY")
except Exception as ex:
    print('KEY가 설정되지 않았습니다! (.env에 OPENAI_API_KEY를 설정하세요)')
    raise ex

# AI가 사용할 수 있는 도구(함수)들을 정의
try:
    with open('app/ai/tools.json', 'r', encoding='UTF-8') as file:
        TOOL_DEFINITIONS = json.load(file)
except Exception as ex:
    print('tools.json을 찾을 수 없습니다!')
    raise ex



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

    # def add_toolcall(self, tool_calls, )
        

# AI 관리 클래스
class AIManager:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=GPT_KEY)
        self.message_history = MessageHistory()
        self.message_history.add_system(SYSTEM_MESSAGE)

    # 사용자의 입력을 받고 AI의 입력을 받음, 대답 내용만 반환
    async def process(self, user_text):
        self.message_history.add_user(user_text)

        for _ in range(MAX_LOOP):
            response = await self.gpt_request()
            msg = response.choices[0].message
            print(msg, type(msg))
            if msg.tool_calls:
                self.message_history.rec.append({
                    'role': 'assistant',
                    'tool_calls': msg.tool_calls
                })

                for tool_call in msg.tool_calls:
                    func_name = tool_call.function.name
                    args = json.loads(tool_call.function.arguments)
                    result = FUNCTION_MAP[func_name](**args)
                    self.message_history.rec.append({
                        'role': 'tool',
                        'tool_call_id': tool_call.id,
                        'content': json.dumps(result, ensure_ascii=False)
                    })
            else:
                break
        assistant_text = msg.content or "뭔가 잘못됨" 
        self.message_history.add_assistant(assistant_text)
        return assistant_text


    # gpt api에 요청을 하고 결과를 반환
    async def gpt_request(self):
        completion = await self.client.chat.completions.create(
            model = "gpt-4o-mini",
            messages = self.message_history.rec,
            tools = TOOL_DEFINITIONS,
            tool_choice = "auto"
        )
        print(type(completion))
        return completion
    


