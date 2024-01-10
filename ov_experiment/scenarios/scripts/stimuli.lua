stimcodes = {
    experiment_start=OVTK_StimulationId_ExperimentStart,
    experiment_stop=OVTK_StimulationId_ExperimentStop,
    trial_start=OVTK_StimulationId_TrialStart,
    trial_stop=OVTK_StimulationId_TrialStop,
    fixation_cross=OVTK_GDF_Cross_On_Screen,
    clear_screen=OVTK_StimulationId_VisualStimulationStop,
    instructions={
        set_0 ={  
        OVTK_StimulationId_Label_A0,
        OVTK_StimulationId_Label_A1},
        set_1 ={ blk_strt = OVTK_StimulationId_Label_B0,
        blk_end = OVTK_StimulationId_Label_B1},
        set_2 ={
        exp_end = OVTK_StimulationId_Label_B2}
    },
    shapes={
        non_freq=OVTK_StimulationId_Label_01,
        freq=OVTK_StimulationId_Label_02,
    }
}