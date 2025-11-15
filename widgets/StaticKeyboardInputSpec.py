from core.Difficulty import Difficulty
from messages.TypingComplete import TypingCompleted

from widgets.StaticKeyboardInput import StaticKeyboardInput

import time

from textual import log


#TODO: Encapsulate keyboard input from high-level typing-test functionality
class StaticKeyboardInputSpec(StaticKeyboardInput):
    can_focus = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.time_start = None
        self.time_end = None
        self.time_recent = None

        self.mismatches = set()

        self.timepoints = []

        self.difficulty = Difficulty.DEFAULT #TODO: Fix the default difficulty to app's default difficulty

    def update_text(self, new_text: str):
        super().update_text(new_text)
        
        self.time_start = None
        self.time_end = None
        self.timepoints = []
        
    def _render_text(self):
        super()._render_text()
        self._check_start_stop()

    def _calculate_accuracy(self):
        return 1-len(self.mismatches)/len(self.text_buffer)

    def _calculate_raw_wpm(self):
        return max((len(self.text_buffer.split())/self.time_recent)*60, ((len(self.text_buffer)/4.7)/self.time_recent)*60)
    
    def _calculate_raw_cpm(self):
        return (len( list(self.text_buffer) )/self.time_recent)*60 

    def _check_start_stop(self):
        if(self.cursor_pos > 1 and self.cursor_pos-1 < len(self.target_text)):
            self.timepoints.append(round(time.time() - self.time_start, 3))
        if(self.cursor_pos == 1):
            self.time_start = time.time()

        if(self.cursor_pos-1 == len(self.target_text)-1):
            self.time_end = time.time()
            
            #TODO: Add hit-ratio influence for the formulas
            self.time_recent = self.time_end - self.time_start

            wpm = self._calculate_raw_wpm()
            cpm = self._calculate_raw_cpm()

            accuraacy_info = f"{len(self.mismatches)}/{len(self.text_buffer)}/{round(self._calculate_accuracy()*100)}%"

            self.post_message(TypingCompleted(wpm, cpm, self.target_text, "", self.wordCount, accuraacy_info, self.timepoints))
            self.reset_text()