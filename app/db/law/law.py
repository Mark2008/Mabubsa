from typing import Dict
import time

from selenium import webdriver
from selenium.webdriver.common.by import By

import re

from db.cached_file import cached_file
import global_driver



def test():
    n = 3
    q = '자동차'
    laws = search_laws(q)

    result = {}
    cnt = 0
    for name in laws.keys():
        result[name] = search_specific_law(name)
        cnt += 1
        if cnt >= n:
            break

    print(result)
    return result

def search_laws(query: str) -> Dict[str, str]:
    url = f'https://www.law.go.kr/lsSc.do?section=&menuId=1&subMenuId=15&tabMenuId=81&eventGubun=060101&query={query}'
    
    driver = global_driver.DRIVER
    driver.get(url)

    driver.implicitly_wait(5)
    elem = driver.find_element(By.CLASS_NAME, 'tbl_wrap')
    e2 = elem.find_elements(By.TAG_NAME, 'a')

    result = {}
    for e in e2:
        result[e.text] = e.get_attribute('href')
    
    return result
    
def search_specific_law(name: str) -> str:
    name = re.sub('[ ㆍ]', '', name)

    @cached_file(f'app/db/cache/law/{name}.txt')
    def wrapper():
        url = f'https://www.law.go.kr/법령/{name}'

        driver = global_driver.DRIVER
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