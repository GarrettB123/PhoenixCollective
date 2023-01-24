#--------------------------------------#
# Title: decks.py
# Desc: holds all decklists for play
# Change Log: (Who, When, What)
#   Garrett Bachman, 2023-Jan-01, Created File
#   Garrett Bachman, 2023-Jan-01, Added header
#   Garrett Bachman, 2023-Jan-01, Added code
#   Garrett Bachman, 2023-Jan-18, Fixed reference issues using deepcopy
#--------------------------------------#

import card
import copy

class Database:
    dictionary = {}
    swamp = card.Land("Swamp", "b", ("Basic",), ("Land",), ("Swamp",), "0", (None,))
    dictionary["swamp"] = swamp

    walking_corpse = card.Creature("Walking Corpse", "b", ("",), ("Creature",), ("Zombie",), "1b", (None,), 2, 2)
    dictionary["walking_corpse"] = walking_corpse

    barony_vampire = card.Creature("Barony Vampire", "b", ("",), ("Creature",), ("Vampire",), "2b", (None,), 3, 2)
    dictionary["barony_vampire"] = barony_vampire

    bogstomper = card.Creature("Bogstomper", "b", ("",), ("Creature",), ("Beast",), "4bb", (None,), 6, 5)
    dictionary["bogstomper"] = bogstomper

    mountain = card.Land("Mountain", "r", ("Basic",), ("Land",), ("Mountain",), "0", (None,))
    dictionary["mountain"] = mountain

    goblin_assailant = card.Creature("Goblin Assailant", "r", ("",), ("Creature",), ("Goblin", "Warrior"), "1r", (None,), 2, 2)
    dictionary["goblin_assailant"] = goblin_assailant

    fearless_halberdier = card.Creature("Fearless Halberdier", "r", ("",), ("Creature",), ("Human", "Warrior"), "2r", (None,), 3, 2)
    dictionary["fearless_halberdier"] = fearless_halberdier

    fire_elemental = card.Creature("Fire Elemental", "r", ("",), ("Creature",), ("Elemental",), "3rr", (None,), 5, 4)
    dictionary["fire_elemental"] = fire_elemental

    dwarven_trader = card.Creature("Dwarven Trader", "r", ("",), ("Creature",), ("Dwarf",), "r", (None,), 1, 1)
    dictionary["dwarven_trader"] = dwarven_trader

    leopard_spotted_jiao = card.Creature("Leopard-Spotted Jiao", "r", ("",), ("Creature",), ("Beast",), "1r", (None,), 3, 1)
    dictionary["leopard_spotted_jiao"] = leopard_spotted_jiao

    bane_alley_blackguard = card.Creature("Bane Alley Blackguard", "b", ("",), ("Creature",), ("Human", "Rogue"), "1b", (None,), 1, 3)
    dictionary["bane_alley_blackguard"] = bane_alley_blackguard

    muck_rats = card.Creature("Muck Rats", "b", ("",), ("Creature",), ("Rat",), "b", (None,), 1, 1)
    dictionary["muck_rats"] = muck_rats


class Deck:
    def __init__(self, size, card_list):
        self.mainlist = []
        self.size = size
        for data_pair in card_list:
            for itr in range(data_pair[0]):
                self.mainlist.append(copy.deepcopy(Database.dictionary[data_pair[1]]))

black = Deck(30, ((4, "walking_corpse"), (4, "barony_vampire"), (2, "bogstomper"), (4, "muck_rats"), (4, "bane_alley_blackguard"), (12, "swamp")))
red = Deck(30, ((4, "goblin_assailant"), (4, "fearless_halberdier"), (2, "fire_elemental"), (4, "leopard_spotted_jiao"), (4, "dwarven_trader"), (12, "mountain")))
decklist = (black, red)