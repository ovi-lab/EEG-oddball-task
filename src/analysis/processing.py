# from src.config import Config
from config import Config

class Processing:
    def __init__(self) -> None:
        pass

    
    @classmethod
    def getPconfig(cls):
        Config.getConfig()