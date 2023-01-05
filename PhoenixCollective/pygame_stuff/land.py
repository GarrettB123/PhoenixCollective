#--------------------------------------#
# Title: land.py
# Desc: creates a new land object, subclass of card
# Change Log: (Who, When, What)
#   Garrett Bachman, 2022-Nov-14, Created File
#   Garrett Bachman, 2022-Nov-14, Added header
#   Garrett Bachman, 2022-Nov-14, Added code
#--------------------------------------#

import os, pygame as pg, card, cost
class Land(card.Card):
    def __init__(self, name, color, cost):
        card.__init__(self, name, color, cost)