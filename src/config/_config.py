import logging 
import os
import glob 

import yaml

logger = logging.Logger(__name__)

class Config:
    def __init__(self):

        start_path = os.path.abspath(__file__)
        file = '.gitignore'

        last_root   = start_path
        current_root = start_path
        found_path   = None
        while found_path is None and current_root:
            pruned = False
            for root, dirs, files in os.walk(current_root):
                if not pruned:
                    try:
                         # Remove the part of the tree we already searched
                        del dirs[dirs.index(os.path.basename(last_root))]
                        pruned = True
                    except ValueError:
                        pass
                if file in files:
                    # found the file, stop
                    found_path = os.path.join(root, file)
                    break
            # Otherwise, pop up a level, search again
            last_root    = current_root
            current_root = os.path.dirname(last_root)     


        if(not found_path):
             raise Exception (" Could not find the root directroy path on "
                             + last_root )
        else:
             self.__root =   os.path.dirname(found_path)

        config_path_from_root =  os.path.relpath(os.path.dirname(os.path.abspath(__file__)), start = self.__root)
        self.__config_path = os.path.join(self.__root ,config_path_from_root , 'config.yml')  


    def __getConfig(self):
        config = {}

        if not os.path.exists(self.__config_path):
            raise Exception (" Could not find the config file on path"
                             + self.__config_path )
        
        else:
            with open(self.__config_path, 'r') as file:
                contents = yaml.safe_load(file)

                if contents is not None:
                    config.update(contents)
                    config['root'] =  self.__root
                    
        return config           


    def getConfigSnapshot(self):
        return self.__getConfig()


# ConfigObj = Config()
