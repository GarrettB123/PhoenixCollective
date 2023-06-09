#--------------------------------------#
# Title: card.py
# Desc: makes a card object
# Change Log: (Who, When, What)
#   Garrett Bachman, 2022-Dec-29, Created File
#   Garrett Bachman, 2022-Dec-29, Added header
#   Garrett Bachman, 2022-Dec-29, Added code
#   Garrett Bachman, 2023-Jan-01, Added mana function
#   Garrett Bachman, 2023-Mar-23, Added Instant, Sorcery, and Enchantment classes
#   Garrett Bachman, 2023-Mar-23, Added target function
#--------------------------------------#

import re

# TODO: instant, sorcery, enchantment
class Card:
    def __init__(self, name, color, supertype, type, subtype, cost, keywords):
        self.name = name
        self.color = color
        self.supertype = supertype
        self.type = type
        self.subtype = subtype
        self.keywords = keywords
        self.target = None
        self.ownership = None
        self.state = "untapped"
        self.field = "library"

        # decrypts string costs ("x4brg") into the mana data type
        gen, w, u, b, r, g, c, x = 0, 0, 0, 0, 0, 0, 0, 0
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
        

    def trigger(self, event, is_my_turn):
        pass
    
    def __str__(self):
        output = self.name 
        if self.field != "battlefield":
            output += " — " + " ".join(map(str, self.type)) + " (" + str(self.cost) + ")" 
        elif self.state != "untapped":
            output += " (" + self.state + ")"
        return output

    def str_long(self):
        #  output: SampleCard is a red Snow Crab Card that costs 0 with trample
        out = re.sub(" {2,}", " ", self.name + " is a " + self.color + " " 
            + " ".join(map(str, self.supertype)) + " " + " ".join(map(str, self.subtype)) 
            + " " + " ".join(map(str, self.type)) + " that costs " + str(self.cost))
        if self.keywords[0] != None:
            out += " with " + ", ".join(map(str, self.keywords))
        return out
    
class Land(Card):
    def str_long(self):
        print(self.cost)
        #  output: SampleLand is a red Snow Crab Land
        return super().str_long()[:-13]
    
    # basic land taps for triggers
    def trigger(self, event, is_my_turn):
        if event == "tap" and self.state == "untapped":
            self.state = "tapped"
            output = ["mana"]
            if len(self.subtype) >= 1:
                for type in self.subtype:
                    if type == "Plains":
                        output.append(("w", 1))
            
                    elif type == "Island":
                        output.append(("u", 1))
            
                    elif type == "Swamp":
                        output.append(("b", 1))
                
                    elif type == "Mountain":
                        output.append(("r", 1))
            
                    elif type == "Forest":
                        output.append(("g", 1))
            return output
            
    def __str__(self):
        if self.field == "battlefield":
            return super().__str__()
        return super().__str__()[:-4]

class Creature(Card):
    def __init__(self, name, color, supertype, type, subtype, cost, keywords, power, toughness):
        super().__init__(name, color, supertype, type, subtype, cost, keywords)
        self.base_power = power
        self.base_toughness = toughness
        self.temp_power = power
        self.temp_toughness = toughness
        self.in_combat = False
        self.is_blocked = False
    
    def heal(self):
        self.temp_power = self.base_power
        self.temp_toughness = self.base_toughness
    
    def trigger(self, event, is_my_turn):
        if event == "attack":
            self.in_combat = True
            if "vigilance" not in self.keywords:
                self.state = "tapped"

        elif event == "is_blocked":
            self.is_blocked = True

    def str_long(self):
        # output: SampleCreature is a 3/6 red Snow Crab Creature that costs 0
        old = super().str_long()

        # pinpoints target after the variable length name and before the color
        idx = old.index(" is a ") + 6
        return old[:idx]+ str(self.base_power) + "/" + str(self.base_toughness) + " " + old[idx:]

    def __str__(self):
        return super().__str__() + "[" + str(self.base_power) + "/" + str(self.temp_toughness) + "]"

class Enchantment(Card):
    def trigger(self):
        pass

class Artifact(Card):
    def trigger(self):
        pass

class Instant(Card):
    def trigger(self):
        pass
class Sorcery(Instant):
    def trigger(self):
        pass
    
    
    
    
        
class Mana:
# creates a dictionary which holds values of in each color of mana. 
# generic, white, blue, red, green, colorless and any variable costs
    def __init__(self, n, w, u, b, r, g, c, x):
        self.mana = {"n": n, "w": w, "u": u, "b": b, "r": r, "g": g, "c": c, "x": x}
    
    def __str__(self):
        out = re.sub("0", "", ("x" * self.mana.get("x")
            + str(self.mana.get("n"))
            + ("w" * self.mana.get("w"))
            + ("u" * self.mana.get("u"))
            + ("b" * self.mana.get("b"))
            + ("r" * self.mana.get("r"))
            + ("g" * self.mana.get("g"))
            + ("c" * self.mana.get("c"))))
        if out == "":
            return "0"
        return out
    
    def max_key(self):
        max = 0
        out = ""
        for key in self.mana.keys():
            if self.mana[key] > max:
                max = self.mana[key]
                out = key
        return out

    # returns the converted mana cost
    def cmc(self):
        return sum(self.mana.values())
    
    def reset(self):
        self.mana = {"n": 0, "w": 0, "u": 0, "b": 0, "r": 0, "g": 0, "c": 0, "x": 0}