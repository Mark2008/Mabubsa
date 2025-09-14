from typing import Dict

from selenium import webdriver
from selenium.webdriver.common.by import By

import global_driver


def cn_serachquery(query: str) -> Dict[str, str]:
    driver = global_driver.DRIVER
    driver.get(f"https://casenote.kr/search/?q={query}")

    elems = driver.find_elements(By.CLASS_NAME, 'title')

    to_find = []

    for elem in elems:
        try:
            e2 = elem.find_element(By.TAG_NAME, 'a')
            child_link = e2.get_attribute('href')
            to_find.append(child_link)
            
        except Exception as e:
            pass

    saved = {}

    for url in to_find:
        driver.get(url)

        title = driver.find_element(By.CLASS_NAME, 'cn-case-title')
        content = driver.find_element(By.CLASS_NAME, 'cn-case-body')

        saved[title.text] = content.text

    return saved