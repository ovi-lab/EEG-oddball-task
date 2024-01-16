import mne
import pandas as pd
import tools.helpers
import os 

from config import Config
configObj = Config()
configss = configObj.getConfigSnapshot()


# todo: add validations to check the path, file type, partipantId check
def loadData(partipantId):
    participant_name = 'P' + str(partipantId)
    partipant_data_path =  participant_name + '/' + participant_name +'.gdf'
    path = os.path.join(configss['root'], configss['data_dir'] , partipant_data_path ) 
    print(path)
    raw  = mne.io.read_raw_gdf(path)
    return raw

def preprocessing(raw):

    raw = raw.resample(sfreq=250)

    # remove unnecessary channels
    data_channels = [x for x in raw.ch_names if x not in 
                     configss['non_data_channels']]
    if configss['target_channels'] is not None:
        data_channels = configss['target_channels']

    raw = raw.pick(data_channels)

    l_freq = configss['l_freq'] if configss['l_freq'] is not None else None 
    h_freq = configss['h_freq'] if configss['h_freq'] is not None else None 
    raw_filtered = raw.filter(l_freq=l_freq, h_freq=h_freq,
                                         picks = data_channels)

    notch_freqs = configss['notch_freqs'] if configss['notch_freqs'] is not \
        None else None 

    raw_filtered =  raw_filtered.notch_filter(freqs=notch_freqs,
                                             picks= data_channels)

    return  raw_filtered


def eventEpochdata(raw):
    # get events and event dict 
    events_from_annot, event_dict =  mne.events_from_annotations(raw)

    stimcodes =  tools.helpers.getOVStimCodes()
    stimGroups = tools.helpers.getStimGroups()

    inv_stimCodesMap =  { v: k for k, v in stimcodes.items()}
    inv_stimGroupsMap = { v: k for k, v in stimGroups.items() }
    modified_event_dict =  { inv_stimGroupsMap[inv_stimCodesMap[int(k)]] :v for k,v in event_dict.items()}

    # only select events related to odd and the frequent stimuli
    epoch_event_dict =  {k:v for k, v in modified_event_dict.items() if 'freq' in k}     

    tmin = configss['epoch_tmin'] if configss['epoch_tmin'] is not None else None 
    tmax = configss['epoch_tmax'] if configss['epoch_tmax'] is not None else None

    # reject high amplitude signals, could be artifacts
    reject_criteria = dict(eeg=100e-6)  # 100 µV

    # baseline correction
    baseline_correction_l = configss['baseline_correction_l'] if configss['baseline_correction_l'] is not None else None 
    baseline_correction_h = configss['baseline_correction_h'] if configss['baseline_correction_h'] is not None else None

    epochs = mne.Epochs(raw, events_from_annot, event_id=epoch_event_dict, tmin=tmin, tmax=tmax, preload=True, reject=reject_criteria, baseline=(baseline_correction_l, baseline_correction_h))

    return epochs, epoch_event_dict


def plot():
    pass