from psychopy import visual, core, event, gui, data
from psychopy.tools.filetools import fromFile, toFile
from psychopy.hardware import keyboard
from trial import TrialObjects, TrialObject, TrialProcess
import numpy as np
import pandas as pd
import random
import os


WIN = None
OBJS = None
FIXATION = None

def dialogue_window():
    global EXPINFO
    try:
        EXPINFO = fromFile('stage1LastParams.pickle')
    except:
        EXPINFO = {'observer' : '', 'number': ''}
    EXPINFO['dateStr'] = data.getDateStr()

    dlg = gui.DlgFromDict(EXPINFO, title='Simple SLP Exp', fixed=['dateStr'])
    if dlg.OK:
        toFile('stage1LastParams.pickle', EXPINFO) # save params to file for next time
    else:
        core.quit()

def __init__():
    global WIN, OBJS, FIXATION
    WIN = visual.Window(allowGUI=False, screen=0,
                        monitor="testMonitor", units="deg", fullscr=True,
                        color=[255, 255, 255])
    
    FIXATION = visual.GratingStim(WIN, color=[0, 0, 0], colorSpace='rgb', 
                            tex=None, mask='cross', size=1)
    
    OBJS = []
    stg1_df = pd.read_csv("./stage1.csv")
    for i in range(stg1_df.shape[0]):
        OBJS.append(TrialObjects(WIN, "./photos_stage1/", stg1_df.values[i]))
                        
def __del__():
    global WIN
    if WIN != None:
        WIN.close()
    core.quit()

def output_stage1_data(df):
    global EXPINFO
    dirname = "stage1_data"
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    filename = os.path.join(dirname,
        EXPINFO['observer'] + EXPINFO['dateStr'] + '.csv')
    df.to_csv(filename)
    

def main():
    global WIN, OBJS, FIXATION
    
    trp = TrialProcess(WIN, OBJS)
    data = trp.run()
    
    df = pd.DataFrame.from_dict(data)
    output_stage1_data(df)


if __name__ == '__main__':
    dialogue_window()
    __init__()
    main()
    __del__()
    