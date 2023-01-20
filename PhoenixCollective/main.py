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
import sys

class Main:
    def __init__(self):
        # initalize variables
        self._running = True
        self._is_p1_turn = False
        self._helpFile = None
        self._curr_phase = None
        self._main_phase_counter = None
        self._pause_queue = None
        self._turn_counter = None
        self.main_phase_total = None
        self._skip_main_1 = False
        self._skip_main_2 = False
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
    
    # method to handle and call appropriate sub-functions for inputted commands
    def on_event(self, event):
        print(event) # DEBUG
        
        # splits event string into a list for easier acess
        _event_list = event.split()
        _do_update = False
        
        if len(_event_list) == 0:
            return None
        
        # -technical events-
        # prints help doc
        if _event_list[0] == "help":
            print(self.helpContents)
        
        # pauses on the next step mentioned to allow for an action
        elif _event_list[0] == "pause":
            self._pause_queue.append(_event_list[0])
            print(self._pause_queue)
        
        elif _event_list[0] == "update":
            _do_update = True
        
        
        # inserts player param if missing
        if len(_event_list) <= 2 and len(_event_list) > 0:
            if self._is_p1_turn:
                _event_list.insert(1, "p1")
            else:
                _event_list.insert(1, "p2")
            
        print(_event_list) # DEBUG
        
        # -game events-
        # casts a card
        if _event_list[0] == "cast":
            _do_update = self.cast(_event_list[1:])

        # passes to a specific phase or to the other player's turn
        elif _event_list[0] == "pass":
            _do_update = self.move(_event_list[2:])
            
        # taps a permanent
        elif _event_list[0] == "tap":
            _do_update = self.tap(_event_list[1:])
        
        # exits game and forefiets player
        elif _event_list[0] == "quit":
            if _event_list[1] == "p1":
                self.p1.lost = True
            else:
                self.p2.lost = True
            _do_update = True
            
        if _do_update:
            self.update()
        
        if _event_list[0] != "pass":
            self.command()

    def cast(self, _event_list):
        # sends command to cast card
        if _event_list[0] == "p1":
            out = self.p1.cast(int(_event_list[1]))
        else:
            out = self.p2.cast(int(_event_list[1]))
        return out
    
    def move(self, _event_list):
        if len(_event_list) == 0 or _event_list[0] == "combat" or _event_list[0] + " " + _event_list[1] == "main 2" or _event_list[0] == "end":
            self._skip_main_1 = True
            
        if len(_event_list) == 0 or _event_list[0] == "end":
            self._skip_main_2 = True
        
        if len(_event_list) > 0:
            out = _event_list[0]
            if len(_event_list) == 2:
                self._main_phase_counter = int(_event_list[1])
                out += _event_list[1]
            
            self._pause_queue.append(out)
        return True
    
    def tap(self, _event_list):
        # inserts default parameter for the target field if missing
        if len(_event_list) < 3:
            _event_list.insert(1, "1")
            
        # taps p1's card
        if _event_list[0] == "p1":
            if _event_list[1] == "0":
                self.p1.decrypt_returns(self.p1.battlefield[int(_event_list[2])].trigger("tap", self._is_p1_turn))
            else:
                self.p1.decrypt_returns(self.p1.landfield[int(_event_list[2])].trigger("tap", self._is_p1_turn))
                
        # taps p2's card
        else:
            if _event_list[1] == "0":
                self.p2.decrypt_returns(self.p2.battlefield[int(_event_list[2])].trigger("tap", not self._is_p1_turn))
            else:
                self.p2.decrypt_returns(self.p2.landfield[int(_event_list[2])].trigger("tap", not self._is_p1_turn))
        return True
    
    
    # method to enter a command to reduce repetition
    def command(self):
        self.on_event(re.sub(" {2,}", " ", str(input("Enter command: ")).lower()))
            
        
    def broadcast_triggers(self, trigger):
        # checks if the trigger is in the pause queue and pauses the game then
        if trigger in self._pause_queue:
            self._pause_queue.remove(trigger)
            self.update()
            print("Paused at " + trigger)
            self.command()
            
        # sends triggers to cards in play that have them, in APNAP order
        if self._is_p1_turn:
            self.p1.on_trigger(trigger, True)
            self.p2.on_trigger(trigger, False)
        else:
            self.p2.on_trigger(trigger, True)
            self.p1.on_trigger(trigger, False)
                        
    def update(self):
        # often enough calls to cover when players lose
        if self.p1.lost or self.p2.lost:
            self.on_loss()

        # prints out the player's board data and other info
        print("\n" * 5 + "Player 1\n" + str(self.p1) + "\n\n" + "Player 2\n" + str(self.p2)
            + "\nTurn " + str(self._turn_counter) + ": Player " + str(int(not self._is_p1_turn) + 1)
            +  " Phase: " + self._curr_phase)
    
    def on_loop(self):
        self._turn_counter += 1
        self._main_phase_counter = 0
        self.main_phase_total = 2
        self._curr_phase = "beginning"
        self._skip_main_1 = False
        self._skip_main_2 = False
        
        if self._is_p1_turn:
            self.p1.lands_remaining = 1
        else:
            self.p2.lands_remaining = 1
        
        # turn phases
        if self._curr_phase == "beginning":
            self.beginning()
        
        if self._curr_phase == "main " + str(self._main_phase_counter):
            self.main(self._skip_main_1)
        
        if self._curr_phase == "combat":
            self.combat()
        
        if self._curr_phase == "main " + str(self._main_phase_counter):
            self.main(self._skip_main_2)
        
        if self._curr_phase == "end":
            self.ending()
        
        self._is_p1_turn = not self._is_p1_turn
    
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
        
    
    def main(self, skip_command):
        self.update()
        if not skip_command:
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
        if self._is_p1_turn:
            self.p1.heal_all()
        else:
            self.p2.heal_all()

        self.broadcast_triggers("cleanup")

    def dice_roll(self, sides, count):
        if count > 0:
            return random.randint(1, sides) + self.dice_roll(sides, count - 1)
        return 0
    
    def on_loss(self):
        if(self.p2.lost):
            print("Player 1 won!")
        else:
            print("Player 2 won!")
        self.on_cleanup()
            
        
    # function to clean up on_execute
    def on_game_startup(self):
        # rolls for who goes first
        _p1_roll = self.dice_roll(6, 2)
        _p2_roll = self.dice_roll(6, 2)
        self._is_p1_turn = _p1_roll > _p2_roll
        # input to wait for player acknoledgement
        input("Player 1 rolled a " + str(_p1_roll) + " and Player 2 rolled a " + str(_p2_roll))
        
        self.p1.draw(7)
        self.p2.draw(7)
        
        self.p1.life_total = 20
        self.p2.life_total = 20
        
    def on_cleanup(self):
        self.helpFile.close()
        self._running = False
        sys.exit()
    
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
            
        self.on_game_startup()
        
        while(self._running):
            self.on_loop()
        self.on_cleanup()
        

if __name__ == "__main__":
    theMain = Main()
    theMain.on_execute()