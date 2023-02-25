from psychopy import visual, core, event, gui, data, sound
from psychopy.tools.filetools import fromFile, toFile
from itertools import product
import psychtoolbox as ptb
import numpy as np
import pandas as pd
import random
import math

CROSS_DISPLAY_INTERVAL = 1
CROSS_PHOTO_INTERVAL = 0.4
PHOTO_DISPLAY_INTERVAL = 1
PHOTO_WORD1_INTERVAL = 0.4
WORD1_DISPLAY_INTERVAL = 0.5
WORD1_WORD2_INTERVAL = 0.4
WORD2_DISPLAY_INTERVAL = 0.5
WORD2_CROSS_INTERVAL = math.inf

WORD_SIZE = 3

class TrialObject(object):
    """
    A class used to represent a trial object
    
    A trial object includes a image and two words, which include a correct
    word and an incorrect word. The experiment participants must choose a 
    correct answer. 
    
    In each round of the trial process, the program will choose a trial 
    object and display its image firstly. Secondly, the screen will show two
    words with a short interval among them.The participants are required to
    press the p and q keys on the keyboard to choose the correct answer.
    
    Attributes
    ----------
    
    Methods
    -------
    
    """
    
    def __init__(self, window, img, word1, word2, ans):
        """
        Parameters
        ----------
        window : psychopy.visual.Window
            an object used to display the stimuli
        img : psychopy.visual.ImageStim
            an image stimulus that show the object in the trial
        word1 : 
        """
        self.__img = img
        self.__word1_name = word1
        self.__word2_name = word2
        self.__window = window
        
        self.__word1 = visual.TextStim(window, text=word1, 
            colorSpace='rgb', font="Songti SC", color=[0, 0, 0])
        self.__word2 = visual.TextStim(window, text=word2, 
            colorSpace='rgb', font="Songti SC", color=[0, 0, 0])
        
        self.__word1.size = self.__word2.size = WORD_SIZE

        
        self.__ans = ans
        self.__response_time = 0
        
    def display(self, flip=True):
        self.__img.draw()
        if flip:
            self.__window.flip()
        
    def display_word1(self, flip=True):
        self.__word1.draw()
        if flip:
            self.__window.flip()
    
    def display_word2(self, flip=True):
        self.__word2.draw()
        if flip:
            self.__window.flip()
        
        
    def response(self, key, clk):
        self.__response_time = clk
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
            return self.__key == self.__ans
        else:
            return ans == self.__ans
        
    def words(self):
        return self.__word1_name, self.__word2_name


class TrialObjects(object):
    """
    A class used to represent a set of trial objects
    
    A set of trial objects includes an image, a correct vocabulary to 
    describe the picture, and 4 incorrect word to test the experiment 
    participants. The picuture will display a thing which
    may be a rabbit, a mountain, a bed and etc...
    
    """
    
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
    
    def get_img_stim(self):
        return self.__img
        
        

        

class TrialProcess(object):
    
    def __init__(self, win, trial_objs_set):
        self.__win = win
        self.__trial_objs_set = trial_objs_set
        self.__fixation = visual.GratingStim(self.__win, color=[0, 0, 0], 
                        colorSpace='rgb', tex=None, mask='cross', size=WORD_SIZE)
                        
        self.__slow_alert_text = visual.TextStim(self.__win, 
            text="快點喔", color=[0, 0, 0], font="Songti SC")
        
        self.__slow_alert_text.size = WORD_SIZE
                        
        self.__all_trial_objs = []
        # yield all trial objects
        for obj in self.__trial_objs_set:
            self.__all_trial_objs += obj.get_trial_objects()
        
        # Should I randomize the test set here?
        self.__all_trial_objs = random.sample(self.__all_trial_objs, 
            len(self.__all_trial_objs))
        
        self.__right_feedback_img = visual.ImageStim(self.__win, "./resources/photos/right.jpeg")
        self.__false_feedback_img = visual.ImageStim(self.__win, "./resources/photos/fault.jpeg")
        self.__right_sound_effect = sound.Sound("./resources/audio/right_sound_effect.wav")
        self.__false_sound_effect = sound.Sound("./resources/audio/false_sound_effect.wav")
     
    def show_right_feedback(self):
        self.__right_feedback_img.draw()
        self.__right_sound_effect.play()
        self.__win.flip()
        
    def show_false_feedback(self):
        self.__false_feedback_img.draw()
        self.__false_sound_effect.play()
        self.__win.flip()
                        
    def run(self, trial_objs=None, reaction=False):
        data = []
        if trial_objs == None:
            trial_objs = self.__all_trial_objs
            
        def __show_reaction(obj, reaction):
            self.__win.flip()
            if reaction:
                if obj.is_correct():
                    self.show_right_feedback()
                else:
                    self.show_false_feedback()
                event.waitKeys(2)
            
        for obj in trial_objs:

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
            key = event.waitKeys(WORD1_DISPLAY_INTERVAL, 
                keyList=['q','p', 'escape'])
                
            
            # check if the subject has responsed or not
            if key != None:
                if 'escape' in key:
                    break
                else:
                    data.append(obj.response(key, clk.getTime()))
                    __show_reaction(obj, reaction)
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
                    __show_reaction(obj, reaction)
                    continue
                
            # show the next word and wait for WORD2_DISPLAY_INTERVAL
            obj.display_word2()
            key = event.waitKeys(WORD2_DISPLAY_INTERVAL, keyList=['q','p', 'escape'])
            
            # check the response
            if key != None:
                if 'escape' in key:
                    break
                else:
                    data.append(obj.response(key, clk.getTime()))
                    __show_reaction(obj, reaction)
                    continue
            
            # clear the seconde word and wait for WORD2_CROSS_INTERVAL
            self.__win.flip()
            key = event.waitKeys(WORD2_CROSS_INTERVAL, keyList=['q','p', 'escape'])
            
            if key != None:
                if 'escape' in key:
                    break
                else:
                    data.append(obj.response(key, clk.getTime()))
                    __show_reaction(obj, reaction)
                    continue
#            else:
#                # show the text that tells the user that his/her 
#                # response is too slow
#                self.__slow_alert_text.draw()
#                self.__win.flip()
#                data.append(obj.response(None, clk.getTime()))
#                key = event.waitKeys(1, keyList=['escape'])
#                if key != None:
#                    break
                    
        return data
    