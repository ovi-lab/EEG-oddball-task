import os
from typing import Callable

from config import Config

configObj = Config()
configss = configObj.getConfigSnapshot()

def getOVStimCodes() -> dict[str, int]:
    ovStimCodes = {}
    ovStimListPath = os.path.join(configss['root'],
                                   configss['ov_stim_list_path'])
    with open(ovStimListPath) as file:
        lines = file.readlines()
        for line in lines:
            val = line.split() 
            ovStimCodes[val[0].strip()] = int(val[2].strip(), base =16)

   
    if not len(ovStimCodes) == len(lines):
        raise Exception (
            "The number of stimulation codes read from the stimulations " +
            "file is not equal to the number of lines in that file."
                         )    
        
    return ovStimCodes

def getChannelNamesEEGO() -> list[str]:
    path = os.path.join(configss['root'],
                         configss['eego_electrode_map_path'])
    with open(path, "r") as f:
        channelNames = [line.strip() for line in f]
    return channelNames
