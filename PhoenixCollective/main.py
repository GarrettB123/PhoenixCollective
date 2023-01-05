#--------------------------------------#
# Title: main.py
# Desc: runs the main game loop
# Change Log: (Who, When, What)
#   Garrett Bachman, 2022-Dec-29, Created File
#   Garrett Bachman, 2022-Dec-29, Added header
#   Garrett Bachman, 2022-Dec-29, Added code
#--------------------------------------#

import re
import os
import sys
import board
import decks

class Main:
    def __init__(self):
        # initalize variables
        self._running = True
        self._is_p1_turn = True
        self.curr_step = None
        self._helpFile = None
        self.p1 = None
        self.p2 = None
        

    def on_init(self):
        # first references
        self.helpFile = open("help.txt", "r")
        self.p1 = board.Board(decks.decklist[int(input("p1 select deck: 0 = black, 1 = red "))])
        self.p2 = board.Board(decks.decklist[int(input("p2 select deck: 0 = black, 1 = red "))])
        
        # additional pre-execute function calls and references
        self.helpContents = self.helpFile.read()
        self.p1.shuffle()
        self.p2.shuffle()
        
    def on_event(self, event):
        # technical events
        if event == "help":
            print(self.helpContents)
            
        elif event == "quit":
            self._running() == False
            
        # game events
        elif event[0:3] == "cast":
            if self._is_p1_turn:
                self.p1.cast(int(event[5:]))
            else:
                self.p2.cast(int(event[5:]))
            self.update()

        elif event == "pass":
            self._is_p1_turn = not self._is_p1_turn
            self.on_loop()
            
                
    def update(self):
        print("\nPlayer 1\n" + str(self.p1), "\n\n", 
            "Player 2\n" + str(self.p2) + "\nCurrent step: " + self.curr_step) 
        
    def on_loop(self):
        # turn steps
        self.upkeep()
    
    def broadcast_triggers(self):
        self.p1.trigger(self.curr_step, self._is_p1_turn)
        self.p2.trigger(self.curr_step, self._is_p1_turn)
        
    def upkeep(self):
        self.curr_step = "upkeep"
        # triggers card triggers for this step
        self.broadcast_triggers()
        if self._is_p1_turn:
            self.p1.untap_all()
            self.p1.draw(1)
        else:
            self.p2.untap_all()
            self.p2.draw(1)
    
    def on_cleanup(self):
        self.helpFile.close()
        self._running = False
        
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
            
        self.p1.draw(7)
        self.p2.draw(7)
        
        self.update()
        while(self._running):
            self.on_event(re.sub(" {2,}", " ", str(input("Enter command: ")).lower()))
            self.update()
        self.on_cleanup()
        

if __name__ == "__main__":
    theMain = Main()
    theMain.on_execute()