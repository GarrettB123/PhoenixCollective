#--------------------------------------#
# Title: database.py
# Desc: contains hard-data classes for every card
# Change Log: (Who, When, What)
#   Garrett Bachman, 2023-Mar-24, Created File
#   Garrett Bachman, 2023-Mar-24, Added header
#   Garrett Bachman, 2023-Mar-24, Added code
#--------------------------------------#

import card
import board
# card database, organized by color(wubrgc) --> cmc (ascending)
dictionary = {}

# --LANDS--
# Basic lands
dictionary["Plains"] = card.Land("Plains", "w", {"Basic"}, {"Land"}, {"Plains"}, "0", {})

dictionary["Island"] = card.Land("Island", "u", {"Basic"}, {"Land"}, {"Island"}, "0", {})

dictionary["Swamp"] = card.Land("Swamp", "b", {"Basic"}, {"Land"}, {"Swamp"}, "0", {})


dictionary["Mountain"] = card.Land("Mountain", "r", {"Basic"}, {"Land"}, {"Mountain"}, "0", {})

dictionary["Forest"] = card.Land("Forest", "g", {"Basic"}, {"Land"}, {"Forest"}, "0", {})

dictionary["Wastes"] = card.Land("Wastes", "c", {"Basic"}, {"Land"}, {"Wastes"}, "0", {})

# --WHITE--
# 0-CMC
# 1-CMC    
# 2-CMC
# 3-CMC
# 6-CMC
# 7-CMC
# 8-CMC
# 9-CMC
# 10-CMC

# --BLUE--
# 0-CMC
# 1-CMC
dictionary["Fugitive Wizard"] = card.Creature("Fugitive Wizard", "u", {}, {"Creature"}, {"Human", "Wizard"}, "u", {}, 1, 1)

dictionary["Merfolk of the Pearl Trident"] = card.Creature("Merfolk of the Pearl Trident", "u", {}, {"Creature"}, {"Merfolk"}, "u", {}, 1, 1)
class ReachThroughMists(card.Instant):
    def __init__(self):
        super().__init__("Reach Through Mists", "u", {}, {"Instant"}, {"Arcane"}, "u", {})
    def trigger(self, event, is_my_turn):
        if event == "etb":
            return ("draw", 1)
dictionary["Reach Through Mists"] = ReachThroughMists()
# 2-CMC
dictionary["Sworn Guardian"] = card.Creature("Sworn Guardian", "u", {}, {"Creature"}, {"Merfolk", "Warrior"} ,"1u", {}, 1, 3)
# 3-CMC
dictionary["Tolarian Scholar"] = card.Creature("Tolarian Scholar", "u", {}, {"Creature"}, {"Human", "Wizard"} ,"2u", {}, 2, 3)
# 6-CMC
# 7-CMC
# 8-CMC
# 9-CMC
# 10-CMC
# 11-CMC
# 12-CMC
# 14-CMC

# --BLACK--
# 0-CMC
# 1-CMC
dictionary["Muck Rats"] = card.Creature("Muck Rats", "b", {}, {"Creature"}, {"Rat"}, "b", {}, 1, 1)
# 2-CMC
dictionary["Walking Corpse"] = card.Creature("Walking Corpse", "b", {}, {"Creature"}, {"Zombie"}, "1b", {}, 2, 2)

dictionary["Bane Alley Blackguard"] = card.Creature("Bane Alley Blackguard", "b", {}, {"Creature"}, {"Human", "Rogue"}, "1b", {}, 1, 3)
# 3-CMC
dictionary["Barony Vampire"] = card.Creature("Barony Vampire", "b", {}, {"Creature"}, {"Vampire"}, "2b", {}, 3, 2)
# 6-CMC
dictionary["Bogstomper"] = card.Creature("Bogstomper", "b", {}, {"Creature"}, {"Beast"}, "4bb", {}, 6, 5)
# 7-CMC
# 8-CMC
# 9-CMC
# 10-CMC
# 11-CMC
# 12-CMC
# 15-CMC

# --RED--
# 0-CMC
# 1-CMC
dictionary["Dwarven Trader"] = card.Creature("Dwarven Trader", "r", {}, {"Creature"}, {"Dwarf"}, "r", {}, 1, 1)

class Shock(card.Instant):
    def __init__(self):
        super().__init__("Shock", "r", {}, {"Instant"}, {}, "r", {})
    def trigger(self, event, is_my_turn):
        if event == "etb":
            if type(self.target) is board.Board:
                self.target.life_total -= 2
                print(self.target.name, "took 2 damage!")
            elif type(self.target) is card.Creature:
                self.target.temp_toughness -= 2
                print(str(self.target), "took 2 damage!")
        elif event == "is_cast":
            return ("target", {"any"})
dictionary["Shock"] = Shock()
# 2-CMC
dictionary["Leopard-Spotted Jiao"] = card.Creature("Leopard-Spotted Jiao", "r", {}, {"Creature"}, {"Beast"}, "1r", {}, 3, 1)

dictionary["Goblin Assailant"] = card.Creature("Goblin Assailant", "r", {}, {"Creature"}, {"Goblin", "Warrior"}, "1r", {}, 2, 2)
# 3-CMC
dictionary["Fearless Halberdier"] = card.Creature("Fearless Halberdier", "r", {}, {"Creature"}, {"Human", "Warrior"}, "2r", {}, 3, 2)
# 4-CMC
# 5-CMC
dictionary["Fire Elemental"] = card.Creature("Fire Elemental", "r", {}, {"Creature"}, {"Elemental"}, "3rr", {}, 5, 4)
# 6-CMC
# 7-CMC
# 8-CMC
# 9-CMC
# 10-CMC
# 12-CMC

# --GREEN--
# 0-CMC
# 1-CMC    
# 2-CMC
# 3-CMC
# 6-CMC
# 7-CMC
# 8-CMC
# 9-CMC
# 10-CMC
# 11-CMC
# 12-CMC
# 15-CMC

# --MULTI-COLORED--
# 0-CMC
# 1-CMC    
# 2-CMC
# 3-CMC
# 6-CMC
# 7-CMC
# 8-CMC
# 9-CMC
# 10-CMC
# 11-CMC
# 12-CMC
# 13-CMC
# 15-CMC

# --COLORLESS--
# 0-CMC
# 1-CMC    
# 2-CMC
# 3-CMC
# 6-CMC
# 7-CMC
# 8-CMC
# 9-CMC
# 10-CMC
# 11-CMC
# 12-CMC
# 13-CMC
# 15-CMC
# 16-CMC