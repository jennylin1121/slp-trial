from psychopy import visual, core, event, gui, data, sound
from psychopy.tools.filetools import fromFile, toFile
from psychopy.hardware import keyboard
from trial import TrialObjects, TrialObject, AudioTrialObjects, AudioTrialObject, TrialProcess
import numpy as np
import math
import pandas as pd
import random
import os


WIN = None
STAGE1_PRACTICE_OBJS = None
STAGE1_FORMER_OBJS = None
STAGE1_LATTER_OBJS = None

STAGE2_PRACTICE_OBJS = None
STAGE2_FORMER_OBJS = None
STAGE2_LATTER_OBJS = None
REST_IMG = None

NUM_OF_PRACTICES = 10
NUM_OF_STAGE1_OBJECTS = 10

TYPE = '1'

def dialogue_window():
    global EXPINFO, TYPE
    try:
        EXPINFO = fromFile('LastParams.pickle')
    except:
        EXPINFO = {'Participant' : '', 'Number': '', 'Gender' : '', 'Age':'', 'type' : '1'}
    EXPINFO['dateStr'] = data.getDateStr()

    dlg = gui.DlgFromDict(EXPINFO, title='Simple SLP Exp', fixed=['dateStr'])
    if dlg.OK:
        toFile('LastParams.pickle', EXPINFO) # save params to file for next time
    else:
        core.quit()
    TYPE = EXPINFO['type']

def __init__():
    global WIN, STAGE1_FORMER_OBJS, STAGE1_LATTER_OBJS, STAGE1_PRACTICE_OBJS
    global STAGE2_FORMER_OBJS, STAGE2_LATTER_OBJS, STAGE2_PRACTICE_OBJS
    global REST_IMG, REST_SOUND_EFFECT
        
    WIN = visual.Window(allowGUI=False, screen=0,
                        monitor="testMonitor", units="deg", fullscr=True,
                        color=[255, 255, 255])
    WIN.mouseVisible = False
    
    def prepare_trial_objs(config_file_name, photo_dir_name):
        objs = []
        df = pd.read_csv(config_file_name)
        for i in range(df.shape[0]):
            objs.append(TrialObjects(WIN, photo_dir_name, df.values[i]))
        assert isinstance(objs, list)
        return objs
    
    def prepare_audio_trial_objs(config_file_name, photo_dir_name, audio_dir_name):
        objs = []
        df = pd.read_csv(config_file_name)
        for i in range(df.shape[0]):
            objs.append(AudioTrialObjects(WIN, photo_dir_name, audio_dir_name, df.values[i]))
        assert isinstance(objs, list)
        return objs
    
    STAGE1_FORMER_OBJS = prepare_trial_objs('./trials/stage1_former.csv', './resources/photos/')
    STAGE1_LATTER_OBJS = prepare_trial_objs('./trials/stage1_latter.csv', './resources/photos/')
    STAGE1_PRACTICE_OBJS = prepare_trial_objs('./trials/stage1_practice.csv', './resources/photos/')
    
    STAGE2_FORMER_OBJS = prepare_audio_trial_objs("./trials/stage2_former.csv", "./resources/photos/", "./resources/audio/")
    STAGE2_LATTER_OBJS = prepare_audio_trial_objs("./trials/stage2_latter.csv", "./resources/photos/", "./resources/audio/")
    STAGE2_PRACTICE_OBJS = prepare_audio_trial_objs("./trials/stage2_practice.csv", "./resources/photos/", "./resources/audio/")
    
    REST_IMG = visual.ImageStim(WIN, "./resources/photos/rest.png")
    REST_SOUND_EFFECT = sound.Sound("./resources/audio/rest.wav")

def __del__():
    global WIN
    if WIN != None:
        WIN.close()
    core.quit()
    
def instructions():
    global WIN
    scenes = [
        {
            "img" : visual.ImageStim(WIN, "./resources/photos/village.jpeg"),
            "audio" : sound.Sound("./resources/audio/village.wav"),
            "skip_key" : 'escape'
        },
        {
            "img" : visual.ImageStim(WIN, "./resources/photos/monster1.png"),
            "audio" : sound.Sound("./resources/audio/monster1-1.wav")
        },
        {
            "img" : visual.ImageStim(WIN, "./resources/photos/monster1.png"),
            "audio" : sound.Sound("./resources/audio/monster1-2.wav")
        },
        {
            "img" : visual.ImageStim(WIN, "./resources/photos/monster2.png"),
            "audio" : sound.Sound("./resources/audio/monster2.wav")
        },
        {
            "img" : visual.ImageStim(WIN, "./resources/photos/desert.jpeg"),
            "audio" : sound.Sound("./resources/audio/desert.wav"),
        },
        {
            "img" : visual.ImageStim(WIN, "./resources/photos/instruction1.jpeg"),
            "audio" : sound.Sound("./resources/audio/instruction1.wav"),
        },
        {
            "img" : visual.ImageStim(WIN, "./resources/photos/instruction2.jpeg"),
            "audio" : sound.Sound("./resources/audio/instruction2.wav"),
        }
    ]
    
    for i in range(len(scenes)):
        sound_duration = scenes[i]['audio'].getDuration()
        if scenes[i]["audio"] != None:
            scenes[i]["audio"].play()
        scenes[i]["img"].draw()
        WIN.flip()
        if 'skip_key' in scenes[i].keys():
            keys = event.waitKeys(sound_duration, keyList=[scenes[i]["skip_key"]])
            if keys != None:
                scenes[i]['audio'].pause()
                break
        else:
            core.wait(sound_duration)
    
    halt_and_show_msg("準備好了嗎? press any key to continue", sec=math.inf, size=1)
    
def ending_scene():
    
    fleeting_sound = sound.Sound("./resources/audio/fleeting.wav")
    fleeting_img = visual.ImageStim(WIN, "./resources/photos/fleeting.png")
    fleeting_img.size *= 0.5
    fleeting_img.draw()
    WIN.flip()
    fleeting_sound.play()
    event.waitKeys(fleeting_sound.getDuration())
    
    

def output_data(data):
    global EXPINFO
    dirname = "experiment_data"
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    
    data_dirname = os.path.join(dirname, "data")
    if not os.path.exists(data_dirname):
        os.mkdir(data_dirname)
    
    filename = os.path.join(data_dirname,
        EXPINFO['Participant'] + EXPINFO['dateStr'] + '.xlsx')
    
    df = pd.DataFrame.from_dict(data)
    df.to_excel(filename)
    
    return df
    
def update_overview(data):
    dirname = "experiment_data"
    filename = os.path.join(dirname, "overview.xlsx")
    
    expinfo = EXPINFO
    
    for key in data:
        df = pd.DataFrame.from_dict(data[key])
        print(df)
        try:
            expinfo[key + '_average_response_time'] = df['response_time'].mean()
            expinfo[key + '_correctness_rate'] = df['correct'].mean()
        except:
            expinfo[key + '_average_response_time'] = 0
            expinfo[key + '_correctness_rate'] = 0
        
    
    info = [expinfo]
    info_df = pd.DataFrame(info)
    
    if os.path.exists(filename):
        overview_df = pd.read_excel(filename)
        overview_df = pd.concat([overview_df, info_df])
    else:
        overview_df = info_df
    
    overview_df.to_excel(filename, index=False)
    
def the_end_of_stage_scene(text):
    REST_SOUND_EFFECT.play()
    halt_and_show_msg(text, sec=max(REST_SOUND_EFFECT.getDuration(), 5))
    
    
def stage1_former_latter(data, start_no_round, final=False):
    halt_and_show_msg("Stage1 練習開始")
    practice(STAGE1_PRACTICE_OBJS)
    halt_and_show_msg("Stage1 練習結束")
    data['stage1_former'] = perform_experiment(STAGE1_FORMER_OBJS, start_no_round)
    the_end_of_stage_scene("The end of stage1 former")
    rest()
    
    data['stage1_latter'] = perform_experiment(STAGE1_LATTER_OBJS, start_no_round + 1)
    the_end_of_stage_scene("The end of stage1 latter")
    if not final:
        rest()
    
def stage1_latter_former(data, start_no_round, final=False):
    halt_and_show_msg("Stage1 練習開始")
    practice(STAGE1_PRACTICE_OBJS)
    halt_and_show_msg("Stage1 練習結束")
    data['stage1_latter'] = perform_experiment(STAGE1_LATTER_OBJS, start_no_round)
    the_end_of_stage_scene("The end of stage1 latter")
    rest()
    
    data['stage1_former'] =  perform_experiment(STAGE1_FORMER_OBJS, start_no_round + 1)
    the_end_of_stage_scene("The end of stage1 former")
    if not final:
        rest()
    
def stage2_former_latter(data, start_no_round, final=False):
    halt_and_show_msg("Stage2 練習開始")
    practice(STAGE2_PRACTICE_OBJS)
    halt_and_show_msg("Stage2 練習結束")
    data['stage2_former'] = perform_experiment(STAGE2_FORMER_OBJS, start_no_round)
    the_end_of_stage_scene("The end of stage2 former")
    rest()
    
    data['stage2_latter'] = perform_experiment(STAGE2_LATTER_OBJS, start_no_round + 1)
    the_end_of_stage_scene("The end of stage2 latter")
    if not final:
        rest()
    

def stage2_latter_former(data, start_no_round, final=False):
    halt_and_show_msg("Stage2 練習開始")
    practice(STAGE2_PRACTICE_OBJS)
    halt_and_show_msg("Stage2 練習結束")
    data['stage2_latter'] = perform_experiment(STAGE2_LATTER_OBJS, start_no_round)
    the_end_of_stage_scene("The end of stage2 latter")
    rest()
    
    data['stage2_former'] = perform_experiment(STAGE2_FORMER_OBJS, start_no_round + 1)
    the_end_of_stage_scene("The end of stage2 former")
    if not final:
        rest()
   
   
    
def type1():
    data = {}
    
    # stage1 : practice -> former -> latter
    stage1_former_latter(data, 1)
    
    # rest
    rest()

    # stage2 : practice -> former -> latter
    stage2_former_latter(data, 3, True)
    
    return data

def type2():
    data = {}
    
    # stage1 : practice -> latter -> former
    stage1_latter_former(data, 1)

    # rest
    rest()
    
    # stage2 : practice -> latter -> former
    stage2_latter_former(data, 3, True)
    
    return data
    
def type3():
    data = {}

    # stage2 : practice -> former -> latter
    stage2_former_latter(data, 1)
    
    # rest
    rest()
    
    # stage1 : practice -> latter -> former
    stage1_latter_former(data, 3, True)
    
    return data
    
def type4():
    
    data = {}
    # stage2 : practice -> latter -> former
    stage2_latter_former(data, 1)
    
    # rest
    rest()
    
    # stage1 : practice -> former -> latter
    stage1_former_latter(data, 3, True)
    
    
    return data
    

def practice(practice_objs):
    global WIN, PRACTICE_OBJS, NUM_OF_PRACTICES
    if NUM_OF_PRACTICES > len(practice_objs):
        NUM_OF_PRACTICES = len(practice_objs)
        
    objs = random.sample(practice_objs, NUM_OF_PRACTICES)
    practice_trial_set = []
    for i in range(NUM_OF_PRACTICES):
        trial_objs = objs[i].get_trial_objects()
        practice_trial_set.append(trial_objs[0])
        
    trp = TrialProcess(WIN, objs)
    trp.run(practice_trial_set, True, 3)
    

def perform_experiment(stage_objs, no_round):
    global WIN
    
    trp = TrialProcess(WIN, stage_objs, no_round)
    dt = trp.run()
    
    return dt
    

def halt_and_show_msg(text, sec=5, keyList=None, size=2):
    global WIN
    
    text_stim = visual.TextStim(WIN, text=text, 
        color=[0, 0, 0], font="Songti SC")
    text_stim.size = size
    text_stim.draw()
    WIN.flip()
    event.waitKeys(sec, keyList=keyList)
    WIN.flip()

def rest():
#    text_stim = visual.TextStim(WIN, text="Rest", 
#        color=[0, 0, 0], font="Songti SC")
#    text_stim.size = 2
#    text_stim.draw()
    REST_IMG.draw()
    WIN.flip()
    keys1 = event.waitKeys(keyList=['lctrl'])
    keys2 = event.waitKeys(keyList=['w'])
    WIN.flip()

if __name__ == '__main__':
    dialogue_window()
    __init__()
    instructions()
    data = eval("type"+TYPE)()
    ending_scene()
    
    combined_data = []
    for key in data:
        combined_data += data[key]
    
    df = output_data(combined_data)
    
    update_overview(data)
    
#    halt_and_show_msg("""
#    Thank you for your participation
#    Supervisor : 
#    Research Assistant : Lin, Chia-Yi
#    Art Director : 
#    Programmer : Lin, Yu-Chun
#    """)
#    halt_and_show_msg("""
#    感謝您的參與
#    指導教授：
#    實驗設計：林佳怡
#    美術設計：XXX、楊朝琮
#    程式設計：林友鈞
#    """)

    __del__()
