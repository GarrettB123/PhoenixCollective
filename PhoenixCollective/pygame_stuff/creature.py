#--------------------------------------#
# Title: creature.py
# Desc: creates a new Creature object, subclass of card
# Change Log: (Who, When, What)
#   Garrett Bachman, 2022-Nov-04, Created File
#   Garrett Bachman, 2022-Nov-04, Added header
#   Garrett Bachman, 2022-Nov-04, Added code
#--------------------------------------#

import os, pygame as pg, card, cost
class Creature(card.Card):
    def __init__(self, name, color, cost, power, toughness):
        card.__init__(self, name, color, cost)
        self.power = power
        self.toughness = toughness