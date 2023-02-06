from psychopy import visual, core, event, gui, data
from psychopy.tools.filetools import fromFile, toFile
from itertools import product
import numpy as np
import pandas as pd
import random

CROSS_DISPLAY_INTERVAL = 1
CROSS_PHOTO_INTERVAL = 0.4
PHOTO_DISPLAY_INTERVAL = 1
PHOTO_WORD1_INTERVAL = 0.4
WORD1_DISPLAY_INTERVAL = 0.5
WORD1_WORD2_INTERVAL = 0.4
WORD2_DISPLAY_INTERVAL = 0.5
WORD2_CROSS_INTERVAL = 0.4

WORD_SIZE = 3

class TrialObjects(object):
    
    def __init__(self, win, dir_path, array):
        self.__name = array[0]
        self.__test = array[1:]
        self.__img = visual.ImageStim(win, dir_path + self.__name + ".jpeg")
        self.__img.size *= 0.5
        
        self.__trial_objects = []
        
        for wrong_ans in self.__test:
            self.__trial_objects.append(
                TrialObject(win, self.__img, 
                    self.__name, wrong_ans, 'q'))
            self.__trial_objects.append(
                TrialObject(win, self.__img, wrong_ans, 
                    self.__name, 'p'))
    
    def display(self):
        self.__img.draw()
        
    def get_trial_objects(self):
#        return self.__trial_objects
        return random.sample(self.__trial_objects, len(self.__trial_objects))
        
        
class TrialObject(object):
    
    def __init__(self, win, img, word1, word2, ans):
        self.__img = img
        self.__word1_name = word1
        self.__word2_name = word2
        
        self.__word1 = visual.TextStim(win, text=word1, 
            colorSpace='rgb', font="Songti SC", color=[0, 0, 0])
        self.__word2 = visual.TextStim(win, text=word2, 
            colorSpace='rgb', font="Songti SC", color=[0, 0, 0])
        
        self.__word1.size = self.__word2.size = WORD_SIZE

        
        self.__ans = ans
        self.__response_time = 0
        
    def display(self):
        self.__img.draw()
        
    def display_word1(self):
        self.__word1.draw()
    
    def display_word2(self):
        self.__word2.draw()
        
    def response(self, key, clk):
        self.__response_time = clk
        print("response : ", key)
        if key == None:
            crt = 'no response'
        else:
            self.__key = key[0]
            crt = str(self.is_correct())
        
        return {"response_time" : self.__response_time,
                "word1" : self.__word1_name,
                "word2" : self.__word2_name,
                "correct" : crt}
        
    def is_correct(self, ans=None):
        if ans == None:
            print("key is ", self.__key)
            return self.__key == self.__ans
        else:
            return ans == self.__ans
        
    def words(self):
        return self.__word1_name, self.__word2_name
        

class TrialProcess(object):
    
    def __init__(self, win, trial_objs_set):
        self.__win = win
        self.__trial_objs_set = trial_objs_set
        self.__fixation = visual.GratingStim(self.__win, color=[0, 0, 0], 
                        colorSpace='rgb', tex=None, mask='cross', size=1)
                        
        self.__slow_alert_text = visual.TextStim(self.__win, 
            text="快一點啦幹", color=[0, 0, 0], font="Songti SC")
        
        self.__slow_alert_text.size = WORD_SIZE
                        
        self.__all_trial_objs = []
        # yield all trial objects
        for obj in self.__trial_objs_set:
            self.__all_trial_objs += obj.get_trial_objects()
        
        # Should I randomize the test set here?
        self.__all_trial_objs = random.sample(self.__all_trial_objs, 
            len(self.__all_trial_objs))
        
            
                        
    def run(self):
        
        data = []
        
        for obj in self.__all_trial_objs:
            # display cross
            self.__fixation.draw()
            self.__win.flip()
            key = event.waitKeys(CROSS_DISPLAY_INTERVAL, keyList=['escape'])
            if key != None:
                break
            
            # the interval between the cross and the photo
            self.__win.flip()
            key = event.waitKeys(CROSS_PHOTO_INTERVAL, keyList=['escape'])
            if key != None:
                break
            
            # display the photo
            obj.display()
            self.__win.flip()
            key = event.waitKeys(PHOTO_DISPLAY_INTERVAL, keyList=['escape'])
            if key != None:
                break
            self.__win.flip()
            
            # the interval between the photo and the word1
            key = event.waitKeys(PHOTO_WORD1_INTERVAL, keyList=['escape'])
            if key != None:
                break
            
            # start measuring the repsonse time
            clk = core.Clock()
            
            # show the first word and wait for WORD1_DISPLAY_INTERVAL
            obj.display_word1()
            self.__win.flip()
            key = event.waitKeys(WORD1_DISPLAY_INTERVAL, 
                keyList=['q','p', 'escape'])
            
            # check if the subject has responsed or not
            if key != None:
                if 'escape' in key:
                    break
                else:
                    data.append(obj.response(key, clk.getTime()))
                    continue
                
            # clear the first word and wait for WORD1_WORD2_INTERVAL
            self.__win.flip()
            key = event.waitKeys(WORD1_WORD2_INTERVAL, 
                keyList=['q','p', 'escape'])
            
            # check the response
            if key != None:
                if 'escape' in key:
                    break
                else:
                    data.append(obj.response(key, clk.getTime()))
                    continue
                
            # show the next word and wait for WORD2_DISPLAY_INTERVAL
            obj.display_word2()
            self.__win.flip()
            key = event.waitKeys(WORD2_DISPLAY_INTERVAL, keyList=['q','p', 'escape'])
            
            # check the response
            if key != None:
                if 'escape' in key:
                    break
                else:
                    data.append(obj.response(key, clk.getTime()))
                    continue
            
            # clear the seconde word and wait for WORD2_CROSS_INTERVAL
            self.__win.flip()
            key = event.waitKeys(WORD2_CROSS_INTERVAL, keyList=['q','p', 'escape'])
            
            if key != None:
                if 'escape' in key:
                    break
                else:
                    data.append(obj.response(key, clk.getTime()))
                    continue
            else:
                # show the text that tells the user that his/her 
                # response is too slow
                self.__slow_alert_text.draw()
                self.__win.flip()
                data.append(obj.response(None, clk.getTime()))
                key = event.waitKeys(1, keyList=['escape'])
                if key != None:
                    break
                    
        return data
    