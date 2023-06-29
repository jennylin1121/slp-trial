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
    
    def __init__(self, window, img, word1, word2, ans, _type):
        """
        Parameters
        ----------
        window : psychopy.visual.Window
            an object used to display the stimuli
        img : psychopy.visual.ImageStim
            an image stimulus that show the object in the trial
        word1 : str
            the first word that will be shown on the screen for participants
        word2 : str
            the second word that will be shown on the screen for participants
        ans : str
            the ans will be a single key and it will be used to check if
            participants' answer is correct or not.

            For example: initially, the ans is set to be 'q'. In the trial
            process, the object will check if the user's input is 'q' or other
            keys. If the user's input is 'q', the user pass this trial.
        """
        self.__img = img
        self.__word1_name = word1
        self.__word2_name = word2
        self.__window = window
        self.__type = _type
        
        self.__word1 = visual.TextStim(window, text=word1, 
            colorSpace='rgb', font="Songti SC", color=[0, 0, 0])
        self.__word2 = visual.TextStim(window, text=word2, 
            colorSpace='rgb', font="Songti SC", color=[0, 0, 0])
        
        self.__word1.size = self.__word2.size = WORD_SIZE

        
        self.__ans = ans
        self.__response_time = 0
        self.__key = None
        
    def display(self, flip=True):
        """Display the stimulus of the trial object and wait for a fix specific
        time interval. The time interval is PHOTO_DISPLAY_INTERVAL. The function
        will listen to the keyboard event. When the user type the 'escape' key,
        the function will immediately return. The return value will be a key
        list, but normally, the list will only contain a single key, the
        'escape' key.

        Parameters
        ----------
        flip : Boolean, optional
            if flip is set the True, the window will flip automatically, which
            means that the image or orther kind of visual sitmulus will appear
            on the screen immediately.

        Returns
        -------
        list : 
            a key list that only contains the 'escape' key, if the user
            types the 'escape' key on the keyboard when the object displayes.
        None : 
            if user doesn't type any key during the interval that the object
            displayes.
        """
        self.__img.draw()
        if flip:
            self.__window.flip()
        key = event.waitKeys(PHOTO_DISPLAY_INTERVAL, keyList=['escape'])
        return key
    
    def display_image(self, flip=True):
        """Display the image of the trial object

        Parameters
        ----------
        flip : Boolean, optional, default is True
            if flip is set the True, the window will flip automatically, which
            means that the image will appear on the screen immediately.
        """
        self.__img.draw()
        if flip:
            self.__window.flip()
        
    def display_word1(self, flip=True):
        """Display the word1 of the trial object and wait for a fixed specific
        time interval. The time interval is set to be WORD1_DISPLAY_INTERVAL.

        Parameters
        ----------
        flip : Boolean, optional, default is True
            if flip is set the True, the window will flip automatically, which
            means that the image will appear on the screen immediately.

        Returns
        -------
        a list that contains keys that are pushed during the interval that 
        word1 is display.
        """
        self.__word1.draw()
        if flip:
            self.__window.flip()
        keys = event.waitKeys(WORD1_DISPLAY_INTERVAL, 
                keyList=['q','p', 'escape'])
        return keys
    
    def display_word2(self, flip=True):
        """Display the word1 of the trial object and wait for a fixed specific
        time interval. The time interval is set to be WORD2_DISPLAY_INTERVAL.

        Parameters
        ----------
        flip : Boolean, optional, default is True
            if flip is set the True, the window will flip automatically, which
            means that the image will appear on the screen immediately.
        
        Returns
        -------
        a list that contains keys that are pushed during the interval that 
        word2 is display.
        """

        self.__word2.draw()
        if flip:
            self.__window.flip()
        keys = event.waitKeys(WORD2_DISPLAY_INTERVAL, 
                keyList=['q','p', 'escape'])
        return keys
        
        
    def response(self, key, clk):
        """Save user's response and the reaction time then return the 
        correctness and the content of the object
        
        Parameters
        ----------
        key : str 
            user's input
        clk : int, float
            user's response time
            
        Returns
        -------
        A dictionary that contains two words, user's response time, and 
        his/her reaction time
        """
        self.__response_time = clk
        if key == None:
            crt = 'no response'
        else:
            self.__key = key[0]
            crt = self.is_correct()
        
        return {"response_time" : self.__response_time,
                "word1" : self.__word1_name,
                "word2" : self.__word2_name,
                "correct" : crt,
                "type" : self.__type}
        
    def is_correct(self, ans=None):
        """Check if user's key input is correct or not
        
        Parameters
        ----------
        ans : str, Optional
            specifies the ans of this trial object
        
        Returns
        -------
        return True if user's input is correct or return False
        """
        if ans == None:
            return self.__key == self.__ans
        else:
            return ans == self.__ans
        
    def words(self):
        """Get two words of the trial object
        
        Returns
        -------
        Two words that are string type
        """
        return self.__word1_name, self.__word2_name
        
    def type(self):
        """The type of the test
        
        Returns
        -------
        A chinese string that representsthe type of the test
        """
        return self._type


class TrialObjects(object):
    """
    A class used to represent a set of trial objects
    
    A set of trial objects includes an image, a correct vocabulary to 
    describe the picture, and 4 incorrect word to test the experiment 
    participants. The picuture will display a thing which
    may be a rabbit, a mountain, a bed and etc...
    
    """
    
    def __init__(self, win, dir_path, array):
        """
        """
        
        self.name = array['目標詞彙']
        self.test = array[1:]
        self.img = visual.ImageStim(win, dir_path + self.name + ".jpeg")
        self.img.size *= 0.5
        
        self.trial_objects = []
        
        for key, value in self.test.items():
            self.trial_objects.append(
                TrialObject(win, self.img, 
                    self.name, value, 'q', key))
            self.trial_objects.append(
                TrialObject(win, self.img, value,
                    self.name, 'p', key))
        
    def get_trial_objects(self):
#        return self.__trial_objects
        return random.sample(self.trial_objects, len(self.trial_objects))
    
class AudioTrialObject(TrialObject):
    
    def __init__(self, window, img, audio, word1, word2, ans, _type):
        self.__window = window
        super().__init__(window, img, word1, word2, ans, _type)
        self.__audio = audio
    
    def display(self, flip=True):
        self.__audio.play()
        return super().display(flip)

class AudioTrialObjects(TrialObjects):
    
    def __init__(self, window, img_directory_path, audio_directory_path, array):
        self.name = array[0]
        self.test = array[1:]
        self.img = visual.ImageStim(window, img_directory_path + self.name + ".jpeg")
        self.audio = sound.Sound(audio_directory_path + self.name + ".wav")
        self.img.size *= 0.5
        
        self.trial_objects = []
        for key, value in self.test.items():
            self.trial_objects.append(AudioTrialObject(window, self.img, 
                self.audio, self.name, value, 'q', key))
            self.trial_objects.append(AudioTrialObject(window, self.img,
                self.audio, value, self.name, 'p', key))
                
        

class TrialProcess(object):
    
    def __init__(self, win, trial_objs_set, no_round=None):
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
        
        self.setup_round_scene(no_round)
        
    def setup_round_scene(self, no_round):
        if no_round != None:
            self.__round_img = visual.ImageStim(self.__win, "./resources/photos/round%d.png" % no_round)
            self.__shot_effect = sound.Sound("./resources/audio/round%d_shot.wav" % no_round)
            self.__round_sound = sound.Sound("./resources/audio/round%d.wav" % no_round)
        else:
            self.__round_img = None
            self.__shot_effect = None
            self.__round_sound = None
            
     
    def show_right_feedback(self):
        self.__right_feedback_img.draw()
        self.__right_sound_effect.play()
        self.__win.flip()
        
    def show_false_feedback(self):
        self.__false_feedback_img.draw()
        self.__false_sound_effect.play()
        self.__win.flip()
                        
    def run(self, trial_objs=None, reaction=False, max_correctness=math.inf):
        data = []
        if trial_objs == None:
            trial_objs = self.__all_trial_objs
            
        
        self.__correctness = 0
        
        def __shot():
            if self.__shot_effect != None:
                self.__shot_effect.play()
        
        def __show_reaction(obj, reaction):
            __shot()
            self.__win.flip()
            if reaction:
                if obj.is_correct():
                    self.show_right_feedback()
                    self.__correctness += 1
                else:
                    self.show_false_feedback()
                event.waitKeys(2)
        
        if self.__round_img != None and self.__round_sound != None:
            self.__round_img.draw()
            self.__win.flip()
            self.__round_sound.play()
            core.wait(self.__round_sound.getDuration())
        
        i = 0
        while i < len(trial_objs) and self.__correctness < max_correctness:
            obj = trial_objs[i]
            i += 1
            
            # display cross
            self.__fixation.draw()
            self.__win.flip()
            keys = event.waitKeys(CROSS_DISPLAY_INTERVAL, keyList=['escape'])
            if keys != None:
                break
            
            # the interval between the cross and the photo
            self.__win.flip()
            keys = event.waitKeys(CROSS_PHOTO_INTERVAL, keyList=['escape'])
            if keys != None:
                break
            
            # display the photo
            keys = obj.display()
            if keys != None:
                break
            self.__win.flip()
            
            # the interval between the photo and the word1
            keys = event.waitKeys(PHOTO_WORD1_INTERVAL, keyList=['escape'])
            if keys != None:
                break
            
            # start measuring the repsonse time
            clk = core.Clock()
            
            # show the first word and wait for WORD1_DISPLAY_INTERVAL
            keys = obj.display_word1()
            
                
            
            # check if the subject has responsed or not
            if keys != None:
                if 'escape' in keys:
                    break
                else:
                    data.append(obj.response(keys, clk.getTime()))
                    __show_reaction(obj, reaction)
                    continue
                    
            # clear the first word and wait for WORD1_WORD2_INTERVAL
            self.__win.flip()
            keys = event.waitKeys(WORD1_WORD2_INTERVAL, 
                keyList=['q','p', 'escape'])
            
            # check the response
            if keys != None:
                if 'escape' in keys:
                    break
                else:
                    data.append(obj.response(keys, clk.getTime()))
                    __show_reaction(obj, reaction)
                    continue
                
            # show the next word and wait for WORD2_DISPLAY_INTERVAL
            keys = obj.display_word2()
            
            # check the response
            if keys != None:
                if 'escape' in keys:
                    break
                else:
                    data.append(obj.response(keys, clk.getTime()))
                    __show_reaction(obj, reaction)
                    continue
            
            # clear the seconde word and wait for WORD2_CROSS_INTERVAL
            self.__win.flip()
            keys = event.waitKeys(WORD2_CROSS_INTERVAL, keyList=['q','p', 'escape'])
            
            if keys != None:
                if 'escape' in keys:
                    break
                else:
                    data.append(obj.response(keys, clk.getTime()))
                    __show_reaction(obj, reaction)
                    continue

                    
        return data
    
