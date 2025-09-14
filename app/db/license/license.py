from typing import Dict, Callable

import requests
from bs4 import BeautifulSoup

from db.cached_file import cached_file


LICENSE_MAP: Dict[str, Callable] = {}

def add_map(key: str):
    def wrapper(func: Callable):
        LICENSE_MAP[key] = func
        return func
    return wrapper

# Creative Commons ----------------------------
def __soup_cc(url: str, cl: str) -> str:
    res = requests.get(url)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')
    
    body = soup.select(cl)
    text = ''
    for tag in body:    
        lines = [p.get_text(strip=True) for p in tag.find_all(["p","div","li"])]
        text += '\n\n'.join(lines)  # 문단 구분용 이중 줄바꿈
    return text

def __cc_factory_4_0(slug: str) -> Callable:
    @add_map(f'CC {slug.upper()} 4.0 legalcode')
    @cached_file(f'app/db/license/cache/cc-{slug}-4.0.txt')
    def get_sth():
        url = f'https://creativecommons.org/licenses/{slug}/4.0/legalcode.ko'
        return __soup_cc(url, "#legal-code-body")
    return get_sth
        
def __cc_deed_factory_4_0(slug: str) -> Callable:
    @add_map(f'CC {slug.upper()} 4.0 deed')
    @cached_file(f'app/db/license/cache/cc-{slug}-4.0.deed.txt')
    def get_sth():
        url = f'https://creativecommons.org/licenses/{slug}/4.0/deed.ko'
        return __soup_cc(url, "#deed-body")
    return get_sth

@add_map(f'About CC')
@cached_file('app/db/license/cache/cc.about.txt')
def get_cc_about():
    url = 'https://creativecommons.org/licenses/by/4.0/legalcode.ko'
    top = __soup_cc(url, '.notice-top')
    bottom = __soup_cc(url, '.notice-bottom')
    return top + bottom
    
get_cc_by_4_0 = __cc_factory_4_0('by')
get_cc_by_nc_4_0 = __cc_factory_4_0('by-nc')
get_cc_by_nc_nd_4_0 = __cc_factory_4_0('by-nc-nd')
get_cc_by_nc_sa_4_0 = __cc_factory_4_0('by-nc-sa')
get_cc_by_nd_4_0 = __cc_factory_4_0('by-nd')
get_cc_by_sa_4_0 = __cc_factory_4_0('by-sa')

get_cc_by_deed_4_0 = __cc_deed_factory_4_0('by')
get_cc_by_nc_deed_4_0 = __cc_deed_factory_4_0('by-nc')
get_cc_by_nc_nd_deed_4_0 = __cc_deed_factory_4_0('by-nc-nd')
get_cc_by_nc_sa_deed_4_0 = __cc_deed_factory_4_0('by-nc-sa')
get_cc_by_nd_deed_4_0 = __cc_deed_factory_4_0('by-nd')
get_cc_by_sa_deed_4_0 = __cc_deed_factory_4_0('by-sa')


# 펑션콜 전용 함수
async def find_license(license: str):
    if license in LICENSE_MAP.keys():
        return LICENSE_MAP[license]()
    else:
        return {'error': 'cannot find requested function'}

async def get_available_license():
    return list(LICENSE_MAP.keys())