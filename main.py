#--------------------------------------#
# Title: main.py
# Desc: runs the main game loop
# Change Log: (Who, When, What)
#   Garrett Bachman, 2022-Dec-29, Created File
#   Garrett Bachman, 2022-Dec-29, Added header
#   Garrett Bachman, 2022-Dec-29, Added code
#--------------------------------------#

import re
import board
import decks
import random

class Main:
    def __init__(self):
        # initalize variables
        self._running = True
        self._is_p1_turn = False
        self._still_my_turn = False
        self._helpFile = None
        self._curr_phase = None
        self._main_phase_counter = None
        self._pause_queue = None
        self._turn_counter = None
        self.main_phase_total = None
        self.p1 = None
        self.p2 = None
        

    def on_init(self):
        # first references
        self.helpFile = open("help.txt", "r")
        self.p1 = board.Board(decks.decklist[int(input("p1 select deck: 0 = black, 1 = red "))])
        self.p2 = board.Board(decks.decklist[int(input("p2 select deck: 0 = black, 1 = red "))])
        self._pause_queue = []
        self._turn_counter = 0
        
        # additional pre-execute function calls and references
        self.helpContents = self.helpFile.read()
        self.p1.shuffle()
        self.p2.shuffle()
        
    def on_event(self, event):
        print(event) # DEBUG
        # -technical events-
        # prints help doc
        if event == "help":
            print(self.helpContents)
        
        # exits loop
        elif event == "quit":
            self._running() == False
        
        # pauses on the next step mentioned to allow for an action
        elif event[0:5] == "pause":
            self._pause_queue.append(event[6:])
            

        # -game events-
        # plays a card from the hand
        elif event[0:4] == "cast": # TODO: find a way to optimize this logic
            # default cast from player based on current turn
            if event[5:].isdigit():
                if self._is_p1_turn:
                    self.p1.cast(int(event[5:]))
                else:
                    self.p2.cast(int(event[5:]))
            # side case cast from player based on inputted player id
            else:
                if event[5:7] == "p1":
                    self.p1.cast(int(event[8:]))
                elif event[5:7] == "p2":
                    self.p2.cast(int(event[8:]))
            self.update()

        # passes to a specific phase or to the other player's turn
        elif event[0:4] == "pass":
            if len(event) > 4:
                self._curr_phase = event[5:]

                if event[10:].isdigit():
                    self._main_phase_counter = int(event[10:])
            else:
                self._is_p1_turn = not self._is_p1_turn
                self._still_my_turn = False
        if len(re.sub(" ", "", event)):
            self.command()
    
    # method to enter a command to reduce repetition
    def command(self):
        self.on_event(re.sub(" {2,}", " ", str(input("Enter command: ")).lower()))
            
        
    def broadcast_triggers(self, trigger):
        # checks if the trigger is in the pause queue and pauses the game then
        if len(self._pause_queue) > 0 and trigger == self._pause_queue[-1]:
            self._pause_queue.pop()
            self.update()
            print("Paused at " + trigger)
            self.command()
            
        # sends triggers to cards in play that have them, in APNAP order
        if self._is_p1_turn:
            self.p1.trigger(trigger, True)
            self.p2.trigger(trigger, False)
        else:
            self.p2.trigger(trigger, True)
            self.p1.trigger(trigger, False)
                        
    def update(self):
        # prints out the player's board data and other info
        print("\n" * 5 + "Player 1\n" + str(self.p1) + "\n\n" + "Player 2\n" + str(self.p2)
            + "\nCurrent Turn: Player " + str(int(not self._is_p1_turn) + 1)
            +  " Phase: " + self._curr_phase)
    
    def on_loop(self):
        self._turn_counter += 1
        self._main_phase_counter = 0
        self.main_phase_total = 2
        self._curr_phase = "beginning"
        # variable to check if this player has passed or not
        self._still_my_turn = True

        # turn phases
        if self._curr_phase == "beginning" and self._still_my_turn:
            self.beginning()
        
        if (self._curr_phase == "main " + str(self._main_phase_counter)
            and self._still_my_turn):
            self.main()
        
        if self._curr_phase == "combat" and self._still_my_turn:
            self.combat()
        
        if (self._curr_phase == "main " + str(self._main_phase_counter) 
            and self._still_my_turn):
            self.main()
        
        if self._curr_phase == "end" and self._still_my_turn:
            self.ending()
        self.on_event("pass")
    
    def beginning(self):
        self.update()
        self.broadcast_triggers("untap")
        if self._is_p1_turn:
            self.p1.untap_all()
        else:
            self.p2.untap_all()
        
        self.broadcast_triggers("upkeep")
        
        self.broadcast_triggers("draw")
        if self._turn_counter > 1:
            if self._is_p1_turn:
                self.p1.draw(1)
            else:
                self.p2.draw(1)
        self._main_phase_counter += 1
        self._curr_phase = "main " + str(self._main_phase_counter)
        
    
    def main(self):
        self.update()
        self.command()
        if self._main_phase_counter < self.main_phase_total:
            self._curr_phase = "combat"
        else:
            self._curr_phase = "end"
    
    def combat(self):
        self.update()
        self._main_phase_counter += 1
        self._curr_phase = "main " + str(self._main_phase_counter)
    
    def ending(self):
        self.update()
        self.broadcast_triggers("end")
        self.broadcast_triggers("cleanup")

    def dice_roll(self, sides, count):
        if count > 0:
            return random.randint(1, sides) + self.dice_roll(sides, count - 1)
        return 0
    
    def on_cleanup(self):
        self.helpFile.close()
        self._running = False
        
    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        _p1_roll = self.dice_roll(6, 2)
        _p2_roll = self.dice_roll(6, 2)
        self._is_p1_turn = _p1_roll > _p2_roll
        print("Player 1 rolled a " + str(_p1_roll) + " and Player 2 rolled a " + str(_p2_roll), end="")
        
        self.p1.draw(7)
        self.p2.draw(7)
        
        while(self._running):
            self.on_loop()
        self.on_cleanup()
        

if __name__ == "__main__":
    theMain = Main()
    theMain.on_execute()