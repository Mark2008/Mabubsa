from typing import Dict
import time

import asyncio

from selenium import webdriver
from selenium.webdriver.common.by import By

import re

from openai import AsyncOpenAI

from db.cached_file import cached_file
import globals


async def batch_process(content: str, situation: str):
    # content에서 situation에 맞는 유용한 내용을 찾아냅니다
    from ai.gpt import MessageHistory

    history = MessageHistory()
    history.add_system('제공되는 법령에서 situation과 적합한 내용을 content에서 찾아냅니다')
    history.add_system('다른 말 없이 해당 내용만을 출력합니다.')
    history.add_system('situation: '+ situation)
    history.add_system('content:'+ content)

    client = AsyncOpenAI()
    response = await client.chat.completions.create(
        model = globals.MODEL,
        messages = history.get_record(),
        temperature=0
    )
    return response.choices[0].message.content

async def search_laws_batch(query: str, situation: str, n: int = 5):
    laws = await search_laws(query)
    if laws == {}:
        return {'failed': f'{query}에 대한 법률을 찾을 수 없습니다.'}

    result = {}
    cnt = 0
    for name in laws.keys():
        result[name] = await search_specific_law(name)
        cnt += 1
        if cnt >= n:
            break
    
    gather = [batch_process(value, query) for value, query in result.items()]
    asyncio.gather(*gather)
    return result

async def search_laws(query: str) -> Dict[str, str]:
    url = f'https://www.law.go.kr/lsSc.do?section=&menuId=1&subMenuId=15&tabMenuId=81&eventGubun=060101&query={query}'
    
    driver = globals.DRIVER
    driver.get(url)

    driver.implicitly_wait(5)
    elem = driver.find_element(By.CLASS_NAME, 'tbl_wrap')
    e2 = elem.find_elements(By.CLASS_NAME, 'tl')

    result = {}
    for e in e2:
        a = e.find_element(By.TAG_NAME, 'a')
        result[a.text] = a.get_attribute('href')
    
    return result
    
async def search_specific_law(name: str) -> str:
    name = re.sub('[ ㆍ]', '', name)

    @cached_file(f'app/db/cache/law/{name}.txt')
    def wrapper():
        url = f'https://www.law.go.kr/법령/{name}'

        driver = globals.DRIVER
        driver.get(url)
        driver.switch_to.frame(driver.find_element(By.TAG_NAME, "iframe"))

        driver.implicitly_wait(10)
        elem = driver.find_element(By.CLASS_NAME, 'scr_area')

        elems = elem.find_elements(By.CLASS_NAME, 'pgroup')

        text = ''
        for e in elems:
            text += e.text

        return text
    
    return wrapper()