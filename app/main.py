from typing import Union

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

import pydantic
from random import randint


app = FastAPI()


test_database = {}

class DataRequest(pydantic.BaseModel):
    session: int
    data: str

@app.get('/api/make-session')
async def make_session():
    session = randint(0, 9999)
    while session in test_database.keys():
        session = randint(0, 9999)
    test_database[session] = 'nothing'
    return {'session': session}

@app.post('/api/write-data')
async def some_request(request: DataRequest):
    test_database[request.session] = request.data
    return {"status": "success"}
    

@app.get('/api/view-data')
async def view_data(session: int):
    return {"data": test_database.get(session, "No data found")}



### 메인 메뉴 화면 ###
app.mount("/mola", StaticFiles(directory="app/templates/mola", html=True))
app.mount("/", StaticFiles(directory="app/templates", html=True))

# 일반 파이썬으로 실행했을 때
if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', port=1234)