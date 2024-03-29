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
        self._skip_combat = False
        self._mull_count_p1 = None
        self._mull_count_p2 = None
        self.p1 = None
        self.p2 = None
        

    def on_init(self):
        # first references
        self.helpFile = open("help.txt", "r")
        self.p1 = board.Board(decks.decklist[int(input("p1 select deck: 0 = black, 1 = red "))])
        self.p2 = board.Board(decks.decklist[int(input("p2 select deck: 0 = black, 1 = red "))])
        self._pause_queue = []
        self._turn_counter = 0
        self._mull_count_p1 = 0
        self._mull_count_p2 = 0
        
        # additional pre-execute function calls and references
        self.helpContents = self.helpFile.read()
        self.p1.shuffle()
        self.p2.shuffle()
    
    # method to handle and call appropriate sub-functions for inputted commands
    def on_event(self, event):
        
        # splits event string into a list for easier acess
        _event_list = event.split()
        _do_update = False
        
        if len(_event_list) == 0:
            return None
        
        # -TECH EVENTS-
        # prints help doc
        if _event_list[0] == "help":
            print(self.helpContents)
        
        # pauses on the next step mentioned to allow for an action
        elif _event_list[0] == "pause":
            self._pause_queue.append(_event_list[0])
            print(self._pause_queue)
        
        elif _event_list[0] == "update":
            _do_update = True
        
        elif _event_list[0] == "desc":
            print(decks.Database.dictionary[_event_list[1]].str_long())
        
        
        # inserts player param if missing
        if len(_event_list) > 0:
            if len(_event_list) >= 2 and _event_list[1][0] == "p":
                pass
            elif self._is_p1_turn:
                _event_list.insert(1, "p1")
            else:
                _event_list.insert(1, "p2")
        
        
        # -GAME EVENTS-
        # casts a card
        if _event_list[0] == "cast":
            _do_update = self.cast(_event_list[1:])

        # passes to a specific phase or to the other player's turn
        elif _event_list[0] == "pass":
            _do_update = self.move(_event_list[2:])
            
        # taps a permanent
        elif _event_list[0] == "tap":
            _do_update = self.tap(_event_list[1:])
        
        # exits game and forfiets player
        elif _event_list[0] == "quit":
            if _event_list[1] == "p1":
                self.p1.lost = True
            else:
                self.p2.lost = True
            _do_update = True
        
        # lists all cards in target player's graveyard
        elif _event_list[0] == "graveyard":
            if _event_list[1] == "p1":
                print("Player 1's graveyard: " + ", ".join(map(str, self.p1.graveyard)))
            else:
                print("Player 2's graveyard: " + ", ".join(map(str, self.p2.graveyard)))
        
        # discards x cards
        elif _event_list[0] == "discard":
            _do_update = self.discard(_event_list[1:])

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
    
    # method that passes turn and to steps on command
    def move(self, _event_list):
        # checks if passing skips input phases
        if len(_event_list) == 0 or _event_list[0] == "combat" or _event_list[0] == "end" or _event_list[0] + " " + _event_list[1] == "main 2":
            self._skip_main_1 = True
            if len(_event_list) == 0 or _event_list[0] == "end" or _event_list[0] + " " + _event_list[1] == "main 2":
                self._skip_combat = True
                if len(_event_list) == 0 or _event_list[0] == "end":
                    self._skip_main_2 = True
        
        if len(_event_list) > 0:
            out = _event_list[0]
            if len(_event_list) == 2:
                out += " " + _event_list[1]
            self._pause_queue.append(out)
        else:
            return True
        
    
    def tap(self, _event_list):
        # inserts default parameter for the target field if missing
        if len(_event_list) < 3:
            _event_list.insert(1, "1")
        
        # taps lands
        if _event_list[1] == "1":
            # taps multiple lands at once
            if _event_list[0] == "p1":
                if _event_list[2][0] == "t":
                    self.p1.multi_tap(_event_list[2])
                else:
                    self.p1.decrypt_returns(self.p1.landfield[int(_event_list[2])].trigger("tap", self._is_p1_turn))
                    self.p1.land_mana -= 1
            else:
                if _event_list[2][0] == "t":
                    self.p2.multi_tap(_event_list[2])
                else:
                    self.p2.decrypt_returns(self.p2.landfield[int(_event_list[2])].trigger("tap", not self._is_p1_turn))
                    self.p2.land_mana -= 1
                
        # taps battlefield cards
        else:
            if _event_list[0] == "p1":
                self.p1.decrypt_returns(self.p1.battlefield[int(_event_list[2])].trigger("tap", self._is_p1_turn))
            else:
                self.p2.decrypt_returns(self.p2.battlefield[int(_event_list[2])].trigger("tap", not self._is_p1_turn))
        return True
    
    def discard(self, events):
        remove = input("Select " + events[1] + " card(s) to send to discard: ").split()
        _count = 0
        for idx in remove:
            if events[0] == "p1":
                self.p1.graveyard.append(self.p1.hand.pop(int(idx) - _count))
            else:
                self.p2.graveyard.append(self.p2.hand.pop(int(idx) - _count))
            _count += 1
        return True
                
    # method to enter a command to reduce repetition
    def command(self):
        self.on_event(re.sub(" {2,}", " ", str(input("Enter command: ")).lower()))
            
        
    def broadcast_triggers(self, trigger):
        # checks if the trigger is in the pause queue and pauses the game
        if trigger in self._pause_queue:
            self._pause_queue.remove(trigger)
            self.update()
            print("\nPaused at " + trigger + "!\n")
            self.command()
            
        # sends triggers to cards in play that have them, in APNAP order
        if self._is_p1_turn:
            self.p1.on_trigger(trigger, True)
            self.p2.on_trigger(trigger, False)
        else:
            self.p2.on_trigger(trigger, True)
            self.p1.on_trigger(trigger, False)
                        
    def update(self):
        # cover when players lose
        if self.p1.life_total <= 0:
            self.p1.lost = True
        elif self.p2.life_total <= 0:
            self.p2.lost = True

        if self.p1.lost or self.p2.lost:
            self.on_loss()

        # checks for card state exceptions, ex dead creatures
        for card in self.p1.battlefield:
            if "Creature"in card.type and card.temp_toughness <= 0:
                print(card.name + " died!")
                card.field = "graveyard"
                card.state = "untapped"
                self.p1.graveyard.append(self.p1.battlefield.remove(card))

        for card in self.p2.battlefield:
            if "Creature"in card.type and card.temp_toughness <= 0:
                print(card.name + " died!")
                card.field = "graveyard"
                card.state = "untapped"
                self.p2.graveyard.append(self.p2.battlefield.remove(card))

        # prints out the player's board data and other info, change /n multiplier to 48 in final version
        print("\n" * 48 + "Turn " + str(self._turn_counter) + " (Player " + str(int(not self._is_p1_turn) + 1)
            + ") Phase: " + self._curr_phase
            + "\n" + "--Player 1--\n" + str(self.p1) + "\n\n" + "--Player 2--\n" + str(self.p2))
    
    def on_loop(self):
        self._turn_counter += 1
        self._main_phase_counter = 0
        self.main_phase_total = 2
        self._curr_phase = "beginning"
        self._skip_main_1 = False
        self._skip_main_2 = False
        self._skip_combat = False
        
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
    
    # method for all parts of the beginning step
    def beginning(self):
        self.broadcast_triggers("untap")
        self.update()
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
    
    # method for any main step
    def main(self, skip_command):
        self.broadcast_triggers("main " + str(self._main_phase_counter))
        self.update()
        if not skip_command:
            self.command()
        
        if self.main_phase_total == self._main_phase_counter:
            self._curr_phase = "end"    

        elif self._main_phase_counter < self.main_phase_total or self._skip_main_1:
            self._curr_phase = "combat"
    
    # method for combat step and logic for combat
    def combat(self):
        self.broadcast_triggers("combat")
        _skip = ""
        self.update()
        # if theres stuff on the field of the current player prompt to skip combat
        if not self._skip_combat and ((self._is_p1_turn and len(self.p1.battlefield) != 0 and self.p1.can_combat("")) 
            or (not self._is_p1_turn and len(self.p2.battlefield) != 0 and self.p2.can_combat(""))):
            _skip = input("\nSkip combat? y/n ")
            if _skip == "y":
                self._skip_combat = True
            
        else:
            self._skip_combat = True
            
        if not self._skip_combat:
            # gathers attacker data and sorts out appropriate references               
            _attacker_list = input("Select attackers from battlefield: ").split()
            _count = 0
            for attacker in _attacker_list:
                if self._is_p1_turn:
                    if self.p1.battlefield[int(attacker)].state == "untapped":
                        _attacker_list[_count] = self.p1.battlefield[int(attacker)]
                    else: 
                        print("Attacker in invalid state")
                else:
                    if self.p2.battlefield[int(attacker)].state == "untapped":
                        _attacker_list[_count] = self.p2.battlefield[int(attacker)]
                    else: 
                        print("Attacker in invalid state")
                _attacker_list[_count].trigger("attack", True)
                _count += 1

            print()
            if self._is_p1_turn:
                print("Player 1", end = "")
            else:
                print("Player 2", end = "")
            print(" attacking with: " + ", ".join(map(str, _attacker_list)))
            
            
        # if theres stuff on the field of the current player prompt to skip blocking
        if not self._skip_combat and ((self._is_p1_turn and len(self.p2.battlefield) != 0 and self.p2.can_combat("blk")) 
            or (not self._is_p1_turn and len(self.p1.battlefield) != 0 and self.p1.can_combat("blk"))):
            _skip = input("\nSkip blocking? y/n ")

        else:
            _skip = "y"
                
        if _skip == "n":
            # Gather blocker data
            if self._is_p1_turn:
                print("Player 2", end = "")
            else:
                print("Player 1", end = "")
            _blocker_setup = input(" select blockers (format: 0v2, 3v1): ").split(", ")

            print()
            _count = 0
            for pair in _blocker_setup:
                temp = pair.split("v")
                _blocker_setup[_count] = [None, _attacker_list[int(temp[1])]]

                # fills list with references to the creatures mentioned, triggers
                if self._is_p1_turn:
                    if self.p2.battlefield[int(temp[0])].state != "tapped":
                        _blocker_setup[_count][0] = self.p2.battlefield[int(temp[0])]
                    else:
                        print("Blocker in invalid state")

                else:
                    if self.p1.battlefield[int(temp[0])].state != "tapped":
                        _blocker_setup[_count][0] = self.p1.battlefield[int(temp[0])]
                    else:
                        print("Blocker in invalid state")

                _blocker_setup[_count][0].trigger("block", False)
                _blocker_setup[_count][1].is_blocked = True

                # prints each blocking pair
                if _count != len(_blocker_setup) - 1:
                    print(" vs ".join(map(str, _blocker_setup[_count])), end = ", ")
                else:
                    print(" vs ".join(map(str, _blocker_setup[_count])))
                        
                # blocking and damage, assignment to not mess up values due to non-simultaneous execution
                _blk_tmp_tgh = _blocker_setup[_count][0].temp_toughness
                _blk_tmp_pow = _blocker_setup[_count][0].temp_power
                _atk_tmp_tgh = _blocker_setup[_count][1].temp_toughness
                _atk_tmp_pow = _blocker_setup[_count][1].temp_power

                # fix for negative power issue
                if _atk_tmp_pow < _blk_tmp_tgh:
                    _blocker_setup[_count][1].temp_power -= _atk_tmp_pow
                else:
                    _blocker_setup[_count][1].temp_power -= _blk_tmp_tgh
                
                if _blk_tmp_pow < _atk_tmp_tgh:
                    _blocker_setup[_count][0].temp_power -= _blk_tmp_pow
                else:
                    _blocker_setup[_count][0].temp_power -= _atk_tmp_tgh

                _blocker_setup[_count][1].temp_toughness -= _blk_tmp_pow
                _blocker_setup[_count][0].temp_toughness -= _atk_tmp_pow

                _blocker_setup[_count][0].in_combat = False
                _count += 1
            
        # hitting the other player
        if not self._skip_combat:
            if self._is_p1_turn:
                _pre_life = self.p2.life_total
            else:
                _pre_life = self.p1.life_total
        
            for attacker in _attacker_list:
                if not attacker.is_blocked or "trample" in attacker.keywords:
                    if self._is_p1_turn:
                        self.p2.life_total -= attacker.temp_power
                    else:
                        self.p1.life_total -= attacker.temp_power
                attacker.in_combat = False
            if self._is_p1_turn:
                input("Player 2 lost " + str(_pre_life - self.p2.life_total) + " life!")
            else:
                input("Player 1 lost " + str(_pre_life - self.p1.life_total) + " life!")
                
        
        self._main_phase_counter += 1
        self._curr_phase = "main " + str(self._main_phase_counter)
    
    # method for ending step
    def ending(self):
        self.broadcast_triggers("end")
        self.update()
        # repairs damaged creatures
        if self._is_p1_turn:
            self.p1.heal_all()
        else:
            self.p2.heal_all()

        self.broadcast_triggers("cleanup")
        if self._is_p1_turn and len(self.p1.hand) > self.p1.max_hand:
            self.discard(("p1", str(len(self.p1.hand) - self.p1.max_hand)))

        elif not self._is_p1_turn and len(self.p2.hand) > self.p2.max_hand:
            self.discard(("p2", str(len(self.p2.hand) - self.p2.max_hand)))

    # wide use case dice roll function that uses a bit of recursion
    def dice_roll(self, sides, count):
        if count > 0:
            return random.randint(1, sides) + self.dice_roll(sides, count - 1)
        return 0
    
    # prints win/loss messages
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

        # rerolls if tied
        while _p1_roll == _p2_roll:
            _p1_roll = self.dice_roll(6, 2)
            _p2_roll = self.dice_roll(6, 2)
        self._is_p1_turn = _p1_roll > _p2_roll

        # input to wait for player acknoledgement
        input("Player 1 rolled a " + str(_p1_roll) + " and Player 2 rolled a " + str(_p2_roll))
        
        self.p1.draw(7)
        self.p2.draw(7)
        
        self.p1.life_total = 20
        self.p2.life_total = 20

        print()

        # handles mulligans
        print("Player 1 hand: " + ", ".join(map(str, self.p1.hand)))
        print()
        print("Player 2 hand: " + ", ".join(map(str, self.p2.hand)))
        _p1_confirm = False
        _p2_confirm = False
        print("Enter 'mulligan p1/p2' or 'keep p1/p2'")

        while not _p1_confirm or not _p2_confirm:
            comm = input().split()
            if len(comm) == 0:
                break

            if comm[0] == "mulligan":
                self.mulligan(comm[1])

            else:
                if comm[1] == "p1":
                    _p1_confirm = True
                elif comm[1] == "p2":
                    _p2_confirm = True
                else:
                    break

    def mulligan(self, player):
        if player == "p1":
            for itr in range(len(self.p1.hand)):
                self.p1.library.append(self.p1.hand.pop())
            self.p1.shuffle()
            self.p1.draw(7)
            print("Player 1 hand: " + ", ".join(map(str, self.p1.hand)))
            self._mull_count_p1 += 1

            if self._mull_count_p1 > 1:
                remove = input("Select " + str(self._mull_count_p1 - 1) + " card(s) to send to the bottom of your library: ").split()
                _count = 0
                for idx in remove:
                    self.p1.library.insert(0, self.p1.hand.pop((int(idx) - _count)))
                    _count += 1
                print("Player 1 hand: " + ", ".join(map(str, self.p1.hand)))

        else:
            for itr in range(len(self.p2.hand)):
                self.p2.library.append(self.p2.hand.pop())
            self.p2.shuffle()
            self.p2.draw(7)
            print("Player 2 hand: " + ", ".join(map(str, self.p2.hand)))
            self._mull_count_p2 += 1

            if self._mull_count_p2 > 1:
                remove = input("Select " + str(self._mull_count_p2 - 1) + " card(s) to send to the bottom of your library: ").split()
                _count = 0
                for idx in remove:
                    self.p2.library.insert(0, self.p2.hand.pop((int(idx) - _count)))
                    _count += 1
                print("Player 2 hand: " + ", ".join(map(str, self.p2.hand)))


    # closes and exits when the program ends
    def on_cleanup(self):
        self.helpFile.close()
        self._running = False
        sys.exit()
    
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
            
        self.on_game_startup()
        
        # loops once for a turn and ends once a player loses
        while(self._running):
            self.on_loop()
        self.on_cleanup()
        

if __name__ == "__main__":
    theMain = Main()
    theMain.on_execute()