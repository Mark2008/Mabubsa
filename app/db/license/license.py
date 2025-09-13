from typing import Callable

import requests
from bs4 import BeautifulSoup

from db.cached_file import cached_file


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
    @cached_file(f'app/db/license/cc-{slug}-4.0.txt')
    def get_sth():
        url = f'https://creativecommons.org/licenses/cache/{slug}/4.0/legalcode.ko'
        return __soup_cc(url, "#legal-code-body")
    return get_sth
        
def __cc_deed_factory_4_0(slug: str) -> Callable:
    @cached_file(f'app/db/license/cc-{slug}-4.0.deed.txt')
    def get_sth():
        url = f'https://creativecommons.org/licenses/cache/{slug}/4.0/deed.ko'
        return __soup_cc(url, "#deed-body")
    return get_sth

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