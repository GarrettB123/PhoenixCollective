#--------------------------------------#
# Title: card.py
# Desc: makes a card object
# Change Log: (Who, When, What)
#   Garrett Bachman, 2022-Dec-29, Created File
#   Garrett Bachman, 2022-Dec-29, Added header
#   Garrett Bachman, 2022-Dec-29, Added code
#   Garrett Bachman, 2023-Jan-01, Added mana function
#--------------------------------------#

import re

class Card:
    def __init__(self, name, color, supertype, type, subtype, cost):
        self.name = name
        self.color = color
        self.supertype = supertype
        self.type = type
        self.subtype = subtype

        # decrypts string costs ("x4brg") into the mana data type
        gen, w, u, b, r, g, c, x = (0, 0, 0, 0, 0, 0, 0, 0)
        for itr, val in enumerate(cost):
            if val == "w":
                w += 1
            elif val == "u":
                u += 1
            elif val == "b":
                b += 1
            elif val == "r":
                r += 1
            elif val == "g":
                g += 1
            elif val == "c":
                c += 1
            elif val.isdigit():
                gen += int(val)
            elif val == "x":
                x += 1
        self.cost = Mana(gen, w, u, b, r, g, c, x)

    def __str__(self):
        return self.name + " — " + " ".join(map(str, self.type))

    def strLong(self):
        #  output: SampleCard is a red Snow Crab Card that costs 0
        return re.sub(" {2,}", " ", self.name + " is a " + self.color + " " 
            + " ".join(map(str, self.supertype)) + " " + " ".join(map(str, self.subtype)) 
            + " " + " ".join(map(str, self.type)) + " that costs " + str(self.cost))

class Land(Card):
    def strLong(self):
        #  output: SampleLand is a red Snow Crab Land
        return super().strLong()[:-12]

class Creature(Card):
    def __init__(self, name, color, supertype, type, subtype, cost, power, toughness):
        super().__init__(name, color, supertype, type, subtype, cost)
        self.power = power
        self.toughness = toughness

    def strLong(self):
        # output: SampleCreature is a 3/6 red Snow Crab Creature that costs 0
        old = super().strLong()
        idx = old.index(" a ") + 3
        return old[:idx]+ str(self.power) + "/" + str(self.toughness) + " " + old[idx:]
    
class Mana:
    # creates a dictionary which holds values of in each color of mana. 
    # generic, white, blue, red, green, colorless and any variable costs
    def __init__(self, gen, w, u, b, r, g, c, x):
        self.mana = {"gen": gen, "w": w, "u": u, "b": b, "r": r, "g": g, "c": c, "x": x}
    
    def __str__(self):
        return re.sub("0", "", ("x" * self.mana.get("x"))
            + str(self.mana.get("gen"))
            + ("w" * self.mana.get("w"))
            + ("u" * self.mana.get("u"))
            + ("b" * self.mana.get("b"))
            + ("r" * self.mana.get("r"))
            + ("g" * self.mana.get("g"))
            + ("c" * self.mana.get("c")))