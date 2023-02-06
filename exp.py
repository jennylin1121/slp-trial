from psychopy import visual, core, event, gui, data
from psychopy.tools.filetools import fromFile, toFile
from psychopy.hardware import keyboard
from trial import TrialObjects, TrialObject, TrialProcess
import numpy as np
import pandas as pd
import random


WIN = None
OBJS = None
FIXATION = None

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
    



def main():
    global WIN, OBJS, FIXATION
    
    trp = TrialProcess(WIN, OBJS)
    trp.run()



if __name__ == '__main__':
    __init__()
    main()
    __del__()
    