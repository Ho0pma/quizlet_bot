from os import environ
from typing import Final

class TgKeys:
    TOKEN: Final = environ.get('TOKEN', 'DefineMe!')