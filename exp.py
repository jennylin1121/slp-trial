from psychopy import visual, core, event, gui, data, sound
from psychopy.tools.filetools import fromFile, toFile
from psychopy.hardware import keyboard
from trial import TrialObjects, TrialObject, TrialProcess
import numpy as np
import pandas as pd
import random
import os


WIN = None
PRACTICE_OBJS = None
STAGE1_OBJS = None
NUM_OF_PRACTICES = 10
NUM_OF_STAGE1_OBJECTS = 10

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
    global WIN, STAGE1_OBJS, PRACTICE_OBJS
    WIN = visual.Window(allowGUI=False, screen=0,
                        monitor="testMonitor", units="deg", fullscr=True,
                        color=[255, 255, 255])
    WIN.mouseVisible = False
    
    def prepare_objs(config_file_name, photo_dir_name):
        objs = []
        df = pd.read_csv(config_file_name)
        for i in range(df.shape[0]):
            objs.append(TrialObjects(WIN, photo_dir_name, df.values[i]))
        return objs
    
    STAGE1_OBJS = prepare_objs("./stage1.csv", "./photos_stage1/")
    PRACTICE_OBJS = prepare_objs("./practice.csv", "./practice/")
                        
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
    

def practice():
    global WIN, PRACTICE_OBJS, NUM_OF_PRACTICES
    if NUM_OF_PRACTICES > len(PRACTICE_OBJS):
        NUM_OF_PRACTICES = len(PRACTICE_OBJS)
        
    objs = random.sample(PRACTICE_OBJS, NUM_OF_PRACTICES)

    
    practice_trial_set = []
    for i in range(NUM_OF_PRACTICES):
        trial_objs = objs[i].get_trial_objects()
        practice_trial_set.append(trial_objs[0])
        
    trp = TrialProcess(WIN, objs)
    
    trp.run(practice_trial_set, True)
    

def stage1():
    global WIN, STAGE1_OBJS

    if len(STAGE1_OBJS) < NUM_OF_STAGE1_OBJECTS:
        objs = STAGE1_OBJS
    else:
        objs = random.sample(STAGE1_OBJS, NUM_OF_STAGE1_OBJECTS)
    
    trp = TrialProcess(WIN, objs)
    dt = trp.run()
    
    df = pd.DataFrame.from_dict(dt)
    output_stage1_data(df)
    

def halt_and_show_msg(text, sec=5, keyList=None):
    global WIN
    
    text_stim = visual.TextStim(WIN, text=text, 
        color=[0, 0, 0], font="Songti SC")
    text_stim.size = 2
    text_stim.draw()
    WIN.flip()
    event.waitKeys(sec, keyList=keyList)
    WIN.flip()


if __name__ == '__main__':
    dialogue_window()
    __init__()
    halt_and_show_msg("練習開始")
    practice()
    halt_and_show_msg("練習結束")
    stage1()
#    halt_and_show_msg("""
#    Thank you for your participation
#    Supervisor : 
#    Research Assistant : Lin, Chia-Yi
#    Art Director : 
#    Programmer : Lin, Yu-Chun
#    """)
    halt_and_show_msg("""
    感謝您的參與
    指導教授：
    實驗設計：林佳怡
    美術設計：XXX、楊朝琮
    程式設計：林友鈞
    """)

    __del__()
    