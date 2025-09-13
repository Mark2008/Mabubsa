from typing import Callable
from pathlib import Path


def cached_file(path: str, encoding: str = "utf-8"):
    def inner(func: Callable):
        def action(*args, **kwargs):
            p = Path(path)
            if p.exists():
                return p.read_text(encoding=encoding)
            
            result = func(*args, **kwargs)
            p.write_text(result, encoding=encoding)
            return result

        return action
    
    return inner