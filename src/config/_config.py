import logging 
import os 

import yaml

logger = logging.Logger(__name__)

class Config:

    def __init__(self) -> None:
        file_path = os.getcwd()

        root =  os.path.dirname(file_path)


        


        self.__root =  root


    def getConfig(self):
        print(self.__root)
            

