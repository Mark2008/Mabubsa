import os
from typing import Dict
from dotenv import load_dotenv

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
# from fastapi.responses import Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates

import pydantic
from uuid import uuid4

from ai import gpt

import globals        ## 드라이버 열기


### 서버 주소 .env에서 가져오기.
try:
    load_dotenv()
    SERVER_IP = os.getenv("SERVER_IP")
except Exception as ex:
    print('.env에 SERVER_IP를 설정하세요')
    raise ex


app = FastAPI()

templates = Jinja2Templates(directory='app/templates')

### CORS 설정
origins = [
    "http://localhost",
    "http://localhost:8000",
    SERVER_IP
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    # allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

test_database : Dict[str, gpt.AIManager] = {}     # key: session, value: 유저 정보


### API
@app.get('/api/make-session')
async def make_session():
    session = str(uuid4())
    test_database[session] = gpt.AIManager()
    return {'session': session}


class PromptRequest(pydantic.BaseModel):
    session: str
    prompt: str

@app.post('/api/enter-prompt')
async def enter_prompt(request: PromptRequest):
    ai_manager = test_database[request.session]
    result_text = await ai_manager.process(request.prompt)
    print(ai_manager.message_history.rec)
    return {'result_text': result_text}


### 메인 메뉴 화면 ###
app.mount("/static", StaticFiles(directory="app/static"), name="static")
@app.get('/')
async def root(request: Request):
    return templates.TemplateResponse("index.html", {
        'request': request,
        'ip': SERVER_IP
    })

async def test():
    from db.law import law

    res = await law.search_laws_batch('자동차')
        
    print(res)

# 일반 파이썬으로 실행했을 때
if __name__ == '__main__':
    try:
        import uvicorn
        uvicorn.run('main:app', host="0.0.0.0")
        
        # import trio
        # trio.run(test)

    except Exception as e:
        raise e
    
    finally:
        globals.DRIVER.close()