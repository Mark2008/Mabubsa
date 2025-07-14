import sys

if __name__ != "__main__":
    sys.exit()

from ai import gpt
from webcrawl import crawler

manager = gpt.AIManager()
manager.process('아아아안녕하세요요요 방방방방수환쌤')